"""
Contract Clause Segmentation Script — Helper for the legal-redliner skill.

Parses a plain-text contract (extracted from PDF or Word) and segments it into
individually addressable clauses with IDs, headings, and classification metadata.

Usage:
    python scripts/segment_contract.py <contract_text_file> [--output <output.json>]

Input:
    Plain text file containing the contract body (extracted via pdf or docx skill).

Output:
    JSON with structured clause data for the redlining pipeline:
    {
        "metadata": {
            "source_file": "contract.txt",
            "total_clauses": 42,
            "total_words": 8500,
            "segmentation_confidence": "high"
        },
        "clauses": [
            {
                "id": "CL-001",
                "section": "1",
                "heading": "Definitions",
                "text": "...",
                "word_count": 350,
                "has_definitions": true,
                "has_obligations": false,
                "has_liability_language": false,
                "has_termination_language": false,
                "has_data_processing_language": false,
                "has_ip_language": false,
                "defined_terms_used": ["Confidential Information", "Disclosing Party"],
                "cross_references": ["Clause 5.2", "Schedule 1"]
            }
        ]
    }
"""

import json
import re
import sys
from pathlib import Path


# ── Clause detection patterns ───────────────────────────────────────────────

# Common section/clause heading patterns in legal documents
HEADING_PATTERNS = [
    # Numbered sections: "1.", "1.1", "1.1.1", "2.3.4"
    re.compile(
        r'^(\d+(?:\.\d+)*)\.\s+([A-Z][^\n]{2,80})$',
        re.MULTILINE
    ),
    # Numbered with parentheses: "(a)", "(i)", "(1)"
    re.compile(
        r'^\(([a-z]|[ivxlc]+|\d+)\)\s+([A-Z][^\n]{2,80})$',
        re.MULTILINE
    ),
    # UPPERCASE headings (common in contracts)
    re.compile(
        r'^(\d+(?:\.\d+)*)\.\s+([A-Z][A-Z\s&,]{3,80})$',
        re.MULTILINE
    ),
    # "Article N" or "Section N" or "Clause N"
    re.compile(
        r'^(?:Article|Section|Clause|Schedule|Annex|Appendix|Exhibit)\s+(\d+|[A-Z])[.:]\s*([^\n]{2,80})$',
        re.MULTILINE | re.IGNORECASE
    ),
]

# ── Language detection patterns ─────────────────────────────────────────────

DEFINITION_MARKERS = [
    r'"[A-Z][^"]{2,50}"\s+(?:means|shall mean|refers to|has the meaning)',
    r'[A-Z][a-zA-Z\s]{2,40}\s+means\b',
    r'\bAs used (?:herein|in this Agreement)\b',
    r'\bFor (?:the )?purposes? of this\b',
]

OBLIGATION_MARKERS = [
    r'\bshall\b', r'\bmust\b', r'\bwill\b(?!\s+not)',
    r'\bobligation\b', r'\brequired to\b',
    r'\bcovenants?\b', r'\bundertakes?\b',
    r'\bagrees? to\b',
]

LIABILITY_MARKERS = [
    r'\bliab(?:le|ility)\b', r'\bindemnif(?:y|ies|ication)\b',
    r'\bdamages?\b', r'\bloss(?:es)?\b',
    r'\bhold harmless\b', r'\bexclusion\b',
    r'\blimitation of liability\b', r'\bcap\b.*\bliability\b',
    r'\bconsequential\b', r'\bindirect\b.*\bdamages?\b',
]

TERMINATION_MARKERS = [
    r'\bterminat(?:e|ion|ing)\b', r'\bexpir(?:e|y|ation)\b',
    r'\bcancel(?:lation)?\b', r'\bnotice period\b',
    r'\brenew(?:al)?\b', r'\bauto[- ]?renew\b',
    r'\bcure period\b', r'\bfor (?:cause|convenience)\b',
]

DATA_PROCESSING_MARKERS = [
    r'\bpersonal data\b', r'\bdata subject\b',
    r'\bdata process(?:ing|or|er)\b', r'\bcontroller\b',
    r'\bGDPR\b', r'\bsub[- ]?processor\b',
    r'\bdata breach\b', r'\bdata protection\b',
    r'\bprivacy\b', r'\btransfer\b.*\bdata\b',
]

IP_MARKERS = [
    r'\bintellectual property\b', r'\bIP\b',
    r'\bcopyright\b', r'\btrademark\b',
    r'\bpatent\b', r'\blicen[cs]e\b',
    r'\bwork product\b', r'\bownership\b',
    r'\bassignment\b.*\brights\b',
]

# ── Defined term extraction ─────────────────────────────────────────────────

DEFINED_TERM_PATTERN = re.compile(
    r'"([A-Z][^"]{2,50})"'
)

# ── Cross-reference extraction ──────────────────────────────────────────────

CROSS_REF_PATTERN = re.compile(
    r'(?:(?:Clause|Section|Article|paragraph|Schedule|Annex|Appendix|Exhibit)\s+'
    r'(?:\d+(?:\.\d+)*|[A-Z]))',
    re.IGNORECASE
)


def detect_headings(text: str) -> list[dict]:
    """Find all clause/section headings with their positions."""
    headings = []
    seen_positions = set()

    for pattern in HEADING_PATTERNS:
        for match in pattern.finditer(text):
            pos = match.start()
            # Avoid duplicate detections at the same position
            if pos not in seen_positions:
                seen_positions.add(pos)
                headings.append({
                    "position": pos,
                    "number": match.group(1).strip(),
                    "heading": match.group(2).strip() if match.lastindex >= 2 else "",
                    "raw": match.group(0).strip(),
                })

    # Sort by position in document
    headings.sort(key=lambda h: h["position"])
    return headings


