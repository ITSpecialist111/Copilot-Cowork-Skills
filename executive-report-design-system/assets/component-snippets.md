# Component Snippets

*Copy-paste HTML for every component. Verbatim asset for
`executive-report-design-system` — take these exactly as they are and change only the
content. Do not add classes, do not add inline styles beyond the ones shown.*

The only inline styles permitted anywhere are `style="width:NN%"` on a `.bar-fill`, and
`style="animation-delay:NNms"` on a card. Everything else comes from the frozen CSS.

---

## The page shell

Every page. Three children, always in this order.

```html
<section class="page palette-warm-paper" id="p3">
  <div class="page-head">
    <span class="wordmark">Contoso</span>
    <span class="page-meta">Q3 Executive Summary &middot; Exec Team</span>
  </div>

  <div class="page-body stack gap-lg">
    <!-- three to five components -->
  </div>

  <div class="page-foot">
    <span>Contoso &middot; Q3 executive summary</span>
    <span>Page <span class="pageno"></span> of 9</span>
  </div>
</section>
```

Palette classes: `palette-warm-paper` (default) · `palette-clean-white` (dense data) ·
`palette-deep-ink` (covers, dividers) · `palette-slate` (operational, technical).

---

## Cover

```html
<div class="page-body cover">
  <div></div>
  <div>
    <p class="eyebrow">Quarterly business review</p>
    <h1 class="cover-title">Q3 performance<span class="accent">and the road into Q4.</span></h1>
    <div class="cover-rule"></div>
    <p class="lede" style="max-width:52ch">Closed revenue, pipeline carry and delivery health
      across eight active initiatives. Prepared for the executive team.</p>
  </div>
  <div class="cover-meta">
    <div><span class="kpi-label">Period</span><span style="font-size:13px">1 Jul – 30 Sep 2026</span></div>
    <div><span class="kpi-label">Prepared</span><span style="font-size:13px">6 October 2026</span></div>
    <div><span class="kpi-label">Owner</span><span style="font-size:13px">Revenue Operations</span></div>
    <div><span class="kpi-label">Classification</span><span style="font-size:13px">Internal</span></div>
  </div>
</div>
```

The empty first `<div>` is load-bearing: it pushes the title block to the optical
centre. Do not remove it.

---

## Contents

```html
<div class="toc">
  <div class="toc-item">
    <span class="toc-num">01</span>
    <span class="toc-label">Executive summary
      <span class="toc-sub">Closed revenue, pipeline carry and delivery health at a glance</span></span>
    <span class="toc-page">3</span>
  </div>
  <!-- repeat -->
</div>
```

---

## Section divider

Full-bleed part opener. Use `palette-deep-ink` on the page.

```html
<div class="page-body">
  <div class="divider">
    <p class="divider-num">Section 05</p>
    <h2 class="divider-title">How this report<br>is produced.</h2>
    <p class="divider-sub">The reporting architecture, the component catalogue and the
      design reference. Nothing in this section changes between quarters.</p>
  </div>
</div>
```

---

## Hero statement

The one sentence that states the finding. Two or three figures in `.accent`, no more.

```html
<p class="hero">Contoso closed <span class="accent">$1.9M</span> in Q3 and carries
  <span class="accent">$1.6M</span> into Q4, with delivery concentrated in
  <span class="accent">7/8 active initiatives</span>.</p>
```

---

## Two-tone display headline

```html
<h1 class="display">One design system.<span class="accent">Four kinds of reports.</span></h1>
<p class="lede" style="margin-top:8px;max-width:56ch">Standfirst paragraph.</p>
```

---

## Section head

```html
<div class="section-head">
  <p class="eyebrow">Performance</p>
  <h2 class="section-title">Closed revenue by month, and where it came from</h2>
  <p class="section-sub">Rolling six months to 30 September 2026</p>
</div>
```

---

## KPI row

Three or four cards. Never five. The value must be the real final figure — the motion
engine counts up to whatever is in the markup.

```html
<section class="kpi-row cols-4" aria-label="Key performance indicators">
  <article class="card">
    <div class="card-label">Q3 closed revenue</div>
    <div class="card-value">$1.9M</div>
    <div class="card-trend">10 deals closed</div>
  </article>

  <article class="card" style="animation-delay:80ms">
    <div class="card-label">Open pipeline</div>
    <div class="card-value">$1.6M</div>
    <div class="card-trend trend-down">$310K in final round</div>
  </article>
</section>
```

Inside a `.kpi-card` the same structure uses `.kpi-label` / `.kpi-value` /
`.kpi-note`; `.kpi-note.is-alert` turns the caption red. **Red is for risk only, never
for good news.**

With a change indicator:

```html
<article class="kpi-card">
  <span class="kpi-label">Win rate</span>
  <span class="kpi-value">31%</span>
  <span class="kpi-delta is-down"><span class="arrow">&#9660;</span> 4 points on Q2</span>
</article>
```

