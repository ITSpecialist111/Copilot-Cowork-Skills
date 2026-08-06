# Component Catalogue

*On-demand reference for `executive-report-design-system`. The complete class inventory.
Nothing outside this list exists. If a class is not here, it is not in the design system
and must not appear in a generated report.*

Copy-paste markup for each of these is in `assets/component-snippets.md`.

---

## The decision table

Match the shape of the data. Do not deliberate.

| The data is… | Component |
|---|---|
| One number that matters most | `.hero` sentence, figure in `.accent` |
| Three or four headline metrics | `.kpi-row` |
| A metric plus its change | `.kpi-card` with `.kpi-delta` |
| Ranked categories, 3–6 of them | `.bar-list` plus `.legend` |
| A time series, 4+ points | `.trend` inside a `.panel` |
| This period against last | `.compare-strip` |
| Named items with a state | `.status-grid` |
| Rows the reader will interrogate | `.data-table` inside a `.panel` |
| A sequence of steps | `.flow-strip` |
| Parallel concepts, 2–4 | `.numbered-cards` |
| Things needing a decision | `.highlights` |
| One urgent thing | `.risk-callout` |
| Explanation, caveats, method | `.prose.cols-2` |
| A memorable quotation | `.pull-quote` |
| A qualifier at the foot of a page | `.note-strip` |
| Where the numbers came from | `.source-note` |

---

## Page furniture

| Class | Element | Notes |
|---|---|---|
| `.page` | `<section>` | One physical A4 landscape sheet. Always carries a palette class |
| `.page-head` | `<div>` | Running head. Real element, repeated per page |
| `.wordmark` | `<span>` | Organisation name, top left |
| `.page-meta` | `<span>` | Uppercase letterspaced meta, top right |
| `.page-body` | `<div>` | Content area. Usually `stack gap-lg` |
| `.page-foot` | `<div>` | Running foot |
| `.pageno` | `<span>` | Empty. CSS counter fills it |

## Palettes

| Class | Use |
|---|---|
| `palette-warm-paper` | Default. Warm printed-report feel |
| `palette-clean-white` | Dense, data-heavy pages |
| `palette-deep-ink` | Covers and section dividers |
| `palette-slate` | Operational and technical reports |

## Type

| Class | Size / weight | Use |
|---|---|---|
| `.display` | 40px / 300 | Two-tone page headline. Second line in `<span class="accent">` |
| `.hero` | 38px / 300 | The one-sentence finding |
| `.cover-title` | 52px / 300 | Cover only |
| `.divider-title` | 46px / 300 | Section divider only |
| `.lede` | 12.5px | Standfirst under a headline |
| `.eyebrow` | 8.5px uppercase | Tiny label above a title |
| `.section-title` | 14px / 600 | Section heading |
| `.section-sub` | 11px | Under a section title |
| `.section-head` | — | Wrapper for eyebrow + title + sub |
| `.caption` | 10px italic | Note under a block |
| `.accent` | — | The red. Figures that matter, nothing decorative |

## Surfaces

| Class | Use |
|---|---|
| `.panel` | The white card that wraps a chart or table |
| `.panel-head` / `.panel-title` / `.panel-sub` | Panel heading group |

## KPI row

| Class | Use |
|---|---|
| `.kpi-row` | Grid. Add `.cols-3` or `.cols-4` |
| `.kpi-card` | One metric |
| `.kpi-label` | Uppercase label |
| `.kpi-value` | The figure. **Animated** — write the real final value |
| `.kpi-note` | Caption. `.is-alert` turns it red (risk only) |
| `.kpi-delta` | Change indicator. `.is-up` green, `.is-down` red |
| `.card` / `.card-label` / `.card-value` / `.card-trend` | Alternative naming, same visual result. `.trend-up` / `.trend-down` colour the caption |

## Progress

| Class | Use |
|---|---|
| `.progress-container` | Wrapper |
| `.progress-label` | Label row, two spans |
| `.progress-track` | The groove. Needs `role="progressbar"` and aria values |
| `.progress-bar` | The fill. Width authored inline |