def has_pattern(text: str, markers: list[str]) -> bool:
    """Check if text contains any of the given regex patterns."""
    text_lower = text.lower()
    for marker in markers:
        if re.search(marker, text_lower):
            return True
    return False


def extract_defined_terms(text: str) -> list[str]:
    """Extract capitalised defined terms in quotes."""
    terms = DEFINED_TERM_PATTERN.findall(text)
    return sorted(set(terms))


def extract_cross_references(text: str) -> list[str]:
    """Extract cross-references to other clauses/sections."""
    refs = CROSS_REF_PATTERN.findall(text)
    return sorted(set(refs))


def segment(text: str) -> dict:
    """Segment contract text into structured clauses."""
    headings = detect_headings(text)

    if not headings:
        # Fallback: treat the entire document as a single clause
        return {
            "metadata": {
                "total_clauses": 1,
                "total_words": len(text.split()),
                "segmentation_confidence": "low",
                "note": "No clause headings detected — treating entire document as one block. Manual segmentation recommended.",
            },
            "clauses": [{
                "id": "CL-001",
                "section": "1",
                "heading": "(Entire Document)",
                "text": text.strip(),
                "word_count": len(text.split()),
                "has_definitions": has_pattern(text, DEFINITION_MARKERS),
                "has_obligations": has_pattern(text, OBLIGATION_MARKERS),
                "has_liability_language": has_pattern(text, LIABILITY_MARKERS),
                "has_termination_language": has_pattern(text, TERMINATION_MARKERS),
                "has_data_processing_language": has_pattern(text, DATA_PROCESSING_MARKERS),
                "has_ip_language": has_pattern(text, IP_MARKERS),
                "defined_terms_used": extract_defined_terms(text),
                "cross_references": extract_cross_references(text),
            }],
        }

    clauses = []
    for i, heading in enumerate(headings):
        # Extract text between this heading and the next
        start = heading["position"]
        end = headings[i + 1]["position"] if i + 1 < len(headings) else len(text)
        clause_text = text[start:end].strip()

        clause_id = f"CL-{i + 1:03d}"
        word_count = len(clause_text.split())

        clauses.append({
            "id": clause_id,
            "section": heading["number"],
            "heading": heading["heading"],
            "text": clause_text,
            "word_count": word_count,
            "has_definitions": has_pattern(clause_text, DEFINITION_MARKERS),
            "has_obligations": has_pattern(clause_text, OBLIGATION_MARKERS),
            "has_liability_language": has_pattern(clause_text, LIABILITY_MARKERS),
            "has_termination_language": has_pattern(clause_text, TERMINATION_MARKERS),
            "has_data_processing_language": has_pattern(clause_text, DATA_PROCESSING_MARKERS),
            "has_ip_language": has_pattern(clause_text, IP_MARKERS),
            "defined_terms_used": extract_defined_terms(clause_text),
            "cross_references": extract_cross_references(clause_text),
        })

    # Determine confidence based on heading detection quality
    avg_words = sum(c["word_count"] for c in clauses) / len(clauses) if clauses else 0
    if len(clauses) >= 5 and avg_words > 20:
        confidence = "high"
    elif len(clauses) >= 3:
        confidence = "medium"
    else:
        confidence = "low"

    # Check for preamble text before first heading
    preamble_text = text[:headings[0]["position"]].strip()
    if preamble_text and len(preamble_text.split()) > 20:
        preamble_clause = {
            "id": "CL-000",
            "section": "0",
            "heading": "(Preamble / Recitals)",
            "text": preamble_text,
            "word_count": len(preamble_text.split()),
            "has_definitions": has_pattern(preamble_text, DEFINITION_MARKERS),
            "has_obligations": has_pattern(preamble_text, OBLIGATION_MARKERS),
            "has_liability_language": False,
            "has_termination_language": False,
            "has_data_processing_language": has_pattern(preamble_text, DATA_PROCESSING_MARKERS),
            "has_ip_language": False,
            "defined_terms_used": extract_defined_terms(preamble_text),
            "cross_references": extract_cross_references(preamble_text),
        }
        clauses.insert(0, preamble_clause)

    total_words = sum(c["word_count"] for c in clauses)

    return {
        "metadata": {
            "total_clauses": len(clauses),
            "total_words": total_words,
            "segmentation_confidence": confidence,
        },
        "clauses": clauses,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python segment_contract.py <contract_text_file> [--output <output.json>]")
        print()
        print("Segments a contract into individually addressable clauses for redlining.")
        print()
        print("Input:  Plain text file (extracted from PDF or Word via the pdf/docx skill)")
        print("Output: JSON with clause IDs, headings, text, and classification flags")
        print()
        print("Classification flags per clause:")
        print("  - has_definitions          Clause contains defined terms")
        print("  - has_obligations          Clause contains obligation language (shall, must)")
        print("  - has_liability_language   Clause relates to liability/indemnification")
        print("  - has_termination_language Clause relates to termination/renewal")
        print("  - has_data_processing_language  Clause relates to data protection/GDPR")
        print("  - has_ip_language          Clause relates to intellectual property")
        sys.exit(1)

    input_file = sys.argv[1]

    # Parse optional output flag
    output_file = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    # Read input
    text = Path(input_file).read_text(encoding="utf-8")

    # Segment
    result = segment(text)
    result["metadata"]["source_file"] = input_file

    # Output
    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        Path(output_file).write_text(output_json, encoding="utf-8")
        print(f"Segmentation complete: {result['metadata']['total_clauses']} clauses written to {output_file}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
