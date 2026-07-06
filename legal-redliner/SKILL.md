---
name: legal-redliner
description: |
  Jurisdiction-aware legal document redlining agent: ingests customer-facing legal
  documents (NDAs, MSAs, DPAs, T&Cs, SOWs), segments them into clauses, rewrites
  each clause to align with internal policy positions and regional legal requirements,
  produces a fully redlined document plus a structured audit pack with change-by-change
  rationale and citations. Supports UK, EU, US, and custom jurisdictions.
  Use when user says "redline this contract", "review against our playbook",
  "localize this agreement", "adapt for EU", "adapt for UK", "jurisdiction review",
  "policy-aligned redline", "clause review", "contract redline", "playbook review",
  "mark up this agreement", "regional adaptation", "legal playbook",
  "NDA review", "MSA review", "DPA review", "T&Cs review",
  "standard positions review", "contract markup with audit trail",
  or needs jurisdiction-specific, policy-aligned contract redlining with full
  auditability.
---

# Legal Redliner

Redline customer-facing legal documents clause-by-clause — aligning each clause to your internal policy positions and jurisdiction-specific legal requirements — with a complete audit trail showing what changed, why, and what evidence supports each change.

## When to Use

- User has a legal document (NDA, MSA, DPA, SOW, T&Cs) that needs redlining against company playbook positions
- User needs to adapt a contract for a specific jurisdiction (UK, EU, US states, etc.)
- User wants a structured audit pack showing every change with rationale and citations
- User needs to compare contract language against internal standard positions
- User wants clause-by-clause analysis with risk flags for non-standard terms

## When NOT to Use

- Litigation or dispute management → use `legal-review`
- Vendor evaluation or spend analysis → use `vendor-intel`
- General contract term extraction without redlining → use `vendor-intel`
- Sending the redlined document to someone → use `email` after redlining

## Quick Start

**User**: "Redline this MSA against our standard positions for a UK customer."

**Steps**:
1. Ingest and segment the document into clauses
2. Identify the document type, jurisdiction, and applicable policies
3. For each clause: retrieve relevant policy positions, check jurisdiction requirements, rewrite if needed
4. Assemble the redlined document with tracked changes
5. Generate the audit pack (change log, citations, risk flags, human review checklist)

---

## How It Works

### Architecture Overview

This skill operates as a **clause-by-clause redlining pipeline** — rather than loading all policies and legislation at once (which would overwhelm context), it performs targeted retrieval per clause.

```
INGEST → CLASSIFY → SEGMENT → [PER-CLAUSE LOOP] → ASSEMBLE → DELIVER
                                    |
                                    ├── Retrieve internal policy snippets
                                    ├── Retrieve jurisdiction-specific requirements
                                    ├── Rewrite with minimal changes
                                    ├── Validate against constraints
                                    └── Record evidence + rationale
```

### Why Clause-by-Clause

- **Precision**: Each clause gets only the relevant policy and legal context
- **Auditability**: Every change maps to specific evidence
- **Control**: Deterministic loop ensures nothing is skipped
- **Transparency**: The audit pack traces each decision back to sources

---

## Redlining Workflow

### Step 1: Document Ingestion

1. **Locate the document** — check `input/` for uploaded files first
2. **Extract text** — use the `pdf` skill for PDFs or `docx` skill for Word files to extract full text
3. **Identify document metadata**:

   | Field | Value |
   |-------|-------|
   | Document Type | NDA / MSA / DPA / SOW / T&Cs / Other |
   | Counterparty | [Name] |
   | Target Jurisdiction | UK / EU / Germany / US-CA / US-NY / etc. |
   | Governing Law | [As stated in doc] |
   | Date | [Document date] |
   | Our Role | Customer / Supplier / Both |

### Step 2: Classification & Context Setup

Based on the document type and jurisdiction, establish:

**Policy positions to retrieve** (examples by document type):

| Document Type | Key Policy Areas |
|--------------|------------------|
| **NDA** | Definition of confidential information, exclusions, term, return/destruction, permitted disclosures, injunctive relief |
| **MSA** | Liability caps, indemnification, IP ownership, warranty, termination, change control, dispute resolution |
| **DPA** | Processing purposes, sub-processors, international transfers, breach notification, data subject rights, DPIA obligations |
| **SOW** | Scope definition, acceptance criteria, change orders, milestones, payment terms, resource commitments |
| **T&Cs** | Liability limitations, consumer rights, refund/cancellation, data collection notices, cookie consent |

**Jurisdiction-specific requirements** (examples):

