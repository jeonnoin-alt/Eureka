# Registration Lifecycle Guide

This is a reference document, not a skill. It covers the **full lifecycle of a hypothesis registration** — from initial registration through amendment, supersession, archival — plus the HARKing severity spectrum and the data-discovery-feedback workflow. Referenced by `eureka:hypothesis-first` (for registration creation and upkeep), `eureka:research-brainstorming` (when pivoting requires a new registration), `eureka:experiment-design` (for plan↔registration contingency inheritance), and `agents/research-reviewer.md` (for HARKing detection in D3/D4).

**Core premise**: pre-registration is not static. Projects discover that their assumptions were wrong, that their samples came out different, that the data has features that were not anticipated. The naive interpretation — "a registration is immutable, so any deviation is HARKing" — is wrong and harmful: it pushes researchers to hide deviations rather than document them. The mature interpretation — "registrations have a lifecycle, deviations are either acceptable amendments or explicit supersessions, and silent modification is HARKing" — is what this guide formalizes.

---

## 1. When to use this reference

| Situation | What to look up |
|---|---|
| Writing a new registration | §4 (YAML frontmatter), §5 (filename convention) |
| Observed data violates registration assumption | §8 (data-discovery feedback workflow) |
| Want to revise a registration after partial execution | §3 (amendment vs supersede decision tree) |
| Pivoting study direction | §3 (supersede path), §6 (INDEX.md upkeep) |
| Confused which registration is authoritative | §6 (INDEX.md) |
| Planning new experiments | §9 (plan ↔ registration contingency inheritance) |
| Reviewing for HARKing concerns | §7 (HARKing severity spectrum) |

---

## 2. Registration lifecycle states

A registration is always in one of four mutually-exclusive states:

| State | Meaning | Can execute analyses from? |
|---|---|---|
| **active** | Current, authoritative registration | Yes |
| **amended-by: <id>** | Original still authoritative, but an amendment file adds/refines content | Yes (read both parent and amendment) |
| **superseded-by: <id>** | Superseded by a new registration; do not execute from this one | No (read the new one) |
| **archived** | Study abandoned; kept for record but not active research | No |

State transitions (forward-only, auditable):

```
active → amended-by (one or more times)
active → superseded-by
active → archived
amended-by → superseded-by (the chain continues with the new parent)
```

**Rule**: state changes are recorded in YAML frontmatter (§4) and reflected in `docs/eureka/registrations/INDEX.md` (§6). Silent state changes are HARKing-equivalent.

---

## 3. Decision tree: amendment vs supersede vs new registration

When the study needs to evolve, choose the right path:

```
Has the HYPOTHESIS changed?
├── No, only operational detail / observation-noted
│   └── Amendment (same registration ID, new amendment file)
│
├── Yes, but on the same dataset and research question
│   └── Supersede (new registration file, mark old as superseded-by)
│
└── Yes, and the new direction is a different research question entirely
    └── New registration (independent, not in a supersede chain)
```

### Worked examples

**Example 1 — Amendment**: "We planned to analyze T+ prevalence assuming 50%. Observed data showed 34%. Hypothesis (AUC improvement over baseline) unchanged, but the power analysis and stratum sizes need to reflect the observed prevalence."

- Decision: **amendment**
- Create `docs/eureka/registrations/2026-04-25-<topic>-amendment-001.md`
- Parent registration stays `active` but gains `amended-by: <amendment-id>` in frontmatter
- Amendment file: documents the observed prevalence, the updated power calculation, and confirms hypothesis unchanged

**Example 2 — Supersede**: "Our original registration planned cross-sectional analysis at N=300. After collection, we have only N=182 but discovered longitudinal data. Pivot to longitudinal design with different primary outcome."

- Decision: **supersede**
- Create `docs/eureka/registrations/2026-05-01-<topic>-registration.md` (new ID, new file)
- Old registration marked `status: superseded-by: 2026-05-01-...`
- New registration's frontmatter: `supersedes: 2026-04-17-<topic>-v1`
- Old registration stays in the repo for record; is no longer authoritative

