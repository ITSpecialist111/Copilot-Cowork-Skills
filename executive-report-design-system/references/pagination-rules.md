# Pagination Rules

*On-demand reference for `executive-report-design-system`. Read this before changing
anything about how the report prints. Print CSS is full of folklore; most of what is
widely believed does not work in the browser your reader will actually use.*

---

## The approach that works

One `<section class="page">` per physical sheet, sized in millimetres, containing its
own header and footer as real elements.

```css
@page { size: A4 landscape; margin: 0; }

.page {
  width: 297mm;
  height: 210mm;
  padding: 13mm 17mm;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

@media print {
  .page {
    height: 209.5mm;              /* see "the blank page" below */
    break-after: page;
    page-break-after: always;
  }
  .page:last-of-type {
    break-after: auto;
    page-break-after: auto;
  }
}
```

That is the whole page model. It is deliberately dull, because dull survives four print
engines.

---

## What does not work, and why

### `@page` margin boxes

```css
/* DOES NOT WORK IN CHROMIUM OR WEBKIT */
@page {
  @bottom-center { content: "Page " counter(page) " of " counter(pages); }
}
```

This is the *correct* CSS. It is in the specification, it is what paged-media engines
like Prince and WeasyPrint implement, and it is what most blog posts recommend.

It is **not implemented in Chromium or WebKit**, and shows no sign of being. Firefox
supports it. So if your reader prints from Edge or Chrome — which they will — they get
no header, no footer and no page number.

**Use in-DOM `.page-head` and `.page-foot` elements instead**, repeated in the markup on
every page. Yes, that means the header text appears nine times in the file. That is the
cost of it working everywhere.

### `position: fixed` for running headers

Widely recommended, and it does work — in Firefox, where a fixed element repeats on
every printed page as the specification requires.

In **Chromium and WebKit a fixed element prints once**, on the first page, or is clipped
entirely. So a "running header" built this way silently vanishes from pages 2 onward in
the most common browser.

Same fix: put the header in the markup, on every page.

### `counter(pages)` for the total

There is no CSS counter that gives you the total number of your own elements. `counter(pages)`
only exists inside `@page` margin boxes, which brings you back to the first problem.

**Write the total in as a literal.** The generator knows how many pages it produced:

```html
<span>Page <span class="pageno"></span> of 9</span>
```

The *current* number comes from a CSS counter and works everywhere:

```css
body  { counter-reset: pageno; }
.page { counter-increment: pageno; }
.pageno::after { content: counter(pageno); }
```

### `height: 100vh` for a page

`vh` is the viewport. In print there is no viewport in the sense you want, and on screen
it makes a "page" whatever height the browser window happens to be. Use millimetres.

---

## The blank trailing page

The single most common defect in printed HTML. Two causes:

**1. `break-after: page` on the last page.** The rule fires, the engine dutifully starts
a new sheet, and the sheet is empty. Fix:

```css
.page:last-of-type { break-after: auto; page-break-after: auto; }
```

Use `:last-of-type`, not `:last-child` — there is usually a script or a stray node after
the final section, which makes `:last-child` silently fail to match.

**2. A page exactly the height of the sheet.** Sub-pixel rounding pushes one line over
the boundary and produces a ghost page. Leave a sliver of slack:

```css
@media print { .page { height: 209.5mm; } }
```

Half a millimetre is invisible and removes the entire class of problem.

---

## Backgrounds disappear in print

By default, browsers strip background colours and images when printing, to save ink. For
a design built on warm paper and tinted emphasis groups, that removes the entire visual
identity — you get black text on white and none of the structure.

```css
@media print {
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
```

Both properties, because the unprefixed one is still not universal. This is mandatory
for this design system, not optional polish.

Note the reader can still override it in the print dialog ("Background graphics" off).
Nothing can be done about that; the report is still legible, just plain.

---

## Keeping a component intact

```css
.panel, .kpi-card, .num-card, .flow-step, .highlight-card, .pull-quote {
  break-inside: avoid;
  page-break-inside: avoid;
}
```

Both properties, for the same reason as above.

**The limit:** `break-inside: avoid` is ignored when the element is taller than the page.
A twelve-row table cannot be rescued by it. For tables, let them break by row and repeat
the header instead:

```css
.data-table thead { display: table-header-group; }
.data-table tr    { break-inside: avoid; }
```

`display: table-header-group` is what makes `<thead>` repeat at the top of each page a
long table spans. It is well supported and quietly one of the most useful print
declarations there is.

---

## Screen chrome must not print

The toolbar, the nav strip, the replay button — none of it belongs on paper.

```css
@media print { .toolbar { display: none !important; } }
```

---

## Animation and print

If a report animates figures counting up, printing while the count is in flight puts a
half-counted number on paper. Belt and braces:

```css
@media print {
  .js-motion .rise { opacity: 1 !important; transform: none !important; }
  .js-motion .bar-fill { width: var(--target) !important; transition: none !important; }
  .js-motion .trend .line { stroke-dashoffset: 0 !important; }
}
```

```js
window.addEventListener('beforeprint', function () { revealAll(); settleAll(); });
```

The CSS alone is not enough, because the script may have written an intermediate value
into `textContent`. The `beforeprint` handler is what restores the true figure. The CSS
covers the case where `beforeprint` does not fire (some Safari versions).

---

## Verifying it actually works

Do not trust `element.scrollHeight` to detect overflow. If the page has
`overflow: hidden` — and it must, or a stray line breaks the layout — `scrollHeight`
reports the clipped height and everything looks fine while content is silently cut off.

Measure geometry against the running foot instead:

```js
const foot = page.querySelector('.page-foot').getBoundingClientRect();
const spill = Math.max(...[...page.querySelectorAll('.page-body *')]
  .filter(el => el.getClientRects().length)
  .map(el => el.getBoundingClientRect().bottom - foot.top));
// spill > 0 means content is running into or past the footer
```

Then actually print to PDF from **both** a Chromium browser and Firefox, and count the
sheets. Nine pages in the document must produce nine sheets in the PDF.