| Jurisdiction | Key Considerations |
|-------------|-------------------|
| **UK** | UK GDPR, Consumer Rights Act 2015, Unfair Contract Terms Act 1977, PECR |
| **EU** | EU GDPR, EU consumer directives, local member state implementations |
| **Germany** | BGB (German Civil Code) provisions, stricter GDPR interpretation, specific AGB rules |
| **US — California** | CCPA/CPRA, California-specific consumer protections |
| **US — New York** | NY General Obligations Law, specific warranty rules |
| **US — Delaware** | Choice of law preferences, corporate governance considerations |

### Step 3: Document Segmentation

Use the segmentation script to split the contract into individually addressable clauses:

```bash
python scripts/segment_contract.py <contract_text_file> --output working/segmented.json
```

The script automatically:
- Detects clause headings (numbered sections, articles, schedules)
- Extracts preamble/recitals as CL-000
- Classifies each clause by content type (definitions, obligations, liability, termination, data processing, IP)
- Extracts defined terms and cross-references
- Returns a confidence score for segmentation quality

Review the JSON output and verify the segmentation. If confidence is "low", manual segmentation may be needed.

The script produces a structured table:

| Clause ID | Section | Clause Heading | Clause Text | Classification |
|-----------|---------|---------------|-------------|----------------|
| CL-001 | 1 | Definitions | [full text] | Standard / Non-standard / Missing |
| CL-002 | 2.1 | Scope of Services | [full text] | Standard / Non-standard / Missing |
| ... | | | | |

**Classification key:**
- **Standard**: Matches or closely aligns with our standard positions
- **Non-standard**: Deviates from our standard positions — needs redlining
- **Missing**: A clause our playbook requires that's not in the document
- **Acceptable**: Non-standard but within acceptable deviation range

### Step 4: Per-Clause Redlining

For each clause marked as Non-standard or Missing, apply this process:

#### 4a. Retrieve Relevant Context

- **Internal policy**: Find the company's standard position for this clause type
- **Jurisdiction requirements**: Find any legal requirements that affect this clause in the target region

**Sources** (in priority order):
1. User-provided policy documents (uploaded to `input/`)
2. Organization's SharePoint playbook (if user directs to a location — use enterprise search to find it)
3. **Official legislation** — see Legislation Sourcing Rule below
4. General best practice for the clause type and jurisdiction

**Legislation Sourcing Rule (MANDATORY):**
All jurisdiction-specific legal citations MUST be retrieved from official government or legislative sources at redlining time — never from pre-training knowledge alone. Use the `deep-research` agent or web search/fetch tools to retrieve the current text of any statute, regulation, or directive being cited.

- **If the user has provided explicit legislation documents** (uploaded to `input/` or linked in their request), use those as the authoritative source. No web lookup is needed for provisions covered by the user's documents.
- **For all other legislation**, fetch from official sources before citing. See [references/jurisdiction-sources.md](references/jurisdiction-sources.md) for the full jurisdiction source table with official URLs. Key sources:
  - **Germany**: gesetze-im-internet.de (BGB, UrhG, BDSG, HGB, etc.)
  - **EU**: eur-lex.europa.eu (GDPR, directives, SCCs decisions)
  - **UK**: legislation.gov.uk (UK GDPR, DPA 2018, UCTA 1977, CRA 2015)
  - **US**: govinfo.gov, state legislature sites (CCPA, UCC, state statutes)
- If an official source cannot be reached or the provision cannot be verified, flag the clause as `NEEDS_RESEARCH` with the note "Legislation not verified from official source" rather than citing from memory.
- Record the source URL and retrieval date in the audit pack's Legal Ref column for every legislative citation.

#### 4b. Rewrite the Clause

**Non-negotiable rewriting rules:**
1. **Minimal changes** — prefer targeted edits over full rewrites
2. **Preserve defined terms** exactly (capitalisation, wording)
3. **Preserve structure** — don't renumber or reorganise unless required
4. **External law prevails** — if internal policy conflicts with mandatory law, law wins (note the conflict)
5. **Conservative approach** — when in doubt, flag for human review rather than rewrite
6. **No invented law** — all legal citations must be verified against official government sources at redlining time (see Legislation Sourcing Rule in Step 4a). If the provision cannot be verified, flag `NEEDS_RESEARCH` rather than citing from memory

#### 4c. Record the Change

For every change, capture:

