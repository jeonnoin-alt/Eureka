# Novelty Audit Guide

This is a reference document, not a skill. It provides lookup material for **pre-submission novelty competitive auditing** — search strategy by field, preemption assessment rubric, differentiation test templates, PASS/CONCERN/BLOCK decision tree, action menu for CONCERN/BLOCK verdicts, worked examples, and common anti-patterns. Referenced by `eureka:novelty-competitive-audit` at submission time and by `eureka:research-brainstorming` Step 3 at design time (same concern, different phase).

**Core premise**: editors' first desk-reject filter is "does this advance the field?" A manuscript with perfect internal rigor can still desk-reject if the field moved in the 6-12 months between design approval and submission. This guide structures a fresh literature competitive review to catch preempts before submission.

---

## 1. When to use this reference

| Phase | Skill | What to look up |
|---|---|---|
| **Design time** (pre-data) | `eureka:research-brainstorming` Step 3 | §2 (search strategy), §3 (time window) — novelty at design approval |
| **Pre-submission** | `eureka:novelty-competitive-audit` | All sections — structured audit |
| **Pre-revision / mid-revision** | `eureka:novelty-competitive-audit` | §4 (rubric), §5 (differentiation), §7 (decision tree) — re-audit after reviewer-surfaced preempt |
| **Venue change decision** | `eureka:submission-readiness` | §8 (action menu: venue change option) |
| **Stuck** (paper rigorous but novel?) | `eureka:whats-next` | §6 (worked examples), §9 (anti-patterns) |

---

## 2. Search strategy by field

| Field | Databases | Key considerations |
|---|---|---|
| **Medical / clinical** | PubMed, medRxiv, bioRxiv, Cochrane | MeSH terms + free-text; clinical trial registries (ClinicalTrials.gov) for active work |
| **Biology / life sciences** | PubMed, bioRxiv, Google Scholar | MeSH + species-specific terms; check recent meeting abstracts (SfN, Cell Symposium) |
| **Neuroscience** | PubMed, bioRxiv, NeuroImage/Brain/Neuron archives | Atlas-specific terms (Desikan-Killiany, AAL, HCP); conference proceedings (OHBM, SfN, CCN) |
| **CS / ML / AI** | arXiv (cs.LG, cs.AI, stat.ML), ACM Digital Library, IEEE Xplore, OpenReview, Papers with Code | Fast-moving field — check preprints aggressively; conference proceedings (NeurIPS, ICML, ICLR, CVPR) have 6+ month lead on journal publication |
| **Physics** | arXiv (cross-lists), PRL, PRX, Nature Physics, Physical Review | Check cross-listed categories; pre-publication competition via arXiv |
| **Chemistry** | Reaxys, SciFinder, ACS, RSC, ChemRxiv | Patent literature (USPTO, Espacenet) for applied work |
| **Social sciences / psychology** | PsycINFO, SSRN, Google Scholar, PubMed (clinical psych) | Pre-registration platforms (OSF, AsPredicted) show active parallel work |
| **Economics / finance** | SSRN, NBER, RePEc, Google Scholar | Working paper culture — many papers live on SSRN for years before journal publication |
| **Engineering** | IEEE Xplore, ACM DL, ScienceDirect, TechRxiv | Standards bodies (IEEE, IEC, ISO) track competing methods |
| **General / cross-disciplinary** | Google Scholar, Semantic Scholar, connected papers (connectedpapers.com) | Use cited-by and citing-this chains from anchor papers |

**Rule of thumb by field velocity:**

- Fast-moving fields (ML, genomics, CS): weight preprints heavily; time window may narrow to 6-12 months of most-recent preprints
- Slow-moving fields (classical physics, some areas of math): time window may extend to 3-5 years
- Hype-cycle fields (LLMs 2023+, topological materials, etc.): check weekly preprint digests, not just archival search

---

## 3. Time window guidance

**Default**: 2 years from the manuscript submission date.

**Adjust upward (3-5 years)** when:
- Field moves slowly (classical areas, mature methodology)
- The research uses a niche method where few papers appear per year
- Preprint culture weak in the field

**Adjust downward (6-12 months)** when:
- Field is in hype cycle (fast-moving, competitive)
- Multiple major labs known to work on the question
- Recent major methodology shift (new architecture, new dataset, new platform) made prior work obsolete

**Never less than 6 months** — even in fast fields, 6 months of lookback is needed to catch preprints that may have appeared in the last 6 weeks of manuscript preparation.

