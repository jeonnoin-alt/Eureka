# Data Reference Guide

This is a reference document, not a skill. It provides lookup tables for data provenance, preprocessing requirements, leakage taxonomy, missing value handling, split strategy, and descriptive statistics. Referenced by `eureka:research-brainstorming`, `eureka:hypothesis-first`, `eureka:experiment-design`, `eureka:systematic-troubleshooting`, and `eureka:verification-before-publication`.

---

## 1. Data Provenance Template

Every dataset used in a study must have all of these fields documented before analysis begins:

| Field | Example | Why it matters |
|---|---|---|
| **Source** | Public registry, institutional cohort, `datasets/my_lab_acquisition_2024` | Reviewers must be able to identify the dataset |
| **Version** | Cohort release 2024-03-15, or file SHA `a1b2c3d4...` | Same dataset name can differ across releases |
| **Access method** | DUA + approved application, public download URL, internal path | Reproduction requires this path |
| **Acquisition date** | Downloaded 2026-02-11 | Datasets drift; snapshot date matters |
| **License / DUA** | DUA v3, CC-BY-4.0, internal-only | Legal and attribution constraints |
| **Raw vs processed** | Raw DICOMs, or `preprocessing_v2.4.0` output | Preprocessing state changes downstream results |
| **File hashes** | SHA256 of each key input file | Detect silent data changes |

Record these in the research design document and again in the hypothesis registration.

---

## 2. Preprocessing Pipeline Requirements

A preprocessing pipeline must satisfy ALL of these conditions to qualify as reproducible:

- [ ] Exists as a script (bash, Python, Snakemake, Nextflow, etc.) — no manual GUI steps
- [ ] Input paths and output paths are explicit in the script or config
- [ ] Has a version tag (git commit hash, release tag, or semantic version)
- [ ] Is deterministic: same input + same seed → same output, bit-for-bit where feasible
- [ ] Has a README documenting how to run it end-to-end with a single command
- [ ] External dependencies (FSL, FreeSurfer, ANTs, etc.) have versions pinned
- [ ] Environment is specified (conda env, Docker, requirements.txt)

**If any box is unchecked, the preprocessing is NOT reproducible.** Results derived from it cannot be verified by anyone else — including future-you.

---

## 3. Data Leakage Taxonomy

Data leakage is the silent killer of research results. Most leakage is discovered too late, after claims are made. Check every type before claiming a result.

| Leakage type | Definition | Example | Prevention |
|---|---|---|---|
| **Temporal** | Future information used to predict past/present | Using subject's t+1 scan to predict t outcome | Time-based split; strict cutoff for features |
| **Group / Subject** | Same subject appears in both train and test | Split by scan instead of by subject; siblings in both sets | Subject-level (or family-level) split |
| **Feature** | Target-derived or target-adjacent feature | Using diagnosis code as a feature for diagnosis prediction | Audit every feature's origin |
| **Preprocessing** | Transformation fit on full data before split | `StandardScaler().fit_transform(X_all)` then split | Fit on train only, transform test |
| **Label** | Proxy for label encoded in features | Including "date of diagnosis" when predicting diagnosis | Feature provenance review |
| **Duplication** | Near-duplicates across splits | Same scan acquired twice; augmented copies in both splits | Deduplicate by content hash |
| **Target encoding** | Encoding categorical features using target statistics on full data | Target mean encoding fit on all | Fit encoding only on train folds |
| **Hyperparameter** | Tuning hyperparameters on the test set | Selecting best model using test performance | Held-out validation set, separate from test |

**Detection strategies:**
- Run model with shuffled labels — if performance remains high, leakage exists
- Train on random subset, test on the rest — if performance matches your main result with an "easy" split, suspect leakage
- Inspect highest-importance features — any of them correlated with the target by construction?

---

## 4. Missing Value Decision Tree

Choose the handling method BEFORE running the analysis. Post-hoc selection inflates Type I error.

### Step 1: Classify the missingness

| Type | Meaning | Detection | Example |
|---|---|---|---|
| **MCAR** (Missing Completely At Random) | Missingness unrelated to any variable | Little's MCAR test | Random equipment failure |
| **MAR** (Missing At Random) | Missingness explained by observed variables | Logistic regression of missingness on observed | Older subjects miss follow-ups more often, but within age groups missing is random |
| **MNAR** (Missing Not At Random) | Missingness related to the unobserved value itself | Cannot be tested directly — requires domain reasoning | Patients with worse outcomes drop out of follow-up |