Health card with its own progress bar:

```html
<article class="kpi-card">
  <span class="kpi-label">Project health</span>
  <span class="kpi-value">4/8</span>
  <div class="progress-container">
    <div class="progress-label"><span>Projects on track</span><span>50%</span></div>
    <div class="progress-track" role="progressbar" aria-label="Projects on track"
         aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
      <div class="progress-bar" style="width:50%"></div>
    </div>
  </div>
</article>
```

---

## Bar list

Widths are **share of the largest item**, not of the total — so the top bar is always
100%.

```html
<div class="panel grow">
  <div class="panel-head">
    <h2 class="panel-title">Closed revenue by region</h2>
    <p class="panel-sub">Q3 won deals only</p>
  </div>
  <div class="bar-list">
    <div class="bar-item">
      <span class="bar-label">North America</span>
      <span class="bar-track"><span class="bar-fill" style="width:100%"></span></span>
      <span class="bar-value">$874K</span>
    </div>
    <div class="bar-item">
      <span class="bar-label">APAC</span>
      <span class="bar-track"><span class="bar-fill is-quiet" style="width:22%"></span></span>
      <span class="bar-value">$192K</span>
    </div>
  </div>
  <div class="legend">
    <span class="legend-item"><span class="legend-key"></span>Above quarter average</span>
    <span class="legend-item"><span class="legend-key is-quiet"></span>Below quarter average</span>
  </div>
  <p class="source-note">Source: CRM export, 30 September 2026.</p>
</div>
```

---

## Trend

Inline SVG. No charting library. The `viewBox` is `0 0 900 150`; plot inside
x 20–880, y 20–130, and put the labels at y 145.

```html
<div class="panel">
  <div class="panel-head">
    <h2 class="panel-title">Closed revenue by month</h2>
    <p class="panel-sub">Won deals, excluding renewals</p>
  </div>
  <svg class="trend" viewBox="0 0 900 150" preserveAspectRatio="none" role="img"
       aria-label="Closed revenue by month. January $412K, February $388K, March $801K.">
    <line class="grid" x1="0" y1="16"  x2="900" y2="16"></line>
    <line class="grid" x1="0" y1="56"  x2="900" y2="56"></line>
    <line class="grid" x1="0" y1="96"  x2="900" y2="96"></line>
    <path class="area" d="M20,104 L450,34 L880,40 L880,130 L20,130 Z"></path>
    <path class="line" d="M20,104 L450,34 L880,40"></path>
    <circle class="dot" cx="20"  cy="104" r="3.5"></circle>
    <circle class="dot" cx="450" cy="34"  r="3.5"></circle>
    <circle class="dot" cx="880" cy="40"  r="3.5"></circle>
    <line class="axis" x1="0" y1="130" x2="900" y2="130"></line>
    <text class="tick" x="20"  y="145" text-anchor="middle">Jan</text>
    <text class="tick" x="450" y="145" text-anchor="middle">Feb</text>
    <text class="tick" x="880" y="145" text-anchor="middle">Mar</text>
  </svg>
</div>
```

**The `aria-label` must list every data point.** A chart that cannot be read aloud is
invisible to a screen reader, and the linter warns if it is missing.

To plot: `y = 130 - (value / max) * 110`, `x = 20 + (i / (n - 1)) * 860`.

---

## Compare strip

```html
<div class="compare-strip cols-3">
  <div class="compare-col">
    <p class="compare-label">Q3 vs Q2</p>
    <p class="compare-value">+18.4%</p>
    <p class="compare-delta is-up">$1.9M against $1.6M</p>
  </div>
  <div class="compare-col">
    <p class="compare-label">Win rate</p>
    <p class="compare-value">31%</p>
    <p class="compare-delta is-down">Down 4 points on Q2</p>
  </div>
</div>
```

---

## Status grid

```html
<div class="panel">
  <div class="panel-head">
    <h2 class="panel-title">Initiative status</h2>
    <p class="panel-sub">As at 30 September 2026</p>
  </div>
  <div class="status-grid cols-2">
    <div class="status-item"><span class="dot ok"></span><span class="status-label">Cloud migration</span><span class="status-note">80%</span></div>
    <div class="status-item"><span class="dot warn"></span><span class="status-label">Partner portal</span><span class="status-note">At risk</span></div>
    <div class="status-item"><span class="dot risk"></span><span class="status-label">Contact centre</span><span class="status-note">Blocked</span></div>
  </div>
</div>
```

---

## Data table

`<thead>` repeats automatically if the table breaks across a page.

```html
<div class="panel grow">
  <div class="panel-head">
    <h2 class="panel-title">Largest closed deals</h2>
    <p class="panel-sub">Q3 2026</p>
  </div>
  <table class="data-table">
    <thead>
      <tr><th>Account</th><th>Region</th><th class="num">Value</th><th class="num">Closed</th></tr>
    </thead>
    <tbody>
      <tr><td>Northwind Traders</td><td>North America</td><td class="num">$412K</td><td class="num">18 Sep</td></tr>
    </tbody>
    <tfoot>
      <tr><td colspan="2">Top three</td><td class="num">$994K</td><td class="num">52% of Q3</td></tr>
    </tfoot>
  </table>
</div>
```