**Example 3 — New registration**: "Our lab has been working on Disease A. We're starting a new independent study on Disease B using different cohorts, methods, and hypothesis."

- Decision: **new registration** (not in a supersede chain)
- Create `docs/eureka/registrations/2026-05-10-disease-b-registration.md` with `status: active` and no `supersedes` or `parent` field

### Do NOT

- Silently edit an existing registration file to "match" observed data — this is HARKing
- Create a new registration and delete the old — breaks chain of custody
- Fork a registration into two "active" versions — exactly one can be active at a time

---

## 4. YAML frontmatter schema

Every registration file (original, amendment, or supersession) starts with machine-readable frontmatter. Example:

```yaml
---
registration_id: 2026-05-01-biomarker-auc-v2
status: active
# OR: status: amended-by: 2026-05-15-biomarker-auc-amendment-001
# OR: status: superseded-by: 2026-06-10-biomarker-auc-v3
# OR: status: archived

# Lineage (mutually-exclusive, set at most one):
supersedes: 2026-04-17-biomarker-auc-v1    # this is a supersede; points to what it replaces
# parent: 2026-04-17-biomarker-auc-v1      # this is an amendment; points to registration it amends

created: 2026-05-01
last_modified: 2026-05-15
target_venue: <journal-name>               # optional; updates if target shifts
---
```

### Field definitions

| Field | Required | Format | Meaning |
|---|---|---|---|
| `registration_id` | Yes | `YYYY-MM-DD-<topic>-<version>` | Globally unique ID for this file |
| `status` | Yes | `active` \| `amended-by: <id>` \| `superseded-by: <id>` \| `archived` | Current state |
| `supersedes` | If supersession | registration_id | What this registration replaces |
| `parent` | If amendment | registration_id | Which registration this amendment refines |
| `created` | Yes | `YYYY-MM-DD` | Initial creation date |
| `last_modified` | Yes | `YYYY-MM-DD` | Most recent modification date |
| `target_venue` | Optional | string | Current target venue (updates trigger `narrative-guide.md` Step 3 re-fire and possibly novelty-audit re-run) |

### Mutual-exclusion rules

- `supersedes` XOR `parent` — a registration is either a supersession or an amendment, not both
- `status: active` is incompatible with being a supersession target or an amendment's parent being active — the system should reflect exactly one authoritative path

---

## 5. Filename convention

| Type | Filename format | Example |
|---|---|---|
| Original registration | `YYYY-MM-DD-<topic>-registration.md` | `2026-04-17-biomarker-auc-registration.md` |
| Versioned registration (post-supersede) | `YYYY-MM-DD-<topic>-v<N>-registration.md` | `2026-05-01-biomarker-auc-v2-registration.md` |
| Amendment | `YYYY-MM-DD-<topic>-amendment-<NNN>.md` | `2026-05-15-biomarker-auc-amendment-001.md` |

All live in `docs/eureka/registrations/`.

---

## 6. `docs/eureka/registrations/INDEX.md`

Machine-generated (or machine-maintained by `hypothesis-first`) index of all registrations with their lifecycle states. Without this, 3 months after a pivot, no one knows which registration is authoritative.

**Starter template**: Eureka ships `docs/templates/registrations-index-template.md` as a seed file. Copy it to `docs/eureka/registrations/INDEX.md` in your project repo when you first register a hypothesis via `hypothesis-first`. The skill will maintain it thereafter.

### Template

```markdown
# Registrations INDEX

Last updated: YYYY-MM-DD

| Registration ID | Status | Lineage |
|---|---|---|
| 2026-04-17-biomarker-auc-v1 | superseded-by: 2026-05-01-biomarker-auc-v2 | — |
| 2026-05-01-biomarker-auc-v2 | amended-by: 2026-05-15-biomarker-auc-amendment-001 | supersedes: 2026-04-17-biomarker-auc-v1 |
| 2026-05-15-biomarker-auc-amendment-001 | active (amendment) | parent: 2026-05-01-biomarker-auc-v2 |
| 2026-05-10-disease-b-v1 | active | — |

## Active registrations summary

- **biomarker-auc**: latest is v2 (with amendment-001). Original v1 superseded 2026-05-01.
- **disease-b**: v1 active since 2026-05-10.
```

