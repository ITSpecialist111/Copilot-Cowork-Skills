#!/usr/bin/env python3
"""
Report Data Validator - helper for the executive-report-design-system skill.

Validates a report data document against the contract in
references/report.schema.json, without requiring the `jsonschema` package. The
repository standard is zero external dependencies, so the subset of JSON Schema
this package actually uses is implemented directly.

Validation is not bureaucracy here. The whole promise of the design system is
"same JSON in, same HTML out". That only holds if the JSON is known-good before
rendering starts, so this runs as a gate, not as a suggestion.

Usage:
    python scripts/validate_report.py report.json
    python scripts/validate_report.py report.json --schema references/report.schema.json
    python scripts/validate_report.py report.json --quiet

Exit codes:
    0  valid
    1  invalid - errors printed to stdout
    2  could not run (file missing, malformed JSON)
"""

import argparse
import json
import os
import sys

# Components the renderer knows how to draw. Anything else is a typo or an
# invention, and inventions are what this whole package exists to prevent.
KNOWN_BLOCKS = {
    "cover", "toc", "divider",
    "hero", "display", "sectionHead",
    "kpiRow", "barList", "trend", "compareStrip", "statusGrid", "dataTable",
    "flowStrip", "numberedCards", "highlights",
    "prose", "riskCallout", "pullQuote", "noteStrip", "sourceNote",
}

PALETTES = {
    "palette-warm-paper",
    "palette-clean-white",
    "palette-deep-ink",
    "palette-slate",
}

# Blocks whose payload we check in detail, and what they must carry.
REQUIRED_FIELDS = {
    "hero": ["text"],
    "kpiRow": ["cards"],
    "barList": ["items"],
    "trend": ["points"],
    "statusGrid": ["items"],
    "compareStrip": ["columns"],
    "riskCallout": ["title", "body"],
    "prose": ["sections"],
    "highlights": ["cards"],
    "numberedCards": ["cards"],
    "flowStrip": ["steps"],
    "dataTable": ["columns", "rows"],
    "pullQuote": ["quote"],
    "noteStrip": ["text"],
    "sourceNote": ["text"],
    "toc": ["items"],
    "divider": ["title"],
    "cover": [],
    "display": ["text"],
    "sectionHead": ["title"],
}


class Problem(object):
    """One validation failure, with the path that produced it."""

    def __init__(self, path, message, hint=None):
        self.path = path
        self.message = message
        self.hint = hint

    def __str__(self):
        line = "  %s\n      %s" % (self.path or "(root)", self.message)
        if self.hint:
            line += "\n      hint: %s" % self.hint
        return line


def _require(obj, key, path, problems, kind=None, kind_name=None):
    if key not in obj:
        problems.append(Problem(path, 'missing required property "%s"' % key))
        return None
    value = obj[key]
    if kind is not None and not isinstance(value, kind):
        problems.append(
            Problem("%s.%s" % (path, key), "must be %s, got %s" % (kind_name, type(value).__name__))
        )
        return None
    return value


def validate_meta(meta, problems):
    path = "meta"
    if not isinstance(meta, dict):
        problems.append(Problem(path, "must be an object"))
        return

    for key in ("wordmark", "title", "period"):
        _require(meta, key, path, problems, str, "a string")

    palette = meta.get("palette")
    if palette is not None and palette not in PALETTES:
        problems.append(
            Problem(
                "meta.palette",
                '"%s" is not a known palette' % palette,
                "one of: %s" % ", ".join(sorted(PALETTES)),
            )
        )

    wordmark = meta.get("wordmark")
    if isinstance(wordmark, str) and len(wordmark) > 24:
        problems.append(
            Problem("meta.wordmark", "is %d characters" % len(wordmark),
                    "the running head is small; keep the wordmark under 24 characters")
        )