---

## Flow strip

Three to six steps. The trailing group can be emphasised — at most one per page.

```html
<div class="flow-strip">
  <div class="flow-step">
    <p class="flow-eyebrow">Start</p>
    <h3 class="flow-title">Beautiful HTML example</h3>
    <p class="flow-desc">Designer or found template — the visual target</p>
    <span class="badge badge-quiet">Once</span>
  </div>

  <div class="flow-group is-emphasis">
    <div class="flow-step">
      <p class="flow-eyebrow">Every time</p>
      <h3 class="flow-title">User sends prompt + data</h3>
      <p class="flow-desc">A two-line prompt and a CSV file — that&rsquo;s it</p>
      <span class="badge badge-live">Live demo</span>
    </div>
  </div>
</div>
<p class="caption" style="margin-top:6px">Explanatory note under the strip.</p>
```

---

## Numbered cards

Two to four parallel concepts.

```html
<div class="numbered-cards cols-3">
  <div class="num-card">
    <span class="num-badge">1</span>
    <h3 class="num-title">Style</h3>
    <p class="num-body">CSS custom properties define every visual decision.</p>
    <div class="inline-chips">
      <code class="chip">palette-warm-paper</code>
      <code class="chip">palette-deep-ink</code>
    </div>
    <p class="num-takeaway">Deterministic — same class, same output, always.</p>
  </div>

  <div class="num-card is-emphasis">
    <span class="num-badge">2</span>
    <h3 class="num-title">Components</h3>
    <p class="num-body">A catalogue of named blocks.</p>
    <p class="num-takeaway">AI-assembled — the skill picks the right blocks.</p>
  </div>
</div>
```

---

## Highlights

Usually the asks. Three cards.

```html
<div class="highlights cols-3">
  <div class="highlight-card">
    <h3 class="highlight-title">Escalate the contact centre contract</h3>
    <p class="highlight-body">Legal review has run eleven weeks. Every week of delay pushes
      $84K of recognised revenue into Q1.</p>
  </div>
</div>
```

---

## Risk callout

At most one per page.

```html
<div class="risk-callout">
  <span class="risk-mark">Read first</span>
  <div>
    <p class="risk-title">One decision cannot wait for the next review</p>
    <p class="risk-body">The contact centre contract has been in legal review for eleven
      weeks. Page 5 sets out the ask.</p>
  </div>
</div>
```

Amber variant: `<div class="risk-callout is-warn">` with `<span class="risk-mark">Caveat</span>`.

---

## Prose

Narrative body copy — method, assumptions, commentary. This is what stops pages 2..n
becoming a wall of cards.

```html
<div class="prose cols-2 grow">
  <h3>Revenue recognition</h3>
  <p><strong>Closed revenue</strong> is the total contract value of deals whose stage moved
    to <em>Closed Won</em> with a close date inside the quarter.</p>

  <h3>Known limitations</h3>
  <ul>
    <li>Figures are taken at 30 September and are not restated.</li>
    <li>Currency is reported as booked.</li>
  </ul>
</div>
```

---

## Pull quote

```html
<div class="pull-quote">
  <blockquote>The blocker is not engineering capacity. It is a single third-party contract
    that has been in legal review since April.</blockquote>
  <cite>Delivery review, 24 September</cite>
</div>
```

---

## Note strip and source note

```html
<p class="note-strip">Regional split is based on the billing entity on the closed contract,
  not the account&rsquo;s headquarters.</p>

<p class="source-note">Source: CRM export 30 September 2026. Prepared by Revenue Operations.</p>
```

---

## Layout utilities

| Class | Effect |
|---|---|
| `.stack` + `.gap-sm` / `.gap-md` / `.gap-lg` | Vertical flow with consistent spacing |
| `.cols-2` / `.cols-3` / `.cols-4` | Column count on any grid component |
| `.split` | Two equal columns |
| `.split-wide` | 1.6fr / 1fr — chart beside a narrow panel |
| `.grow` | Absorb slack. Put it on the last block so a page never ends in a void |

---

## Screen chrome

Screen only — hidden in print by the frozen CSS. Optional, but useful for a long report.

```html
<div class="toolbar">
  <strong>Q3 executive summary</strong>
  <nav>
    <a href="#p1">Cover</a>
    <a href="#p3">Executive summary</a>
  </nav>
  <button type="button" id="replay" style="margin-left:auto;background:#3A342F">Replay</button>
  <button type="button" onclick="window.print()" style="margin-left:8px">Print / Save as PDF</button>
</div>
```

The `id="replay"` is wired by the frozen motion engine. If you omit the button, nothing
breaks.
