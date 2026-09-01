# Protocol: fusion

N personas research the request independently and read-only. One fresh, neutral FUSION persona
then merges their work into a single canonical result and — when the request asks for something
to be built, written or changed — **is the only persona allowed to do it**. Afterwards every
source persona reviews the fused result and either accepts it or objects.

Cost: one turn per source, plus one merge turn, plus one dissent-check turn per source.
Default 3 + 1 + 3 = 7.

Use this when the user wants one answer or one artefact, informed by every angle. Use `opinion`
when they want to see the angles themselves.

## Phase 1 — sources (read-only)

For each slot in roster order, independently (C1):

> You are one research worker in a fusion harness. Every persona is analysing this same request
> independently. A separate FUSION persona will combine the successful results and is the only
> one permitted to change anything.
>
> Strictly read-only (C2): inspect, do not modify, do not send, do not claim implementation.
> Produce decisive, implementation-ready guidance: the exact files or items, the constraints, the
> concrete steps or draft content, the validation, the risks, and the evidence for each.

Write each to `agents/<slot>.md`. Then write `source-manifest.md`: one row per source with slot,
status, artifact path, and a one-line summary.

**Quorum (C6):** fewer than 2 successful sources means the merge does not run. Stop, report what
was gathered, and say plainly that a fusion of one source is a single answer wearing a costume.

## Phase 2 — the merge (sole writer)

Announce `WRITE TOKEN → FUSION` before anything changes (C3).

The FUSION persona is a *fresh* perspective, not one of the roster. It has not argued for any of
the source positions and must not inherit their loyalties.

> You are the FUSION persona. `<n>` personas independently analysed the request; their complete
> outputs are in the run folder and summarised in the manifest.
>
> You are the only process permitted to change anything in this run. First critically merge the
> sources. Then, if the request asks for something to be built, written, created or sent, do it —
> as the sole writer — and report what actually changed. Never merely recommend that someone else
> do the work.

Merge rules:

- Resolve consensus **and** divergence with `[SLOT]` attribution (C8).
- Preserve valuable minority observations. Reject weak claims explicitly, and say why.
- Where sources conflict on a fact, go back to the evidence and resolve it. Do not average.
- Where sources conflict on a judgement, state both, choose one, and give the condition under
  which the other is right.
- Disclose failed or missing sources.

Write the merged result to `fused.md`. If deliverables were produced, list every one with its
path. Sensitive actions still require the user's approval — the write token is not consent.

## Phase 3 — dissent check

The original harness required each source model to acknowledge the fused bytes, proving the
result had actually propagated. Here there is one context, so a receipt proves nothing. The
useful half of that step is the review, so run that instead.

Show each source persona the final fused result. Each replies with **one** of:

- `ACK <run-id>` — the fused result represents my contribution fairly and I have no objection; or
- `OBJECT <run-id>` — followed by the specific location and the specific misuse: a claim
  attributed to me that I did not make, a load-bearing point dropped, or a conclusion my evidence
  does not support.

An objection is not overruled silently. Either correct `fused.md` and re-run that persona's
check, or record the objection verbatim in the output under **Unresolved objections**.

Write the results to `acks.md`.

## Output

1. The fused answer, or the description of what was built, first.
2. **What changed** — every file, message or item, with its path. Or `nothing — analysis only`.
3. **Consensus & Divergence** — with `[SLOT]` attribution.
4. **Rejected claims** — what was dropped and why.
5. **Unresolved objections** — from phase 3, or `none`.
6. **Sources** — including any that failed.