| Field | Content |
|-------|---------|
| Clause ID | CL-XXX |
| Change Type | Insert / Delete / Replace / Add Missing Clause |
| Original Text | [exact original wording] |
| Revised Text | [proposed new wording] |
| Rationale | [why this change was made — in plain language] |
| Policy Citation | [which internal policy position this aligns to] |
| Legal Citation | [which law or regulation requires or supports this] |
| Risk Level | Low / Medium / High |
| Needs Human Review? | Yes / No |
| Open Questions | [anything unresolved or uncertain] |

#### 4d. Validate

Before finalizing each clause:
- Does the revised text align with the cited policy position?
- Does it comply with the cited jurisdiction requirement?
- Are defined terms preserved?
- Is the commercial position unchanged (unless compliance requires it)?
- Is the change truly necessary, or is the original acceptable?

---

## Output Deliverables

The legal redliner produces two documents:

### 1. Redlined Document

A Word document with tracked changes showing:
- Deleted text (strikethrough, red)
- Inserted text (underline, red)
- Comments on each change referencing the audit pack entry

**Use the `docx` skill** to create the redlined document with proper tracked changes formatting.

Include the privilege notice from [assets/privilege-notice.md](assets/privilege-notice.md) at the top of the document and as the header on every page.

When inserting missing clauses (e.g., force majeure, third party rights, severability), use the pre-approved standard wording from [assets/standard-clauses-uk.md](assets/standard-clauses-uk.md) instead of generating from scratch. This ensures consistency with the legal team's approved language.

### 2. Audit Pack

A comprehensive audit record. Generate as an Excel workbook using the `xlsx` skill with these sheets:

**Sheet 1: Change Log**

| Clause ID | Section | Change Type | Original Text | Revised Text | Rationale | Policy Ref | Legal Ref | Risk | Human Review? |
|-----------|---------|-------------|---------------|-------------|-----------|-----------|----------|------|---------------|

**Sheet 2: Risk Summary**

| Risk Level | Count | Clauses |
|-----------|-------|---------|
| High | | [list] |
| Medium | | [list] |
| Low | | [list] |

**Sheet 3: Human Review Checklist**

| # | Clause ID | Item for Review | Reason | Reviewer | Status |
|---|-----------|----------------|--------|----------|--------|
| | | | Insufficient policy data / Judgment call / Complex clause | | Pending / Reviewed / Approved |

**Sheet 4: Coverage Summary**

| Total Clauses | Standard (no change) | Redlined | Missing (added) | Needs Research | % Coverage |
|--------------|---------------------|----------|-----------------|----------------|------------|

**All counts and percentages must be computed using code tools.**

---

### 3. Risk Dashboard (Adaptive Card)

Before generating the file deliverables, render an inline risk dashboard using the `render-ui` skill so the user can review the summary at a glance. The card must include:

**KPI Row** (ColumnSet with 4 columns):
- Total Clauses (count)
- Redlined (count + percentage)
- Standard (count, green)
- Coverage (percentage, green if 100%)

**Risk Distribution** (Chart.Donut):
- High Risk (attention colour) with count
- Medium Risk (warning colour) with count
- Low Risk (good colour) with count
- Standard (neutral colour) with count

**Clause Summary Table** (Table):
- Columns: Clause ID | Clause Name | Key Issue | Risk (as Badge) | Human Review? (as Badge where applicable)
- Only show non-standard clauses (omit standard clauses from the table)
- Sort by risk level: High first, then Medium, then Low

**Legislation Verified** (FactSet):
- List each statute cited with its source (e.g., "UCTA 1977 s.2 → legislation.gov.uk")

Render the card **before** generating the Word and Excel files — this gives the user a chance to review the analysis before committing to file generation.

---

## Supported Document Types

| Type | Abbreviation | Typical Clauses Reviewed |
|------|-------------|------------------------|
| Non-Disclosure Agreement | NDA | Confidentiality definition, exclusions, term, return, remedies |
| Master Service Agreement | MSA | Scope, liability, indemnity, IP, warranty, termination, governing law |
| Data Processing Agreement | DPA | Processing purposes, sub-processors, transfers, breach notification, DSAR |
| Statement of Work | SOW | Scope, deliverables, acceptance, milestones, change control, payment |
| Terms and Conditions | T&Cs | Liability, consumer rights, data, refunds, dispute resolution |
| Software License Agreement | SLA | License scope, restrictions, support, updates, audit rights |
| Employment Agreement | EA | Duties, compensation, restrictive covenants, IP assignment, termination |

---

## Built-In Skills Used

This skill leverages Copilot Cowork's built-in capabilities:

