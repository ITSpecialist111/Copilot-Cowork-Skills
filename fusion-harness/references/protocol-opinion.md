# Protocol: opinion

Every persona answers the same request independently. Nothing is merged and nobody wins. The
output is the spread of answers, because the spread is the information.

Cost: one persona turn per slot. Default 3.

## Procedure

1. **Gather the evidence once.** Read what the request points at and list what you read. Every
   persona works from this same base (C1).
2. **For each slot, in roster order:**
   - Load the charter from `references/roster.md` verbatim.
   - Answer the request as that persona, using the output contract below.
   - Write the complete answer to `agents/<slot>.md` in the run folder.
   - Do not look at, or think forward to, any other persona's answer.
3. **Compare, do not merge.** Produce the comparison block. It reports positions; it does not
   pick one unless the user asked for a recommendation.
4. **Apply the divergence floor (C7).** If the personas agree on everything, say so and label
   the consensus unearned.

## Persona output contract

Each persona produces, under 1,200 words:

1. **Position** — one sentence, decisive. No hedging, no "it depends" without saying on what.
2. **Case** — the strongest 3–5 arguments, each with its evidence and a locator.
3. **What would change my mind** — the specific observation that would move this position.
4. **Cost of being wrong** — what it costs if this position is followed and turns out wrong.

A persona that cannot answer on the available evidence writes `FAILED: <reason>` and says what
evidence it needed. It does not guess.

## Comparison block

Close with:

| | `rune` | `sol` | `nova` |
| --- | --- | --- | --- |
| Position | | | |
| Agrees with | | | |
| Splits from | | | |

Then:

- **Consensus** — what all personas held, and whether it was earned (C7).
- **Divergence** — the real splits, and the observation that would settle each one.
- **Minority worth keeping** — the position that did not win but should not be discarded.
- **If you want one answer** — only if the user asked. Name it, name the runner-up, and give the
  one condition under which the runner-up is right instead.

## Read-only

This protocol writes nothing except its own artifacts (C2). If the request implies action —
"and send it", "and update the doc" — produce the opinions, then ask whether to switch to
`fusion`, which has a write phase. Do not act on the back of an opinion round.
