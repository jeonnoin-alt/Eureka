# Research Design: [Title]

**Date**: YYYY-MM-DD
**Researcher**: [Name or project identifier]
**Status**: DRAFT | APPROVED | REGISTERED
**Design Review**: PENDING | APPROVED | CHANGES_REQUESTED

---

## 1. Research Question

**Primary Question**: [One sentence. Answerable, specific, novel.]

**Secondary Questions** (if any):
1. ...

**Out of Scope**: [Explicitly list what this study will NOT address]

---

## 2. Background and Motivation

**Literature Gap**: [What specifically has NOT been done. With citations if available.]

**Why This Matters**: [Scientific or practical significance]

**Prior Work**: [Most relevant 3-5 papers and how this study differs from each]

---

## 3. Hypotheses

**Primary Hypothesis (H1)**: [Exact statement. Directional if applicable.]

**Null Hypothesis (H0)**: [Exact statement of what "no effect" looks like]

**Alternative Hypotheses** (if applicable):
- H1a: ...
- H1b: ...

**Falsifiability Criterion**: [What specific result would DISPROVE H1? Be exact — state the threshold, direction, or pattern that would constitute disconfirmation.]

---

## 4. Study Design

**Design Type**: [e.g., randomized controlled, observational cohort, computational simulation, case-control, cross-sectional, longitudinal]

**Unit of Analysis**: [What is one "observation"?]

**Sample / Data Source**:
- Source: [dataset name, collection method, or simulation parameters]
- Inclusion criteria: ...
- Exclusion criteria: ...
- Expected N: ...

**Key Variables**:

| Variable | Role | Measurement | Notes |
|---|---|---|---|
| [name] | Outcome | [how measured] | Primary outcome |
| [name] | Predictor | [how measured] | |
| [name] | Confounder | [how measured] | Controlled by [method] |

**Controls for Confounds**:
- [Confound 1]: Controlled by [mechanism]
- [Confound 2]: Controlled by [mechanism]
- [Confound 3]: Controlled by [mechanism]

---

## 5. Pre-Specified Analysis Plan

**Primary Outcome Measure**: [Exactly one. The measure that determines whether H1 is supported.]

**Statistical Test**: [Exact test with justification for why this test fits this data type and design]

**Effect Size Metric**: [e.g., Cohen's d, Pearson r, odds ratio, R-squared]

**Significance Threshold**: alpha = [value], corrected for [N comparisons] using [FDR / Bonferroni / none — justify]

**Sample Size Justification**:
- Expected effect size: [value, with source — prior study, pilot, or convention]
- Desired power: [e.g., 0.80]
- Required N: [from power analysis or justification if power analysis is not feasible]

**Secondary Analyses** (pre-specified):
1. [Analysis, outcome measure, test]
2. ...

**Sensitivity Analyses** (pre-specified):
1. [What parameter changes, what you expect to see]
2. ...

**Exploratory Analyses** (clearly labeled):
1. [These are NOT confirmatory — results will be reported as exploratory]

**Stopping Rules** (if applicable): [When to stop early for efficacy, futility, or safety]

---

## 6. Operationalization

**Implementation**:
- Tools/software: [names and versions]
- Code location: [path in repository]
- Data location: [path or access instructions]
- Environment: [how to set up — requirements.txt, conda env, etc.]

**Reproducibility Commitment**:
- [ ] Random seeds will be fixed and recorded for every experiment
- [ ] All configs will be saved alongside results at experiment time
- [ ] A single command can reproduce all results from raw data
- [ ] Environment specification will be committed (requirements.txt / environment.yml)

---

## 7. Limitations and Risks

**Known Limitations**:
1. ...

**Risks to Internal Validity**:
1. [Threat and mitigation]

**Risks to External Validity**:
1. [Threat and mitigation]

**Contingency Plans**:
- If [primary approach fails]: [fallback approach]
- If [sample size insufficient]: [alternative]

---

## 8. Approval

**Design Review Status**: PENDING | APPROVED
**Approved By**: [Researcher / supervisor / self]
**Approval Date**: YYYY-MM-DD

**Pre-Registration Commitment**:
- [ ] This design will be registered before data collection/analysis begins
- Registration target: [OSF / AsPredicted / version control commit / internal log]
- Registration ID (after registration): [to be filled]