### Upkeep

`hypothesis-first` SKILL.md is the source of truth for INDEX.md. Each time a registration is created, amended, or superseded, `hypothesis-first` regenerates the INDEX entry for the affected chain.

---

## 7. HARKing severity spectrum

"HARKing" (Hypothesizing After Results are Known) is not binary. There is a spectrum from benign observation-noting to outright fraud. The spectrum matters because treating every deviation as equally severe pushes researchers to hide deviations; treating none as severe is the same problem from the other side.

| Tier | Example | Severity | Disclosure required? | HARKing? |
|---|---|---|---|---|
| 1. Observation-noted | "We assumed T+ prevalence 50%; observed 34%" (hypothesis unchanged) | **No concern** | Yes (amendment) | No |
| 2. Pre-planned exploratory | "We pre-specified X as primary; Y, Z as secondary exploratory" — and Y turned out interesting | **No concern** | Report Y as exploratory, not confirmatory | No |
| 3. Post-hoc subgroup | Ran a subgroup analysis not in registration because the main effect was suggestive | **Acceptable with disclosure** | Clearly label as post-hoc in Results + Discussion | Soft — acceptable only with honest labeling |
| 4. Post-hoc statistical test change | Changed the test (e.g., parametric → non-parametric) because the pre-registered one gave a null | **Concern — disclose or treat as exploratory** | Must disclose both test results (pre-registered and post-hoc) | Moderate — the pre-registered test's null result must be reported |
| 5. Post-hoc hypothesis change | Saw the results, invented a hypothesis that fits the observed direction, reported as confirmatory | **CRITICAL** | Effectively impossible to disclose while retaining confirmatory claim | **Yes — hard HARKing** |
| 6. Silent registration edit | Modified the registration file after seeing results, without an amendment trail | **CRITICAL** | — | **Yes — fraud-adjacent** |

### How this feeds into `research-reviewer` (D3, D4)

- Tier 1-2: no deduction
- Tier 3: -5 to -10 if disclosure is incomplete (D3.1 Pre-specification compliance)
- Tier 4: -10 to -20 if both tests not disclosed
- Tier 5: **-30 CRITICAL** deduction (D3.1) — HARKing detected
- Tier 6: **-40 CRITICAL** + recommend submission blocked until resolved

Researchers should proactively label Tier 3-4 deviations in their Methods + Results; this prevents a reviewer from discovering the deviation and escalating the severity in their own read.

---

## 8. Data-discovery feedback workflow

When the observed data violates a pre-registration assumption (observed prevalence ≠ assumed; observed effect ≠ expected; observed distribution ≠ assumed), follow this decision tree:

```
Does the observed value invalidate the HYPOTHESIS (not just the analysis plan)?

├── No, hypothesis still testable with the observed data
│   ├── Was the assumption integral to the analysis plan?
│   │   ├── Yes — create amendment updating analysis plan (e.g., power recalculation)
│   │   └── No — note the observation in Methods + Results, no formal amendment needed
│   └── Proceed with analysis
│
└── Yes, the observation makes the hypothesis untestable or the pre-specified test invalid
    ├── Can a related hypothesis be tested with the available data?
    │   ├── Yes — SUPERSEDE with new hypothesis
    │   └── No — ARCHIVE (and consider reporting the null as a methods-failure paper)
```

### Worked example — data discovery → amendment

Registration assumed: "T+ prevalence = 50%, N=300 provides 80% power to detect AUC improvement of 0.05."

Observation: T+ prevalence = 34%.

Analysis:
- Hypothesis (AUC improvement of 0.05 over baseline) unchanged — testable at 34% prevalence
- Analysis plan: power recalculation needed (actual N of T+ = 102, not 150)
- Power at observed prevalence may be lower (e.g., 65% instead of 80%)