| Built-in Skill | How It's Used |
|---------------|--------------|
| **Word** | Read input documents, create redlined output with tracked changes |
| **PDF** | Extract text from PDF contracts, create final PDF versions |
| **Excel** | Generate the audit pack workbook with change log, risk summary, and coverage |
| **Enterprise Search** | Find internal playbook documents and policy positions across SharePoint |
| **Deep Research** | Research jurisdiction-specific legal requirements when policy sources are insufficient |
| **Email** | Send the completed redline and audit pack to reviewers for approval |
| **Communications** | Draft cover notes using [assets/cover-note-template.md](assets/cover-note-template.md) explaining the redline for stakeholders |
| **Adaptive Cards** | Display the risk summary and coverage dashboard inline before generating files |
| **Scheduling** | Book review meetings with legal team to walk through the redline |
| **Calendar Management** | Check reviewer availability before scheduling review sessions |
| **Meetings** | Prepare briefing notes for the redline review meeting |

---

## Workflow Integration

### End-to-End Process

1. **User uploads contract** → Legal Redliner segments and classifies
2. **Redlining** → Clause-by-clause analysis with audit trail
3. **Review dashboard** → Display risk summary and coverage as an **Adaptive Card** for quick review
4. **Generate deliverables** → Redlined **Word** document + **Excel** audit pack
5. **Circulate for review** → **Email** the package to the legal team with a cover note via **Communications**
6. **Schedule review** → Use **Scheduling** to find time for the legal team to review together
7. **Post-review** → Update the redline based on feedback, generate final versions

### Multi-Jurisdiction Handling

When a document needs adaptation for multiple regions:
- Run the redliner once per jurisdiction
- Generate a comparison view showing regional differences
- Highlight clauses where jurisdictions require conflicting approaches
- Recommend the most conservative position that satisfies all jurisdictions, or separate regional versions

---

## Quality Assurance

### Pre-Delivery Checks

Before delivering the redline:

- [ ] Every change has a rationale and at least one citation
- [ ] All defined terms preserved exactly
- [ ] No commercial position changed without explicit flagging
- [ ] Risk levels assigned consistently
- [ ] Human review items clearly identified
- [ ] Coverage > 90% (all clauses addressed or explicitly marked)
- [ ] Audit pack totals match the redlined document
- [ ] Document formatted correctly with tracked changes visible

### Confidence Indicators

For each clause assessment:
- **High confidence**: Both policy source and legal source available, clear alignment
- **Medium confidence**: Policy source available but no jurisdiction-specific confirmation, or vice versa
- **Low confidence / Needs Research**: Insufficient sources — flagged for human review

---

## Guardrails

- **This skill does NOT provide legal advice**: All redlines are drafting suggestions based on policy alignment and identified legal requirements. A qualified lawyer must review before any document is finalized.
- **Never invent law or policy**: All legislative citations must be retrieved and verified from official government sources (e.g., gesetze-im-internet.de, eur-lex.europa.eu, legislation.gov.uk) at redlining time — not from pre-training knowledge. The only exception is when the user has explicitly provided the legislation as uploaded documents. If a provision cannot be verified from an official source, flag `NEEDS_RESEARCH` — never fabricate or cite from memory
- **Minimal intervention principle**: Prefer targeted edits over rewrites. The goal is compliance and policy alignment, not stylistic preference.
- **Commercial neutrality**: Do not change the commercial position (pricing, scope, payment terms) unless specifically required for legal compliance — flag any commercial impact prominently
- **Confidentiality**: Contract documents are commercially sensitive. Never reference details from one counterparty's contract in another review.
- **Privilege**: Mark all redlining output as "PRIVILEGED AND CONFIDENTIAL — ATTORNEY WORK PRODUCT" unless user instructs otherwise
- **All calculations computed by code tools**: Coverage percentages, clause counts, risk distributions — never estimate

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Contract is a scanned PDF with no text | Image-only PDF | Use `pdf` skill with OCR extraction first |
| No internal playbook provided | User hasn't uploaded policy documents | Ask user to provide or point to SharePoint location; use enterprise search to find |
| Jurisdiction not supported | Niche jurisdiction with no available sources | Flag all jurisdiction-dependent clauses as `NEEDS_RESEARCH`, recommend local counsel review |
| Too many "Needs Research" flags | Insufficient source material | Engage the `deep-research` skill to investigate specific legal requirements, then re-run affected clauses |
| Redline changes commercial terms | Clause mixes legal and commercial language | Separate the legal compliance change from the commercial term, flag the commercial element for business review |
| Audit pack doesn't match redline | Manual edits after generation | Always regenerate audit pack from the final redlined document |