**Record the chosen window and justification in the search log.** The reviewer subagent will verify.

---

## 4. Preemption assessment rubric

For each candidate paper, evaluate along 4 dimensions:

| Dimension | High overlap | Partial overlap | Low overlap |
|---|---|---|---|
| **Primary claim** | Same effect / conclusion claimed (e.g., "X causes Y") | Related variable or narrower/broader claim (e.g., "X correlates with Y' under condition Z") | Different question entirely (e.g., "X's prevalence", "mechanism of Y" — not the effect itself) |
| **Method** | Same approach (same algorithm / study design / model class) | Related but meaningfully different (same family but different specifics) | Orthogonal approach |
| **Data / population** | Same dataset or cohort | Similar population / different sample (same disease + different cohort; same task + different benchmark) | Different (different disease, different species, different domain) |
| **Date** | Published / preprinted AFTER your registration date | Around your registration time (±3 months) | Before your registration date |

**Flagging rule:**
- **3+ dimensions at "high"** → high-overlap candidate, requires differentiation test (§5) and may trigger CONCERN or BLOCK
- **2 dimensions at "high"** → partial-overlap candidate, should be cited + discussed in manuscript, Advisory severity
- **≤1 dimension at "high"** → low-overlap, note for completeness but no action required

**Example flags in context:**

- Primary claim = high, method = high, data = high, date = after registration → **strong preempt**, BLOCK likely
- Primary claim = high, method = partial, data = low, date = after registration → **narrowed preempt**, CONCERN (narrow claim or reframe)
- Primary claim = partial, method = high, data = high, date = around registration → **concurrent work**, cite and discuss; PASS possible if manuscript adds distinct angle
- Primary claim = low, method = high, data = high, date = after registration → **method overlap only**, PASS (different question)

---

## 5. Differentiation test

For each high-overlap candidate, write a substantive differentiation statement. The bar: a reader should understand **exactly** how the current paper differs and why that matters.

### Bad (desk-reject risk)

> "Ours is different because we focus on X."

*Problem*: restates scope without explaining how the approach, data, or findings differ. Editors and reviewers read this as evasion.

> "We use a larger sample."

*Problem*: sample-size-only differentiation. States an existence claim about the difference but doesn't connect it to a finding that's enabled by the larger sample.

> "Our method is more principled."

*Problem*: vague adjective. "Principled" relative to what specific limitation?

### Good (substantive)

> "They used **approach A** on **dataset D1** and reported **result R1** under **assumption X**. We used **approach B** on **dataset D2**, which **resolves limitation L (specific to X)** and enables **finding F** not accessible to their approach because F requires **capability C** that A lacks."

*Why this works*: names the specific method, dataset, limitation, and enabled finding. A reviewer can verify each claim.

### Template

```
They [approach A] on [dataset D1] reporting [result R1].

We [approach B] on [dataset D2], which:
- Resolves [specific limitation L] present in their approach
- Enables [finding F] that [approach A] cannot access because [reason]

Therefore, our contribution [specific contribution C] is distinct from theirs at the [mechanism / evidence / scope] level.
```

### Worked example — good differentiation (abstract)

> [Preempt 2024] used [method A] on [single dataset D1, N=326] to establish [relationship R, with moderate accuracy r=0.57]. We use [method B — a more expressive model class] on [the same D1 (N=749) combined with independent dataset D2 (N=1662) for transfer validation], achieving [stronger accuracy r=0.88 on D1 and r=0.89 on D2] — the first cross-cohort generalization in this model class. This resolves the "model fit without generalization" limitation of [Preempt 2024] and enables [downstream application X] that their single-cohort accuracy does not support.

*Why this works*: specific citation, specific sample sizes, specific result comparison, specific limitation named, specific downstream implication enabled by the difference.

---

## 6. Worked preemption examples

### Example 1 — BLOCK → narrowed CONCERN → PASS

**Situation**: manuscript claims "model M achieves state-of-the-art on task T using new architecture A."

**Preempt found**: paper published 4 months ago claims same SOTA on task T with architecture A' (same family as A).

**Rubric**: primary claim = high, method = high, data = high, date = after registration. 4 high → strong preempt.

**Bad response (desk-reject risk)**: "Ours is different because architecture A vs A'." → hand-waved. Editor reads this as "essentially the same work."