### Step 2: Choose handling method

| Method | When appropriate | When NOT appropriate |
|---|---|---|
| **Listwise deletion** | MCAR, loss of power acceptable (< 5% missing) | MAR/MNAR (biased), high missingness (loses power) |
| **Mean/median imputation** | Quick exploratory only | Any confirmatory analysis — underestimates variance |
| **Multiple imputation (MICE)** | MAR, continuous or mixed data, multiple variables missing | MNAR (still biased) |
| **Model-based (EM, full likelihood)** | MAR with a well-specified model | Model misspecification |
| **Inverse probability weighting** | MAR with a model of missingness | Unreliable weights, small samples |
| **Sensitivity analysis with MNAR assumptions** | When MNAR is suspected | — (always reasonable as a robustness check) |

### Step 3: Lock it before seeing results

The missing value handling method is part of the pre-analysis plan. Swapping methods after seeing results is p-hacking.

---

## 5. Data Split Best Practices

### Split types

| Split type | Use when | Key rule |
|---|---|---|
| **Random** | IID samples, no grouping | Rarely appropriate in real data |
| **Stratified** | Classification, imbalanced classes | Preserve label distribution across splits |
| **Subject-level (grouped)** | Multiple samples per subject | All samples of one subject must be in one split |
| **Time-based** | Longitudinal or time-series data | Train on past, test on future |
| **Site-based** | Multi-site studies, generalization test | Hold out an entire site |
| **Nested CV** | Hyperparameter tuning + unbiased estimate | Outer CV for test, inner CV for hyperparameter selection |

### The held-out principle

Your test set must be touched ONCE, at the very end, after all model selection, hyperparameter tuning, and debugging are done.

If you:
- Check test performance during development → the test set is now validation, not test
- Tune based on test metrics → inflated performance, guaranteed
- "Sneak a peek" at test once → the sneak counts

**Test set is for confirmation, not iteration.** If you must iterate, keep a separate held-out test set you will not touch until submission.

---

## 6. Descriptive Statistics Template (Table 1)

Every paper should have a "Table 1" characterizing the study sample. Required fields:

| Field | Example |
|---|---|
| N per group | Control: 47, MCI: 62, AD: 34 |
| Age (mean ± SD, range) | 72.3 ± 6.8 (58–89) |
| Sex (M/F count and %) | M: 73 (52%), F: 70 (48%) |
| Key demographics | Education years, APOE status, handedness, etc. |
| Primary outcome baseline | MMSE: 27.4 ± 2.1 |
| Inclusion/exclusion applied | "Excluded: 12 subjects for motion > 3mm" |
| Missingness rate per variable | Biomarker A: 4% missing; Cognition: 0% missing |
| Outliers | 2 subjects flagged by IQR > 3, retained / excluded per pre-spec |
| Group differences at baseline | t/chi-square tests of balance |

Generate this table programmatically from the exact data file used in the analysis — not hand-typed.

---

## 7. Data Version Locking (for hypothesis registration)

At the moment of hypothesis registration, the data must be frozen. Record:

1. **Dataset version tag**: `cohort_v2.4.0-2024-03-15` or equivalent
2. **File hash(es)**: SHA256 of every input file the analysis will read
3. **Preprocessing pipeline version**: git commit hash of the preprocessing script/repo
4. **Inclusion/exclusion applied snapshot**: the actual list of subjects that will be analyzed
5. **Missing value handling policy**: chosen method (see Section 4)

Commit all of the above to version control alongside the hypothesis registration. The data is now locked. If the data changes after this point, the registration is invalidated and a new one must be created.

---

## Quick Integration Map

| Question | Which skill enforces |
|---|---|
| "Where does this data come from?" | research-brainstorming (design) |
| "Is the data version locked?" | hypothesis-first (REGISTER) |
| "What files does this experiment read?" | experiment-design (Inputs with version) |
| "Why is this result unexpected?" | systematic-troubleshooting (Phase 1 data checks) |
| "Can the data pipeline be reproduced?" | verification-before-publication (reproducibility sub-check) |
