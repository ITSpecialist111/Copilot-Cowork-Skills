# Legal Redliner — Jurisdiction Sources Reference

Official legislation sources by jurisdiction. Loaded on demand when the redliner needs to verify legal requirements for a specific region.

## United Kingdom

| Legislation | Official Source | Notes |
|------------|----------------|-------|
| UK GDPR | legislation.gov.uk/eur/2016/679/contents | As retained and amended post-Brexit |
| Data Protection Act 2018 | legislation.gov.uk/ukpga/2018/12/contents | Supplements UK GDPR |
| Consumer Rights Act 2015 | legislation.gov.uk/ukpga/2015/15/contents | Consumer contract terms |
| Unfair Contract Terms Act 1977 | legislation.gov.uk/ukpga/1977/50/contents | B2B reasonableness test |
| PECR 2003 | legislation.gov.uk/uksi/2003/2426/contents | Electronic communications |
| Companies Act 2006 | legislation.gov.uk/ukpga/2006/46/contents | Corporate governance |

**Key considerations for UK contracts:**
- Post-Brexit: UK GDPR is separate from EU GDPR — check for divergences
- International data transfers: UK adequacy decisions and UK IDTA replace EU SCCs
- Consumer contracts: CRA 2015 makes certain terms automatically unfair
- UCTA 1977 applies to B2B: exclusion of liability for negligence must pass reasonableness test

## European Union

| Legislation | Official Source | Notes |
|------------|----------------|-------|
| GDPR (Regulation 2016/679) | eur-lex.europa.eu/eli/reg/2016/679/oj | Core data protection |
| ePrivacy Directive 2002/58/EC | eur-lex.europa.eu/eli/dir/2002/58/oj | Cookies, electronic comms |
| Unfair Contract Terms Directive 93/13/EEC | eur-lex.europa.eu/eli/dir/1993/13/oj | Consumer protection |
| Digital Services Act | eur-lex.europa.eu/eli/reg/2022/2065/oj | Platform obligations |
| AI Act (Regulation 2024/1689) | eur-lex.europa.eu/eli/reg/2024/1689/oj | AI system obligations |
| Standard Contractual Clauses (2021/914) | eur-lex.europa.eu/eli/dec_impl/2021/914/oj | International transfers |

**Key considerations for EU contracts:**
- GDPR applies to processing of EU residents' data regardless of entity location
- SCCs required for transfers to non-adequate countries
- Consumer contracts: Directive 93/13 makes unfair terms non-binding
- Check member state implementations — some have stricter local rules

## Germany

| Legislation | Official Source | Notes |
|------------|----------------|-------|
| BGB (Bürgerliches Gesetzbuch) | gesetze-im-internet.de/bgb/ | Civil Code — contract law |
| AGB-Recht (§§305-310 BGB) | gesetze-im-internet.de/bgb/__305.html | General terms and conditions rules |
| BDSG (Bundesdatenschutzgesetz) | gesetze-im-internet.de/bdsg_2018/ | Federal data protection (supplements GDPR) |
| HGB (Handelsgesetzbuch) | gesetze-im-internet.de/hgb/ | Commercial Code |
| UrhG (Urheberrechtsgesetz) | gesetze-im-internet.de/urhg/ | Copyright law |
| TMG/TTDSG | gesetze-im-internet.de/ttdsg/ | Telecoms and telemedia data protection |

**Key considerations for German contracts:**
- AGB-Recht (§§305-310 BGB): Standard terms subject to strict judicial control — many common clauses invalid under German law
- Limitation of liability: Cannot exclude liability for intent or gross negligence (§276 BGB)
- Written form requirements: Some clauses require Schriftform (wet signature) — electronic may not suffice
- Forum selection: German courts may refuse to apply foreign choice-of-law clauses for consumer contracts

## United States — Federal

| Legislation | Official Source | Notes |
|------------|----------------|-------|
| UCC (Uniform Commercial Code) | law.cornell.edu/ucc | Sale of goods, commercial transactions |
| ECPA (Electronic Communications Privacy Act) | govinfo.gov | Electronic surveillance |
| COPPA | ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule | Children's privacy |
| CAN-SPAM Act | ftc.gov/legal-library/browse/rules/can-spam-rule | Commercial email |
| Defend Trade Secrets Act | govinfo.gov | Trade secret protection |

## United States — Key States

### California
| Legislation | Official Source | Notes |
|------------|----------------|-------|
| CCPA/CPRA | oag.ca.gov/privacy/ccpa | Consumer privacy |
| Cal. Civ. Code §1798.100+ | leginfo.legislature.ca.gov | Privacy rights |

### New York
| Legislation | Official Source | Notes |
|------------|----------------|-------|
| NY General Obligations Law | nysenate.gov/legislation | Contract formation |
| NY SHIELD Act | nysenate.gov/legislation | Data breach notification |

### Delaware
| Legislation | Official Source | Notes |
|------------|----------------|-------|
| DGCL (Delaware General Corporation Law) | delcode.delaware.gov/title8/ | Corporate governance |
| Delaware Personal Data Privacy Act | legis.delaware.gov | Consumer privacy (effective 2025) |

---

## How to Use This Reference

When redlining a clause that requires a legal citation:

1. **Identify the jurisdiction** from the contract's governing law clause
2. **Find the relevant legislation** in the table above
3. **Use `deep-research` or web fetch** to retrieve the current text from the official source URL
4. **Cite the specific section/article** in the audit pack's Legal Ref column
5. **Record the source URL and retrieval date** for the audit trail

**If an official source cannot be reached**, flag the clause as `NEEDS_RESEARCH` with the note "Legislation not verified from official source — [source URL] unreachable on [date]".