**Good response (narrow → CONCERN → PASS)**:
- Narrow claim from "SOTA on task T" to "SOTA on task T under low-resource regime (< 1000 training examples), where A's inductive bias matters"
- Add their paper as primary comparison, report their numbers and yours side by side
- Re-fire `manuscript-writing` Step 3 narrative-arc lock: altitude drops from "new framework for task T" to "method improvement under specific conditions"
- Re-run novelty audit: the narrowed claim is novel; PASS

### Example 2 — BLOCK → venue change → PASS

**Situation**: manuscript claims "new phenomenon: effect E in system S."

**Preempt found**: Nature paper 6 months ago demonstrated effect E in system S with robust replication.

**Rubric**: primary claim = high, method = high, data = high (same system), date = after registration. BLOCK — they own the phenomenon claim at Nature-family altitude.

**Options**:
- (a) Narrow: E under specific condition C not explored in preempt — but if preempt tested C, narrowing fails
- (b) **Venue change**: submit to specialty venue where the independent replication value is the contribution ("confirmatory replication of E in S, extending to sample population P")
- (c) Expand evidence: add mechanistic dimension (preempt was observational; add causal manipulation)
- (d) Abandon

**Good response**: choose (b) venue change. Reframe from "novel phenomenon" to "independent confirmation + population extension" for a confirmatory-replication-friendly specialty venue.

### Example 3 — partial overlap → pre-emptive citation → PASS

**Situation**: manuscript claims "X predicts Y using method M."

**Preempt found**: paper published 3 months ago using method M' (different family) on similar data, reports X predicts Y with different accuracy.

**Rubric**: primary claim = high, method = low (different family), data = partial. 1 high, 1 partial → partial-overlap candidate.

**Good response**: no verdict block. Cite and discuss: "Recent work (Preempt 2025) showed X predicts Y using M'; our approach using M achieves [different result] and reveals [additional aspect] that their approach could not capture because [reason]." Novelty audit verdict PASS with Advisory (add citation).

---

## 7. PASS / CONCERN / BLOCK decision tree

```
START: For each high-overlap candidate (3+ dimensions at "high"), run differentiation test.

├── No high-overlap candidates found in time window
│   └── Check partial-overlap candidates are cited → PASS

├── High-overlap candidate(s) found, all pass differentiation test
│   ├── Altitude still defensible → PASS (with Advisory to cite preempts)
│   └── Altitude needs narrowing → CONCERN (narrow + re-fire Step 3)

├── High-overlap candidate(s) found, at least one fails differentiation
│   ├── Can narrow to sub-question still novel → CONCERN (narrow claim)
│   ├── Can change venue where claim is original → CONCERN (venue change)
│   ├── Can expand evidence to re-establish novelty → CONCERN (add evidence before submission)
│   └── None of above feasible → BLOCK

└── Red-team search by reviewer finds additional high-overlap preempt
    └── Re-run from "differentiation test" with new candidate
```

**Verdict documentation**: every verdict must state which rule fired and which action was chosen.

---

## 8. Action menu for CONCERN / BLOCK

### Narrow claim

Retreat from the broader claim to a narrower sub-question that remains novel.

- Example: "SOTA on task T" → "SOTA on task T under low-resource regime"
- Example: "X causes Y" → "X causes Y under condition C not tested in preempt"
- Bar: the narrowed claim must be **substantively different**, not just verbose

### Venue change

Submit to a venue where the current claim is still original at that venue's altitude expectations.

- Example: preempt is at Nature → submit to specialty journal where confirmatory replication is valued
- Example: preempt is at high-altitude venue → submit to mechanism-focused venue that values causal extension
- See `docs/references/narrative-guide.md` section "Venue-specific altitude tuning" for venue altitude mapping

### Expand evidence

Add dataset, analysis, or mechanism that re-establishes novelty.

- Example: preempt was observational → add causal manipulation
- Example: preempt was single-cohort → add independent cohort transfer
- Example: preempt was single-time-point → add longitudinal
- Bar: the added evidence must be collectable in reasonable time and must substantively change the contribution

### Re-frame altitude

Drop contribution altitude to match post-audit evidence landscape. Re-fire `manuscript-writing` Step 3 narrative-arc lock.

- Example: "new phenomenon" → "method improvement under specific conditions"
- Example: "new framework" → "framework validation in extended domain"
- See `narrative-guide.md` section "Contribution altitude — 4 tiers"

### Abandon

Archive per `submission-readiness` Option 4. **Not a failure** — negative evidence (the preempt) is still evidence; the work informs the field even unpublished.

- Example: preempt fully covers the claim at target altitude, no feasible expansion, no alternative venue
- Action: document what was learned, archive code and data for future work

---