## Bar list

| Class | Use |
|---|---|
| `.bar-list` / `.bar-item` | Container and row |
| `.bar-label` / `.bar-value` | Name and figure |
| `.bar-track` / `.bar-fill` | Groove and fill. `.is-quiet` for below-average |
| `.legend` / `.legend-item` / `.legend-key` | Required when more than one bar style is used |

**Widths are share of the largest item, not of the total.** The top bar is always 100%.

## Trend (inline SVG)

| Class | Element |
|---|---|
| `.trend` | `<svg>`, `viewBox="0 0 900 150"` |
| `.grid` / `.axis` | Guide lines |
| `.area` / `.line` / `.dot` | Fill, stroke, points |
| `.tick` | Axis labels |

The `<svg>` needs `role="img"` and an `aria-label` naming every data point.

## Compare strip

`.compare-strip` · `.compare-col` · `.compare-label` · `.compare-value` ·
`.compare-delta` (`.is-up` / `.is-down`)

## Status grid

`.status-grid` · `.status-item` · `.dot` (`.ok` / `.warn` / `.risk`) ·
`.status-label` · `.status-note`

## Data table

`.data-table` · `.num` on numeric cells. `<thead>` repeats automatically across a page
break; rows do not split.

## Flow strip

`.flow-strip` · `.flow-step` · `.flow-group.is-emphasis` · `.flow-eyebrow` ·
`.flow-title` · `.flow-desc` · `.badge` (`.badge-quiet` / `.badge-live`)

## Numbered cards

`.numbered-cards` · `.num-card` (`.is-emphasis`) · `.num-badge` · `.num-title` ·
`.num-body` · `.num-takeaway` · `.chip` · `.inline-chips`

## Highlights

`.highlights` · `.highlight-card` · `.highlight-title` · `.highlight-body`

## Narrative

| Class | Use |
|---|---|
| `.prose` / `.prose.cols-2` | Body copy. Supports `h3`, `p`, `ul`, `li`, `strong`, `em` |
| `.risk-callout` (`.is-warn`) · `.risk-mark` · `.risk-title` · `.risk-body` | One urgent thing |
| `.pull-quote` + `<blockquote>` + `<cite>` | A verbatim line |
| `.note-strip` | Footnote-weight qualifier |
| `.source-note` | Provenance line |

## Structural

| Class | Use |
|---|---|
| `.cover` · `.cover-title` · `.cover-rule` · `.cover-meta` | Page 1 |
| `.toc` · `.toc-item` · `.toc-num` · `.toc-label` · `.toc-sub` · `.toc-page` | Printed contents |
| `.divider` · `.divider-num` · `.divider-title` · `.divider-sub` | Part opener |

## Layout utilities

| Class | Effect |
|---|---|
| `.stack` | Vertical flex |
| `.gap-sm` / `.gap-md` / `.gap-lg` | 10px / 15px / 18px |
| `.cols-2` / `.cols-3` / `.cols-4` | Column count on any grid |
| `.split` | Two equal columns |
| `.split-wide` | 1.6fr / 1fr |
| `.grow` | Absorb slack. Put on the last block of a page |
| `.visually-hidden` | Screen-reader-only text |

## Screen chrome

`.toolbar` · `.icon-btn`. Hidden in print. Never part of the printed report.

## Motion (applied by the engine — do not author these)

`.rise` · `.is-in` · `.is-counting` · `.js-motion`. The engine adds them. You never
write them.

---

## Composition rules

1. **Three to five components per page.** Two looks thin, seven looks like a dashboard.
2. **At most one `.is-emphasis` and one `.risk-callout` per page.** Emphasis works by
   contrast; more than one destroys it.
3. **`.grow` on the last block** so a page never ends in a void.
4. **Content must fit.** If a page overflows, move a block to the next page. Never
   reduce the type size.
5. **A chart with more than one style needs a legend.** It will be printed in mono
   sooner or later.
6. **Red only where it means something.** Figures in the hero, risk captions, the
   emphasis group, numbered badges. Nowhere else.