def validate_block(block, path, problems):
    if not isinstance(block, dict):
        problems.append(Problem(path, "must be an object"))
        return

    btype = block.get("type")
    if btype is None:
        problems.append(Problem(path, 'missing required property "type"'))
        return

    if btype not in KNOWN_BLOCKS:
        problems.append(
            Problem(
                "%s.type" % path,
                '"%s" is not a component in the catalogue' % btype,
                "see references/component-catalogue.md - do not invent components",
            )
        )
        return

    for field in REQUIRED_FIELDS.get(btype, []):
        if field not in block:
            problems.append(
                Problem(path, 'a "%s" block requires "%s"' % (btype, field))
            )

    # ---- per-component checks that catch the mistakes that actually happen ----

    if btype == "hero":
        text = block.get("text", "")
        if isinstance(text, str):
            if "{{" not in text:
                problems.append(
                    Problem("%s.text" % path,
                            "no figure is marked for the accent colour",
                            "wrap the figures that matter in {{ }}, e.g. 'closed {{$1.9M}} in Q2'")
                )
            if text.count("{{") != text.count("}}"):
                problems.append(Problem("%s.text" % path, "unbalanced {{ }} markers"))
            if len(text) > 220:
                problems.append(
                    Problem("%s.text" % path, "is %d characters" % len(text),
                            "the hero is one sentence; over ~220 characters it stops working as a statement")
                )

    if btype == "kpiRow":
        cards = block.get("cards")
        if isinstance(cards, list):
            if not 2 <= len(cards) <= 4:
                problems.append(
                    Problem("%s.cards" % path, "has %d cards" % len(cards),
                            "use 3 or 4; 5+ stops being a summary")
                )
            for i, card in enumerate(cards):
                cpath = "%s.cards[%d]" % (path, i)
                if not isinstance(card, dict):
                    problems.append(Problem(cpath, "must be an object"))
                    continue
                _require(card, "label", cpath, problems, str, "a string")
                value = _require(card, "value", cpath, problems, str, "a string")
                if isinstance(value, str):
                    if not any(ch.isdigit() for ch in value):
                        problems.append(
                            Problem("%s.value" % cpath, '"%s" contains no digit' % value,
                                    "the motion engine counts up to a number; a value with no digit will not animate")
                        )
                    if value.strip() in ("0", "0.0", "-"):
                        problems.append(
                            Problem("%s.value" % cpath, "is a placeholder",
                                    "write the real final figure; the engine animates to whatever is in the markup")
                        )

    if btype == "barList":
        items = block.get("items")
        if isinstance(items, list):
            if len(items) > 8:
                problems.append(
                    Problem("%s.items" % path, "has %d bars" % len(items),
                            "over 8 bars, use a data table instead")
                )
            biggest = 0.0
            for i, item in enumerate(items):
                ipath = "%s.items[%d]" % (path, i)
                if not isinstance(item, dict):
                    problems.append(Problem(ipath, "must be an object"))
                    continue
                _require(item, "label", ipath, problems, str, "a string")
                _require(item, "value", ipath, problems, str, "a string")
                pct = item.get("percent")
                if not isinstance(pct, (int, float)):
                    problems.append(Problem("%s.percent" % ipath, "must be a number 0-100"))
                elif not 0 <= pct <= 100:
                    problems.append(Problem("%s.percent" % ipath, "%s is outside 0-100" % pct))
                else:
                    biggest = max(biggest, float(pct))
            if items and biggest < 99.0:
                problems.append(
                    Problem("%s.items" % path,
                            "the largest bar is %.0f%%" % biggest,
                            "percent is share of the largest item, not of the total, so one bar should be 100")
                )

    if btype == "trend":
        points = block.get("points")
        if isinstance(points, list):
            if len(points) < 3:
                problems.append(
                    Problem("%s.points" % path, "has %d points" % len(points),
                            "under 3 points is not a trend; use a compare strip")
                )
            for i, pt in enumerate(points):
                ppath = "%s.points[%d]" % (path, i)
                if not isinstance(pt, dict):
                    problems.append(Problem(ppath, "must be an object"))
                    continue
                _require(pt, "label", ppath, problems, str, "a string")
                if not isinstance(pt.get("value"), (int, float)):
                    problems.append(Problem("%s.value" % ppath, "must be a number"))

    if btype == "statusGrid":
        items = block.get("items")
        if isinstance(items, list):
            for i, item in enumerate(items):
                ipath = "%s.items[%d]" % (path, i)
                if not isinstance(item, dict):
                    problems.append(Problem(ipath, "must be an object"))
                    continue
                _require(item, "label", ipath, problems, str, "a string")
                state = item.get("state")
                if state not in ("ok", "warn", "risk"):
                    problems.append(
                        Problem("%s.state" % ipath, '"%s" is not a state' % state,
                                "one of: ok, warn, risk")
                    )

    if btype == "prose":
        sections = block.get("sections")
        if isinstance(sections, list):
            for i, sec in enumerate(sections):
                spath = "%s.sections[%d]" % (path, i)
                if not isinstance(sec, dict):
                    problems.append(Problem(spath, "must be an object"))
                    continue
                if "body" not in sec and "list" not in sec:
                    problems.append(Problem(spath, 'needs "body" or "list"'))


