# Mode: model slots

Cowork can dispatch **sub-agents with a per-dispatch model override**. That makes real
cross-model fan-out possible inside a single session — the thing the pi harness was actually
buying. Verified live on 2026-08-30; see the evidence rule below.

## What the platform can and cannot do

| Fact | Consequence |
| --- | --- |
| Sub-agent dispatch accepts an explicit **model** parameter | Each slot runs on the model you name. No manual picker switching |
| Sub-agents run in **separate sessions with separate contexts** | C1 independence is structural, not promised. Dispatch all slots in parallel |
| The dispatch result carries a **runtime session record** naming the executing model | This is your evidence. Record it verbatim |
| **Effort is settable per dispatch** | Name it per slot. A run at Extra High / Extra High / Medium was applied and honoured |
| The compose-box picker governs **only the main conversation** | Pinning the session does not constrain the slots |
| The picker is grouped by vendor: **GPT** (OpenAI) → GPT 5.6 Sol, GPT 5.6 Terra, GPT 5.5 · **Claude** (Anthropic) → Opus 5, Sonnet 5, Fable 5 | Six models, two vendors |
| **Fable 5 requires data retention** — prompts and responses are kept by the model provider | Say so before recommending it, every time. Offer Opus 5 instead |

The model list is per-tenant. If a named model is missing, say so and substitute rather than
asserting a model was used.

## The evidence rule

After every slot returns, read the **platform's runtime session record** for that dispatch and
report the executing model verbatim, in `provider/id` form. Verified values look like:

```
rune → model: anthropic/fable-5
sol  → model: substrate-responses/gpt-5.6-sol
nova → model: anthropic/sonnet-5
```

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
| `rune` | ARCHITECT | Claude → **Fable 5** | Extra High | The toughest-problem slot. **Retention applies** — offer Opus 5 instead |
| `sol` | BUILDER (primary) | GPT → **GPT 5.6 Sol** | Extra High | Different vendor, strong on concrete execution |
| `nova` | BUILDER | GPT → **GPT 5.6 Terra** | Medium | The fast, cheap challenger |

That is `anthropic/claude-fable-5` + `openai/gpt-5.6-sol` + `openai/gpt-5.6-terra` at
`xhigh`/`xhigh`/`medium` — the same trio as `.pi/fusion-harness/model-stack-trio.yaml`, with
Cowork's **Extra High** standing in for `xhigh`.

Substitutions:

- **Opus 5** for `rune` whenever the user declines Fable 5's retention. This is the safe default
  for anything touching real tenant data.
- **Sonnet 5** and **GPT 5.5** as slots 4 and 5. The roster caps at five, so with six models
  available one is always left out — name which, rather than quietly dropping it.

**Be honest about the ceiling.** Six models, two houses: OpenAI and Anthropic. The pi stack's third
vendor is Gemini and there is no Gemini here. A three-slot Cowork run gives a different *model* in
every slot, not a different *house* in every slot. Say that rather than implying three independent
vendors — the whole point of recording the badge is that the claim stays checkable.

## Running a model-slot protocol

**1. Quote the cost and the roster, then proceed.** Print the slot table — slot, model, phase —
before dispatching. Warn about Fable 5 retention if it is in the stack.

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
