# Copilot Cowork — Skills Library

A dedicated research and experimentation repository for **Microsoft 365 Copilot Cowork** custom skills. This workspace is where I design, test, and evolve reusable skill packages that extend Cowork's agentic capabilities across concrete business workflows.

> **Status:** Research / art-of-the-possible. This repository is a personal exploration of what is technically feasible today with Copilot Cowork custom skills. It is **not** a Microsoft product, nor an official reference implementation.

---

## What is Copilot Cowork?

[Microsoft 365 Copilot Cowork](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/) is an agentic experience inside Microsoft 365 Copilot that can work alongside a user across email, documents, calendar, and line-of-business data. Cowork supports **custom skills** — small, declarative packages (a `SKILL.md` plus optional `references/`, `scripts/`, and `assets/`) that teach Cowork a new reusable capability. Skills sync into Cowork from the user's OneDrive.

This repo is a library of such skill packages, organised by theme.

---

## Repository Layout

| Folder | Purpose | Status |
|---|---|---|
| [`skill-factory/`](skill-factory/) | A meta-skill: a skill that **creates other skills** to a rigorous quality bar (frontmatter, tiering, trigger phrases, cross-linking, post-write verification). | Operational |
| [`rfp-agent-swarm/`](rfp-agent-swarm/) | A seven-skill agent swarm that takes an inbound RFP from first ingestion through to a fully-assembled, reviewed, and gate-approved submission package. See the [overview](rfp-agent-swarm/README.md). | Research |
| [`executive-report-design-system/`](executive-report-design-system/) | A design system as a skill: produces multi-page, print-ready HTML executive reports that look designed rather than generated, by removing the model's authority over layout and giving it a closed component catalogue instead. See the [overview](executive-report-design-system/README.md). | Research |

---

## What I'm Trying to Achieve

This library is organised around a handful of hypotheses I want to prove (or disprove) about Cowork custom skills:

1. **Meta-authoring works.** A single well-designed skill (`skill-factory`) can reliably author other skills to a published quality bar, reducing the cost of building new agentic workflows from days to minutes.
2. **Agent swarms can be expressed as skill chains.** Complex multi-stage knowledge work (bids, proposals, security questionnaires) can be decomposed into a sequence of cooperating, narrowly-scoped skills with explicit upstream/downstream contracts and a shared audit trail.
3. **Humans stay in the loop, by design.** Every skill in every chain has explicit *gates* and *review steps* — AI drafts, humans approve. Confidence tiering, provenance, and structured correction capture are first-class concerns, not afterthoughts.
4. **The artefacts are portable.** A skill is just Markdown plus a pinch of Python and static templates. Anyone with Cowork access can lift a skill package out of this repo, drop it into their own OneDrive, and adapt it.
5. **Learning loops compound.** Every reviewer correction should make the next run cheaper. Skills here log corrections in a shared schema so the knowledge base genuinely improves over time.
6. **Constraint beats instruction.** Asking a model to "avoid a generic AI look" fails, because the request travels the same channel that produced the look. Removing the choice — a frozen stylesheet, a closed component catalogue, a validated data contract — makes output quality a property of the design rather than of the prompt. `executive-report-design-system` is the test of this.

Future themes I plan to add as separate folders:

- **Sales & account planning** — account research, QBR prep, opportunity scoring
- **Meeting lifecycle** — prep → run → follow-up with decisions logged
- **Deep research** — structured literature reviews with citation hygiene
- **Internal comms** — exec briefings, all-hands drafts, change management

Each will follow the same pattern: one folder, a short art-of-the-possible README, and one or more `SKILL.md` packages.

---

## How to Use a Skill

1. Clone or download the skill folder (e.g. `rfp-agent-swarm/skills/rfp-intake/`).
2. Copy it into your Cowork personal skills location (`Cowork/Skills/<skill-name>/` in OneDrive).
3. Wait for Cowork to pick it up (typically under a minute).
4. Invoke with one of the trigger phrases listed in the skill's `SKILL.md` description.

> The fastest way to get a feel for this is to install [`skill-factory`](skill-factory/) first and ask it to generate a small skill for you.

---

## Disclaimers

- **Not a Microsoft product.** This is a personal research repository. Nothing here is endorsed, supported, or warranted by Microsoft Corporation.
- **Not a reference implementation.** The skills here reflect one person's working hypotheses. Official guidance lives at [Microsoft Learn — Cowork](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/) and wins over anything in this repo if the two disagree.
- **No customer data.** Any company names, email domains, or sample content are generic placeholders (`Contoso`, `contoso.com`, etc.). No real customer identities, contracts, pricing, or confidential material are included.
- **No guarantees.** Skills that look production-ready are still research artefacts. Validate carefully before using them with real data, especially for anything with legal, financial, or security consequences.
- **Human in the loop required.** Every skill in this repo assumes a human reviewer signs off before output is shipped externally. Do not wire these into fully automated pipelines.
- **Licensing.** See [`LICENSE`](LICENSE). Use of Copilot Cowork itself requires an appropriate Microsoft 365 Copilot licence — consult the Microsoft Learn docs for current requirements.

---

## Contributing

This is a personal library, but thoughtful issues and pull requests are welcome — especially: (a) bug reports on existing skills, (b) new trigger phrases, (c) corrections to workflows, and (d) suggestions for new skill themes. Please open an issue first for anything larger than a minor fix.

---

*Last updated: April 2026.*