Action: **amendment**
- Create `2026-05-01-<topic>-amendment-001.md`
- Documents: observed T+ = 34%, revised power calc, stratum sizes, any analysis-plan adjustments
- Parent registration `status: amended-by: 2026-05-01-...`
- Research-reviewer D3.1 will not deduct for this deviation because it was honestly disclosed via amendment

### Worked example — data discovery → supersede

Registration assumed: "Longitudinal scans at 6, 12, 18, 24 months available for N=300."

Observation: Longitudinal scans ≥ 12 months available for only N=182. Original primary outcome (rate of change over 24 months) is not measurable for the full cohort.

Analysis:
- Original hypothesis requires 24-month data; not available
- Related hypothesis (cross-sectional association) is testable
- But this is a different research question, not an analysis-plan tweak

Action: **supersede**
- New registration with cross-sectional hypothesis
- Original registration `status: superseded-by: <new-id>`
- New registration documents why the supersession occurred (the data reality)

---

## 9. Plan ↔ Registration contingency inheritance rules

`experiment-design` skill builds execution plans that inherit contingencies from the registration. The rules:

| Scenario | Action |
|---|---|
| Plan contingency **matches** registration contingency | ✓ PASS |
| Plan adds **new operational contingency** not in registration (e.g., "restart if GPU OOM") | ✓ PASS (task-level detail, not scientific contingency) |
| Plan contingency is **stricter** than registration (e.g., registration says "proceed as pilot if N<300", plan says "halt if N<300") | ✗ FAIL — plan is overriding registration. Either fix plan to match, OR create registration amendment with stricter contingency |
| Plan contingency is **weaker** than registration (e.g., registration says "halt if N<300", plan says "proceed regardless") | ✗ FAIL — plan is weakening registration's safety rule. Fix plan to match (no amendment path — weakening requires research-brainstorming → new registration) |
| Plan **omits** a registration contingency | ✗ FAIL — silent override. Add it to the plan |

`experiment-plan-reviewer` (the subagent prompt at `skills/experiment-design/experiment-plan-reviewer-prompt.md`) flags contingency-inheritance violations as Must-fix.

---

## 10. Anti-patterns

| Anti-pattern | Description | Fix |
|---|---|---|
| **Silent amendment** | Editing a registration file to "reflect observed data" without creating an amendment file and updating frontmatter | Create proper amendment file with YAML frontmatter; never in-place edit |
| **Dual-live** | Two registration files both in `status: active` state for the same study (fork) | Archive or supersede one. Exactly one active at a time per study |
| **Lost-INDEX** | INDEX.md missing or out-of-date, so chain is not machine-readable | Regenerate INDEX each time hypothesis-first creates/amends/supersedes |
| **Status-field drift** | Frontmatter says `active` but prose says "this has been superseded" | Frontmatter is source of truth; fix the frontmatter + INDEX |
| **Invisible pivot** | Researcher starts executing a new analysis plan without any registration change | Before the pivot, either amendment or supersede; analysis without registration = HARKing |
| **Delete-and-rewrite** | Old registration deleted; new one created as if the old never existed | Mark old as superseded; never delete for reproducibility |
| **Amendment as hypothesis change** | Amendment file actually changes the hypothesis (not just operational details) | Should be a supersede, not an amendment |

---

## 11. Further reading

- OSF (Open Science Framework) registration conventions: [osf.io/prereg](https://osf.io/prereg)
- AsPredicted registration platform: [aspredicted.org](https://aspredicted.org)
- Nosek, B. A. et al. (2018). *The preregistration revolution*. PNAS
- Hardwicke, T. E. & Ioannidis, J. P. A. (2018). *Mapping the universe of registered reports*. Nature Human Behaviour
- Center for Open Science: [cos.io/prereg](https://www.cos.io/initiatives/prereg)
- Registered Reports model (Chambers): [https://www.cos.io/initiatives/registered-reports](https://www.cos.io/initiatives/registered-reports)
