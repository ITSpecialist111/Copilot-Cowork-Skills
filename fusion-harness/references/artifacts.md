# Artifacts

Every run writes an inspectable folder. The artifacts are what make a run checkable after the
fact: they show who said what, in what order, and what was actually changed. They are also the
mechanism that enforces independence — a persona's answer is fixed the moment it is written
(C1), so writing it is not bookkeeping, it is the contract.

**This is mandatory and is not a judgement call.** Every file listed below is required, not a menu.
Write the artifacts even when the request looks conversational, even when the answer is short, even
when files feel like clutter. The only two permitted reasons to skip are that the environment
refuses to create files, or that the user said so in this request, in words. Deciding on the user's
behalf that they did not want files is a protocol failure, not an adaptation — disclosing it
afterwards does not make it compliant.

Files created during a session appear in the **Output folder** in the side panel and in the
user's OneDrive `Cowork` folder.

## Run folder

```
fusion-harness/<yyyymmdd-hhmm>-<protocol>/
├── prompt.md              the request, verbatim, plus any protocol options
├── roster.md              the slots actually used, with roles
├── evidence.md            what was read to establish the shared base
├── summary.md             the ledger — always written, even on a failed run
└── (protocol-specific, below)
```

Per protocol:

```
opinion/         agents/<slot>.md
debate/          debate/round-<n>/<slot>.md
fusion/          agents/<slot>.md · source-manifest.md · fused.md · acks.md
collaborate/     collaborate/proposals/<slot>.md · collaborate/plan.json
                 collaborate/reports/<task-id>.md
auto-validate/   gate.md (or gate.py) · gate-baseline.txt · gate-round-<n>.txt
                 builder-round-<n>.md · triage-round-<n>.md
```

If the environment will not let you create files, do not abandon the run and do not silently skip
the artifacts. Keep each persona's output complete and immutable in the transcript instead, and
state once that artifacts could not be written. A paid-for answer is never discarded because a
file could not be saved.

## `summary.md`

Always written, including when the run fails or halts.

```markdown
# Fusion harness run <run-id>

- Protocol: opinion | debate | fusion | collaborate | auto-validate
- Request: <one line>
- Roster: rune (ARCHITECT), sol (BUILDER, primary), nova (BUILDER)
- Persona turns: <n>
- Outcome: complete | halted | failed
- Write token held by: <slot, or "none — read-only run">

## Per persona

| Slot | Role | Status | Artifact |
| --- | --- | --- | --- |
| rune | ARCHITECT | ok | agents/rune.md |
| sol | BUILDER | ok | agents/sol.md |
| nova | BUILDER | failed: <reason> | — |

## What changed
<every file, message or item, with its path — or "nothing — read-only run">

## Consensus & divergence
<the same block that went to the user, including the C7 verdict on whether
 any consensus was earned>

## Deviations
<any phase skipped, round cut under C5, or order changed — with the reason.
 "none" if the protocol ran exactly as written.>
```

## Naming

- Run id: `<yyyymmdd-hhmm>-<protocol>`, for example `20260830-1415-debate`.
- Slot files use the slot id exactly: `agents/rune.md`.
- Never overwrite a previous run folder. If the same protocol runs twice in one minute, append
  `-2`.

## Retention

The run folder is the user's, in their OneDrive. Never delete it and never delete a previous
run's folder. If the user asks for a clean-up, list what would be removed and let them confirm.
