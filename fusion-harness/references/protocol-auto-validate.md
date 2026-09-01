# Protocol: auto-validate

The acceptance gate is written **before** any work starts, by a persona that is forbidden from
doing the work. The gate is the definition of done. The builder builds against it, the gate runs,
and every failure line comes back to the builder verbatim as its next instructions. The loop
repeats until the gate passes or the round limit halts it.

Red before green. A gate written after the work is a description of the work, not a test of it.

Defaults: `max_rounds = 5`, `escalate_at = 3`. The user may override both.

Cost: unbounded until the gate passes or the limit halts. Say so before starting.

## Roles

| Role | Who | May write |
| --- | --- | --- |
| VALIDATOR | `rune` | The gate file only. Never the work. |
| BUILDER | `sol` | The work only. Never the gate. |

The separation is the whole mechanism. A persona that can edit both grades its own homework.

## Phase 1 — the VALIDATOR designs the gate

Read-only inspection first: what exists now, the conventions in use, how correctness is normally
established here. Ground every check in what is actually there.

Then write the gate to `gate.md` (or `gate.py`, see below) in the run folder.

Hard requirements:

- **Fidelity.** Enumerate every explicit requirement in the request and map each one to at least
  one check. Nothing asked for goes unchecked. Nothing that was not asked for is required. No
  weaker proxies, no narrowing of scope.
- **Objective.** Check contents, values, behaviour, exit codes — real observable outcomes. Never
  "looks good". Never mere existence when content or behaviour was asked for.
- **One line per check**, in exactly this form:
  - `PASS: <what was verified>`
  - `FAIL: expected <X>, found <Y>, at <exact location> — <exactly what to do to fix it>`
- **The FAIL line is the builder's next instruction.** Make it specific enough to act on with no
  further interpretation.
- **Verdict:** the gate passes only if every check passes.
- Deterministic, fast, non-interactive, and with no side effects on the work.

The VALIDATOR then replies with the gate path and a one-line summary of what it checks. It never
pastes the gate into chat, and it never touches anything else.

**Choosing the gate format.** If script execution is available in this session, write `gate.py`
so the verdict is mechanical and the exit code is real. If it is not, write `gate.md` as a
numbered list of assertions, each phrased so that it can only be answered by looking at the
actual artifact — a value to read, a string to find, a count to compare. An assertion that can be
satisfied by re-reading the request is not a check; rewrite it.

## Phase 2 — baseline

Run the gate against the current, unmodified state.

**The baseline must fail.** If it passes, one of two things is true and you must stop and say
which: the work was already done, or the gate does not actually test the request. Do not proceed
to build against a gate that passes on an empty room.

Record the baseline verdict.

## Phase 3 — the correction loop

Round 1: the BUILDER receives the request **and the full gate**.

> Execute the request directly and completely. An acceptance gate already exists and runs after
> you finish; it alone defines done. It is outside your control — you cannot edit it or its
> verdict. Satisfy it by genuinely completing the request, never by gaming individual checks.
> When done, report the exact items changed and what you ran.

Hold `WRITE TOKEN → sol` for the whole builder turn (C3).

Then run the gate. If it passes, go to the close-out.

Rounds 2+: the BUILDER receives **the gate output verbatim** — every FAIL line, unedited — plus
the round number and how many attempts remain. Do not summarise the failures; the exact wording
is the instruction.

## Phase 4 — escalation at `escalate_at`

On the third consecutive failure the VALIDATOR stops being a silent grader and diagnoses why the
builder is stuck. It reads the current state and the recent gate history read-only, then produces
a triage brief: what is actually wrong, what the builder has misread, and the specific next move.

The brief is advisory and goes to the builder alongside the gate output. **The gate output
remains the source of truth.**

**One-shot gate repair.** If triage concludes the *gate itself* is defective — checking something
that was never asked for, or unsatisfiable as written — the VALIDATOR may rewrite `gate.md` once
per run. When it does:

1. Say explicitly that the gate was repaired and what was wrong with it.
2. Re-run the repaired gate immediately against the current state.
3. Give the builder the repaired gate in full, marked as replacing the stale copy from round 1.
   A builder reasoning against checks that no longer exist will fail forever.

Repair is available once. A gate that needs repairing twice means the request was never
well-defined; stop and say so.

## Phase 5 — close-out

**Passed:** report the round count, and the gate's own PASS lines as the evidence. "The gate
passed" means the gate was run and returned no failures (C9). Nothing else earns that sentence.

**Halted at `max_rounds`:** report it as a failure, not a partial success. Include the last gate
output verbatim, what was actually completed, what was not, and the single most likely cause.
Leave the work in a coherent state and say exactly what state that is.

## Output

1. Verdict: `PASSED in <n> rounds` or `HALTED after <n> rounds`.
2. The final gate output, verbatim.
3. **What changed** — every item, with paths.
4. **Round history** — one line per round: what was attempted, how many checks failed.
5. **Gate repaired** — yes/no, and what was wrong with it.