def validate_page(page, index, problems):
    path = "pages[%d]" % index
    if not isinstance(page, dict):
        problems.append(Problem(path, "must be an object"))
        return

    palette = page.get("palette")
    if palette is not None and palette not in PALETTES:
        problems.append(
            Problem("%s.palette" % path, '"%s" is not a known palette' % palette,
                    "one of: %s" % ", ".join(sorted(PALETTES)))
        )

    blocks = _require(page, "blocks", path, problems, list, "an array")
    if blocks is None:
        return

    if len(blocks) == 0:
        problems.append(Problem("%s.blocks" % path, "is empty"))
    elif len(blocks) > 6:
        problems.append(
            Problem("%s.blocks" % path, "has %d components" % len(blocks),
                    "three to five reads best; over six looks like a dashboard")
        )

    emphasis = 0
    risk = 0
    for i, block in enumerate(blocks):
        validate_block(block, "%s.blocks[%d]" % (path, i), problems)
        if isinstance(block, dict):
            if block.get("emphasis"):
                emphasis += 1
            if block.get("type") == "riskCallout":
                risk += 1

    if emphasis > 1:
        problems.append(
            Problem("%s.blocks" % path, "%d emphasised components on one page" % emphasis,
                    "at most one; if everything is emphasised, nothing is")
        )
    if risk > 1:
        problems.append(
            Problem("%s.blocks" % path, "%d risk callouts on one page" % risk,
                    "at most one; split the content across two pages instead")
        )


def validate(doc):
    problems = []

    if not isinstance(doc, dict):
        return [Problem("", "the document must be a JSON object")]

    if "meta" not in doc:
        problems.append(Problem("", 'missing required property "meta"'))
    else:
        validate_meta(doc["meta"], problems)

    pages = doc.get("pages")
    if pages is None:
        problems.append(Problem("", 'missing required property "pages"'))
    elif not isinstance(pages, list):
        problems.append(Problem("pages", "must be an array"))
    elif not pages:
        problems.append(Problem("pages", "is empty"))
    else:
        for i, page in enumerate(pages):
            validate_page(page, i, problems)

        types = []
        for page in pages:
            if isinstance(page, dict):
                for b in page.get("blocks", []):
                    if isinstance(b, dict):
                        types.append(b.get("type"))
        if len(pages) >= 6 and "toc" not in types:
            problems.append(
                Problem("pages", "%d pages with no contents page" % len(pages),
                        "six pages or more should open with a printed contents page")
            )
        if "hero" not in types:
            problems.append(
                Problem("pages", "no hero statement anywhere in the report",
                        "the executive summary needs one sentence stating the finding")
            )

    return problems


def main():
    parser = argparse.ArgumentParser(
        description="Validate a report data document for the executive-report-design-system skill."
    )
    parser.add_argument("document", help="path to the report JSON")
    parser.add_argument(
        "--schema",
        default=None,
        help="path to report.schema.json (informational; validation is built in)",
    )
    parser.add_argument("--quiet", action="store_true", help="print nothing on success")
    args = parser.parse_args()

    if not os.path.isfile(args.document):
        sys.stdout.write("cannot read %s\n" % args.document)
        return 2

    try:
        with open(args.document, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
    except ValueError as exc:
        sys.stdout.write("%s is not valid JSON\n  %s\n" % (args.document, exc))
        return 2

    problems = validate(doc)

    if problems:
        sys.stdout.write("INVALID  %s\n\n" % args.document)
        for problem in problems:
            sys.stdout.write("%s\n\n" % problem)
        sys.stdout.write(
            "%d problem%s. Fix the JSON; do not render around a validation failure.\n"
            % (len(problems), "" if len(problems) == 1 else "s")
        )
        return 1

    if not args.quiet:
        pages = len(doc.get("pages", []))
        blocks = sum(len(p.get("blocks", [])) for p in doc.get("pages", []) if isinstance(p, dict))
        sys.stdout.write(
            "VALID    %s\n         %d page%s, %d component%s\n"
            % (args.document, pages, "" if pages == 1 else "s", blocks, "" if blocks == 1 else "s")
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
