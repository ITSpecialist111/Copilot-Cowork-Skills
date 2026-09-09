# Mode: model slots

Cowork can dispatch **sub-agents with a per-dispatch model override**. That makes real
cross-model fan-out possible inside a single session — the thing the pi harness was actually
buying. Dispatch was verified live on 2026-08-30; the picker inventory was refreshed from
[Microsoft's Cowork model documentation](https://learn.microsoft.com/microsoft-365/copilot/cowork/cowork-models)
on 2026-09-09. See the evidence rule below.

## What the platform can and cannot do

| Fact | Consequence |
| --- | --- |
| Sub-agent dispatch accepts an explicit **model** parameter | Each slot runs on the model you name. No manual picker switching |
| Sub-agents run in **separate sessions with separate contexts** | C1 independence is structural, not promised. Dispatch all slots in parallel |
| The dispatch result carries a **runtime session record** naming the executing model | This is your evidence. Record it verbatim |
| **Effort is settable per dispatch** | Name it per slot. A run at Extra High / Extra High / Medium was applied and honoured |
| The compose-box picker governs **only the main conversation** | Pinning the session does not constrain the slots |
| The picker is grouped by vendor: **GPT** (OpenAI) → GPT 5.5, GPT 5.6 Sol, GPT 5.6 Terra, GPT 6 Astra · **Claude** (Anthropic) → Opus 5, Claude Sonnet 5, Claude Fable 5.1 | Seven models, two vendors |
| **Fable 5.1 terms vary by tenant eligibility** | Inspect the picker/banner. It may run under Microsoft's DPA with no Anthropic retention, or as a retention variant under additional terms |

Microsoft documents both Fable arrangements in
[Anthropic models in Microsoft Online Services](https://learn.microsoft.com/microsoft-365/copilot/connect-to-ai-subprocessor#anthropic-fable-class-models).
Do not infer the tenant's arrangement from the model name alone.

The model list is per-tenant. If a named model is missing, say so and substitute rather than
asserting a model was used.

## The evidence rule

After every slot returns, read the **platform's runtime session record** for that dispatch and
report the executing model verbatim, in `provider/id` form. Historical values from the
2026-08-30 run looked like:

```
rune → model: anthropic/fable-5
sol  → model: substrate-responses/gpt-5.6-sol
nova → model: anthropic/sonnet-5
```

Those are evidence from the old roster, not identifiers to reuse for Fable 5.1 or GPT 6 Astra.
Record the current runtime values rather than guessing their provider IDs from picker labels.

**Never use a model's self-report as evidence.** Measured in the same run: the slot on Fable 5
identified itself as "Claude Sonnet 4.5" — right vendor, wrong model — and the other two said
"unknown". Self-identification is unreliable and must be labelled as such if quoted at all.

State the honest limit once: attribution rests on platform metadata. If the runtime silently
substituted a model while reporting the requested one, that is not detectable from here.

## Two modes

### Single-session mode — the default

One session, one model, N personas in roster order. Everything in `references/roster.md` and
`references/contracts.md` applies as written, **including the divergence floor (C7)**: agreement
between personas on one model is not evidence.

Use it when the run is exploratory, when speed matters, or when the user has not asked for
specific models. It is the cheaper and simpler mode and it is the right default.

### Model-slot mode — real fan-out

One sub-agent per slot, each dispatched with its own model and effort, all in parallel from this
session. Independence is **structural** rather than promised: each sub-agent runs in its own
context, so a slot cannot have seen another slot's answer.

Use it when the decision is expensive to get wrong, when the user asks for specific models, or
when they say "fan this out", "run this on Opus and Sol", or "actually use different models".

In this mode C7 relaxes: agreement across two vendors is real corroboration. Say so — and still
name what none of them checked.

## Slot bindings

This mirrors the pi stack in `.pi/fusion-harness/model-stack-copilot.yaml`.

This reproduces the upstream fusion stack model for model.

| Slot | Role | Model | Effort | Why |
| --- | --- | --- | --- | --- |
| `rune` | ARCHITECT | Claude → **Fable 5.1** | Extra High | Most advanced ambitious-work slot. Check and disclose the tenant's retention terms |
| `sol` | BUILDER (primary) | GPT → **GPT 6 Astra** | Extra High | Latest tough-problem model, strong on concrete execution |
| `nova` | BUILDER | GPT → **GPT 5.6 Terra** | Medium | The fast, cheap challenger |

Request the picker labels above exactly. Do not infer provider IDs: after each dispatch, record
the actual runtime model metadata and compare it with the requested label. Cowork's **Extra High**
stands in for Pi's `xhigh` on the first two slots.

Substitutions:

- **Opus 5** for `rune` whenever the available Fable 5.1 variant requires retention and the user
  declines it.
- **Claude Sonnet 5** and **GPT 5.6 Sol** as slots 4 and 5. The roster caps at five, so with seven
  models available at least two are left out — name them rather than quietly dropping them.

**Be honest about the ceiling.** Seven models, two houses: OpenAI and Anthropic. The Pi stack's third
vendor is Gemini and there is no Gemini here. A three-slot Cowork run gives a different *model* in
every slot, not a different *house* in every slot. Say that rather than implying three independent
vendors — the whole point of recording the badge is that the claim stays checkable.

## Running a model-slot protocol

**1. Quote the cost and the roster, then proceed.** Print the slot table — slot, model, phase —
before dispatching. For Fable 5.1, inspect and disclose the retention state shown by the product.

**2. Write the run artifacts first.** `prompt.md` and `roster.md` before any slot speaks.

**3. Dispatch every slot in parallel**, each with its explicit model parameter and a
**self-contained** prompt: the charter verbatim, the shared evidence, the question, and the output
contract. A sub-agent has no memory of this session, so anything it needs must be in its prompt.

**4. Collect the runtime model for each slot** and check it against what you requested. A mismatch
means the run is not what it claims — say so and either re-dispatch or record it under C9. Never
relabel silently.

**5. Merge or compare** per the protocol. The merge happens in this session, which has not itself
argued any of the positions.

## Fallback: one session per slot

If sub-agent dispatch is unavailable, fall back to the manual route: the user sets the picker,
pastes a self-contained slot prompt, and the artifacts hand off through the OneDrive Cowork folder.
This is slower and needs the user in the loop for every slot.

## Cost

Model-slot mode costs one model turn per slot plus the merge, and each slot is a full sub-agent
session with its own context load. Two three-model fan-outs measured in one tenant cost **151** and
**362 credits**, against **11–38 credits** for ordinary single-turn sessions. That spread is wide,
so quote it as an order of magnitude rather than a price. Quote the mode, the models and the slot
count before starting, and offer single-session mode as the cheaper answer.

**Measuring a run.** Ask the user to type `/cost` after the run. It reports credits for the current
task and costs nothing to use. You cannot invoke it — it is a client-side slash command and is not
exposed to you as a tool; asked to call it, the platform answers *"no such skill or tool is available
in this session"*. So never state a credit figure yourself. Because `/cost` is scoped to one task,
run the harness in a fresh session and it becomes an exact meter for that run.

## Degrading gracefully

If the user wants fan-out but not the cost, run single-session mode and say plainly that the
personas share a model, so C7 applies and agreement is not evidence. That is an honest cheaper run.
Silently running single-session mode while presenting it as multi-model is not.
