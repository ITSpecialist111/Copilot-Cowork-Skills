# fusion-harness

A Cowork skill that runs one question across **several different models in parallel**, then reports
whether their agreement was actually earned.

Cowork already has the orchestration — sub-agents, parallel dispatch, per-dispatch model and effort
selection. What it does not have is a protocol that makes a multi-model run worth more than one good
answer. That is what this skill adds.

Ported from [disler/fusion-harness](https://github.com/disler/fusion-harness), which ran the same
protocols outside Microsoft 365 against five provider APIs. This version is pure Cowork: a `SKILL.md`
and nine reference files. No MCP server, no local runtime, nothing to install.

---

## Why bother

If three "perspectives" are really one model, agreement between them is close to worthless. It is
the same set of priors restated three times, and it feels like corroboration while providing none.

So the skill does two things a single prompt cannot:

1. **Puts each slot on a genuinely different model**, in its own context, dispatched in parallel.
   Independence becomes structural rather than promised.
2. **Refuses to let consensus flatter you.** Contract C7, the divergence floor, requires the run to
   state whether agreement was earned — and to say so plainly when it was not.

From a verified run, unprompted:

> "Consensus — and it is earned... though note it's two houses, not three, so it isn't fully
> independent triangulation."

It had worked out on its own that Cowork offers six models from only two vendors, so three slots
gives you a different *model* each but not a different *vendor* each.

---

## Layout

```
fusion-harness/
├── SKILL.md                    the router: mode, protocol choice, roster, rules, run procedure
├── references/
│   ├── model-slots.md          model bindings, per-dispatch model and effort, evidence rules
│   ├── roster.md               persona charters, used verbatim
│   ├── contracts.md            C1–C9, including the divergence floor
│   ├── protocol-opinion.md     fan out, N independent answers, no merge
│   ├── protocol-debate.md      opening, rebuttals, closing. No judge
│   ├── protocol-fusion.md      N read-only sources, one sole-writer merge, dissent check
│   ├── protocol-collaborate.md proposals, a delegation plan as JSON, execution, integration
│   ├── protocol-auto-validate.md  gate first, build second, failures fed back verbatim
│   └── artifacts.md            run folder layout and summary.md schema
├── scripts/build-skill-zip.ps1 validates against the documented limits, then packages
├── Screenshots/                evidence from the verified runs
└── Cowork-multi-model-findings.pdf   the full write-up, 10 pages
```

`SKILL.md` stays under ~2,000 words because Cowork loads the whole body whenever the skill triggers.
Protocol detail lives in `references/`, which is loaded only when that protocol runs.

---

## The two modes

| Mode | What it is | Use when |
| --- | --- | --- |
| **Single-session** (default) | One session, one model, N personas in roster order | Exploratory work, speed, no model named by the user |
| **Model slots** | Each slot dispatched as a sub-agent on a *different model*, in parallel | The decision is expensive to get wrong, or the user names models |

Single-session is the default deliberately. It is cheaper, and running an ensemble over a settled
question produces three restatements and charges you for three. In that mode every persona shares a
model, so C7 is mandatory: agreement is cheap and the skill must say so.

### Default slot bindings

| Slot | Role | Model | Effort |
| --- | --- | --- | --- |
| `rune` | ARCHITECT | Claude → **Fable 5** | Extra High |
| `sol` | BUILDER (primary) | GPT → **GPT 5.6 Sol** | Extra High |
| `nova` | BUILDER | GPT → **GPT 5.6 Terra** | Medium |

**Fable 5 retains prompts and responses with the model provider.** The skill is required to say so
before recommending it, and to offer Opus 5 instead. Substitutes: Opus 5 for `rune`, then Sonnet 5
and GPT 5.5 as slots 4 and 5.

Six models, two vendors. There is no Gemini in Cowork, so a three-slot run gives a different model
per slot, not a different vendor per slot. The skill says that rather than implying otherwise.

---

## Install

**OneDrive.** Copy this folder's `SKILL.md` and `references/` so the path is
`/Documents/Cowork/skills/fusion-harness/SKILL.md`. Wait for sync, then start a **new** session —
custom skills are discovered at session start.

**Upload.** Run `./scripts/build-skill-zip.ps1`, then in Cowork choose
**Customize → Skills → Add ▾ → Upload skill** and pick `dist/fusion-harness.zip`. The script checks
`name`, `description`, kebab-case, folder/name match and every documented size limit first, so a
rejection at upload means something other than packaging.

### Two traps that will cost you an afternoon

**Never leave a duplicate behind.** Deleting a skill in Cowork spawns an agentic task that halts at
an approval gate — *Delete file · Paths: skills/fusion-harness · Recursive: Yes · [Cancel]
[Approve]*. Until you approve it nothing is deleted, and re-uploading gives you `fusion-harness-1`
**alongside** the original. Two skills with near-identical descriptions and the skill stops
triggering altogether, which looks exactly like a propagation failure and is not one.
**Delete → approve → confirm it is gone → upload.**

**Then wait.** A freshly uploaded skill appears in *Your skills* immediately but is not loadable for
roughly ten minutes. Sessions started inside that window report that no such skill exists, and an
explicit `/fusion-harness` renders *Custom skill … failed*. Do not start editing frontmatter.
Verified non-causes: forward-slash zip entries, a `>-` folded description, and the `license` and
nested `metadata` keys all parse correctly.

---

## Verify it works

Run these in order in a **new** session. Each checks a different failure mode.

| # | Prompt | Passes if |
| --- | --- | --- |
| 1 | `What skills do you have available?` | `fusion-harness` is listed |
| 2 | `Run a fusion opinion round on this question: should a 6-person IT team standardise on Teams or on email for release announcements?` | Sections headed `[RUNE]`, `[SOL]`, `[NOVA]`; a comparison table; a consensus block carrying the C7 verdict; a run folder in the output panel |
| 3 | `Debate this over 3 rounds: our change-approval process should be removed entirely.` | Nine turns; round 2 cites `[SLOT]` by name; no judge picks a winner |
| 4 | `Fan this out across three different models and give me the opinion round: <question>` | A slot table naming three models before dispatch; three parallel sub-agents; C7 addresses the two-vendor limit |
| 5 | `What's the capital of France?` | The skill does **not** fire, or fires and immediately declines as out of scope |

Test 5 is the one that usually fails. An over-triggering skill is worse than a missing one — it makes
every trivial question cost three passes. If it fires, tighten the `description` frontmatter, not the
body: the description is the only part Cowork reads when deciding.

---

## Evidence

Cowork's multi-model claim was tested rather than assumed. Two independent instruments, agreeing.

**The platform's own session record** for one run:

```
model: gpt-5.6-sol      status: completed   duration: 48,775 ms
model: claude-fable-5   status: completed   duration: 48,388 ms
model: claude-sonnet-5  status: completed   duration: 47,588 ms
```

Durations within 1.2 seconds of each other — parallel, not sequential.

**Microsoft Purview's unified audit log**, independently, on the same activity:

```json
"AppHost": "cowork",
"ModelTransparencyDetails": [
  { "ModelName": "GPT-5.6 Terra", "ModelProviderName": "OpenAI" }
]
```

Worth knowing: the current Microsoft Learn page states Cowork "doesn't show provider details". In the
tested tenant it plainly does. Read that as documentation lag and check your own.

A model's self-report is **not** evidence — the slot on Fable 5 identified itself as "Claude Sonnet
4.5". Right vendor, wrong model. `references/model-slots.md` forbids quoting self-reports.

The full write-up, including what the evidence does *not* prove, is in
[Cowork-multi-model-findings.pdf](Cowork-multi-model-findings.pdf). Screenshots are in
[Screenshots/](Screenshots/), with tenant identifiers redacted.

### Cost

Two measured three-model fan-outs cost **151** and **362 credits**, against **11–38** for ordinary
single-turn sessions. That spread is wide, so treat it as an order of magnitude rather than a price.
Run the harness in its own fresh session: `/cost` is scoped to one task, which turns it into an exact
meter for the run.

---

## Editing it

The persona charters in `references/roster.md` are load-bearing and must be used verbatim.
Paraphrasing them collapses the personas into one voice within a turn, which is exactly the failure
this skill exists to prevent.

If you add a protocol, add a row to the routing table in `SKILL.md` and a new
`references/protocol-*.md`. Do not inline it — the body loads in full on every trigger.

---

## Credits

Protocols and persona model from [disler/fusion-harness](https://github.com/disler/fusion-harness).
Cowork port, model-slot mode and the evidence work are mine. Testing was done in a Microsoft demo
tenant; see the repository [DISCLAIMER](../DISCLAIMER.md).