## 9. Common anti-patterns

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| **Biased search terms** | Only keywords that favor the framing; avoids terminology the field uses for competing work | Search the field's terminology, including competitors' phrasings |
| **Silent preprint exclusion** | Search log lists only peer-reviewed venues | Always include preprints (bioRxiv, medRxiv, arXiv, SSRN, OSF) in search |
| **Cherry-picked candidates** | Only candidates that are easy to differentiate from | Record all hits, then evaluate with rubric — let the rubric filter, not your judgment |
| **Hand-waved differentiation** | "Ours is different because we focus on X" without method/data/finding specificity | Use the good-template in §5 |
| **Sample-size-only differentiation** | "Our N is bigger" as sole novelty claim | State what the larger sample **enables scientifically** — subgroup analysis? Power to detect interaction? Rare-event detection? |
| **Citation-count appeal** | "We have more citations" as novelty argument | Citations describe reception, not novelty. State what your contribution adds that existing citations don't |
| **Combination-novelty without specificity** | "Novelty is the combination of X, Y, Z" | State why the combination enables a specific finding none of X, Y, Z alone could reach |
| **BLOCK → CONCERN rationalization** | Downgrading verdict to avoid rework | Reviewer subagent will flag — trust the rubric, not the inconvenience |
| **"I know the field"** | Skipping structured search | The search log is evidence of honest audit; omitting it is itself a red flag |
| **No red-team search** | Author's own search treated as complete | Reviewer subagent runs red-team mode independently; the author should also attempt to find preempts from a competing lab's perspective before dispatch |

---

## 10. Search log template

For reviewer verification, record the audit in structured form at `docs/eureka/novelty-audit/YYYY-MM-DD-search-log.md`:

```markdown
# Novelty Audit Search Log — YYYY-MM-DD

## Manuscript
- Path: paper/main.tex
- Target venue: [venue name]
- Claimed contribution altitude: [method improvement / new framework / new phenomenon / falsification]

## Headline claims extracted
1. [Claim 1]
2. [Claim 2]
3. [Claim 3]

## Search strategy
- Time window: [X years], justification: [...]
- Databases: [list]
- Keyword queries: [list with approximate hit counts]
- Competitor author-name queries: [list]
- Conference proceedings scanned: [list]
- Preprint servers: [list]

## Candidate list (top 5-15)
| # | Citation | Year | Venue | One-sentence claim |
|---|---|---|---|---|
| 1 | [author year] | ... | ... | ... |

## Per-candidate rubric evaluation
### Candidate 1: [short ID]
- Primary claim: [high/partial/low — reasoning]
- Method: [...]
- Data: [...]
- Date: [...]
- Overall: [high-overlap / partial / low]

### Candidate 2: ...

## Differentiation statements (for high-overlap candidates)
### Candidate 1
> [Substantive differentiation per §5 template]

## Altitude recheck
- Original altitude claim: [...]
- Post-audit altitude defensible: [yes / no]
- If no, proposed re-frame: [...]

## Verdict
- Verdict: [PASS / CONCERN / BLOCK]
- Rule fired: [...]
- Action (if CONCERN/BLOCK): [...]
- Re-audit required after action: [yes / no]
```

---

## 11. Further reading

**On editorial rejection and novelty:**

- Nature editorial criteria: [https://www.nature.com/nature/for-authors/editorial-criteria-and-processes](https://www.nature.com/nature/for-authors/editorial-criteria-and-processes)
- eLife "reviewed preprints" model commentary: [https://elifesciences.org/inside-elife](https://elifesciences.org/inside-elife)
- Nature Communications desk-rejection patterns
- Retraction Watch (commentary on post-publication preempt discovery)
- "Why papers get rejected": editorials in Science, Cell, JAMA archives

**On literature search methodology:**

- Grindlay, D. J. et al. (2012). *Searching the literature: tools and techniques*. BMJ — general methodology
- PRISMA-S checklist for systematic search reporting (applies at higher rigor, but the principles transfer to novelty audit)
- Connected Papers ([connectedpapers.com](https://www.connectedpapers.com/)) — visual citation network tool for discovering adjacent work
- Research Rabbit ([researchrabbitapp.com](https://www.researchrabbitapp.com/)) — interactive citation exploration

**On contribution altitude matching to venue:**

- `docs/references/narrative-guide.md` section "Venue-specific altitude tuning" — this guide's sibling reference
- Schimel, J. *Writing Science* (Oxford, 2012) — ABT structure and venue-appropriate framing
