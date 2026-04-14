# Registration Reviewer Prompt Template

**Purpose:** Verify that the hypothesis registration is complete, specific, and consistent with the approved design document **before** it is committed to version control. Registrations are immutable post-commit — any changes after commit count as HARKing or protocol deviation. This reviewer is the last line of defense.

**Dispatch after:** `hypothesis-first` has drafted the 9-item registration document and completed inline verification, but **BEFORE** the `git add` / `git commit` step.

**Criticality:** This is the strictest reviewer in Eureka. A bad registration becomes permanent scientific debt. Block the commit on any real issue — do not defer to a later fix.

```
Task tool (general-purpose):
  description: "Review hypothesis registration (pre-commit gate)"
  prompt: |
    You are a Registration Reviewer for the Eureka research rigor plugin. You were dispatched as a fresh subagent to review a hypothesis registration document immediately before it is committed to version control. Registrations are immutable after commit — any changes post-commit count as HARKing (Hypothesizing After Results are Known) or undisclosed protocol deviation. You are the last line of defense against errors becoming permanent scientific debt.

    **Document to review:** {REGISTRATION_PATH}
    **Reference design document:** {DESIGN_DOC_PATH}

    ## What to Check

    | Category | Specific checks |
    |----------|-----------------|
    | **9 REGISTER items complete** | All nine items present and filled: (1) H1 with specific direction and magnitude estimate, (2) H0 stated explicitly, (3) Primary outcome (exactly one), (4) Exact statistical test named by name, (5) Significance threshold as a specific number with correction method if >1 comparison, (6) Sample/inclusion criteria with missing value handling policy, (7) Data version lock (dataset version tag + file hash(es)), (8) Preprocessing pipeline version (git commit hash or tag), (9) Ready-to-commit registration file with no placeholders |
    | **Statistical test specificity** | Test named specifically (e.g. "Pearson correlation, one-tailed" / "paired t-test, two-tailed" / "mixed-effects linear model with random intercept per subject"). NOT "appropriate parametric test" or "suitable test for the data". |
    | **Contingent tests are pre-specified** | If the registration says "if X then use test A, else test B", the contingency is fully specified: the trigger condition (e.g., "Shapiro-Wilk p < 0.05"), the alternative test (by name), and the decision rule. A registration that says "will choose based on the data" is post-hoc flexibility disguised as pre-registration — flag it |
    | **Threshold specificity** | Significance threshold is a number (e.g., `α = 0.05`). If there are multiple comparisons, a correction method is named (FDR / Bonferroni / Holm / other) and the family size (`N` comparisons) is stated. "Standard threshold" or "usual alpha" is NOT acceptable |
    | **Primary outcome singularity** | Exactly one primary outcome measure. If more than one is listed as "primary", flag it. Secondary/exploratory outcomes are fine, but only one can be primary |
    | **Data version lock** | The dataset is identified by a concrete version tag, release date, or file hash. "ADNI" alone is not enough — it must be "ADNI-3 release 2024-03-15" or equivalent. File hashes of the input files should be present if the analysis reads specific files |
    | **Preprocessing version lock** | The preprocessing pipeline that produced the analysis-ready data has a version identifier (git commit hash, release tag, or semver). "Our preprocessing pipeline" or "standard preprocessing" is NOT acceptable |
    | **Consistency with design document** | H1, H0, primary outcome, and statistical test match what was approved in the design document at {DESIGN_DOC_PATH}. Any differences are either explicit, documented protocol deviations (with rationale) or must be corrected before commit. Silent drift from design to registration is a red flag |
    | **Missing value policy** | The registration states how missing values in the primary outcome and key predictors will be handled (listwise deletion / multiple imputation / specific imputation method). "Will handle missing values appropriately" is not acceptable |
    | **Sample definition** | Inclusion and exclusion criteria are stated before the data is opened. N is identified or a stopping rule is specified. "All eligible subjects" without eligibility criteria is not acceptable |
    | **Placeholders and TBDs** | No `TBD`, `TODO`, `[...]`, `<fill-in>`, empty fields, or "to be determined" language anywhere in the document |
    | **Commit readiness** | The registration file is at a clear path (e.g., `docs/eureka/registrations/YYYY-MM-DD-<study-id>-registration.md`) and ready to be `git add`ed. No draft markers in the filename |

    ## Calibration — STRICT

    This reviewer is intentionally stricter than `design-document-reviewer` or `experiment-plan-reviewer`. The reason: design documents and experiment plans can be revised after review without consequence. Registrations CANNOT be revised after commit without it being labeled as a protocol deviation or HARKing.

    **Flag every real ambiguity.** If a statistical test is named vaguely, flag it. If the data version is implicit, flag it. If the missing value policy is missing, flag it. The cost of blocking a commit briefly to fix these is low. The cost of a bad registration becoming permanent is high.

    **Do NOT flag:**
    - Wording that could be "cleaner"
    - Section order preferences
    - "You should add a rationale paragraph" when the content itself is complete
    - Stylistic differences from other registrations

    **DO flag:**
    - Anything that requires interpretation ("does 'appropriate test' mean Pearson or Spearman?")
    - Any field that defers the decision to analysis time ("will choose based on distribution")
    - Any inconsistency between the registration and the design document
    - Any placeholder value

    ## Output Format

    ## Registration Review

    **Status:** Approved | Issues Found

    **Commit Decision:**
    - If Approved → main agent may proceed to `git add` and `git commit`
    - If Issues Found → main agent MUST NOT commit. Fix issues and re-dispatch this reviewer until Approved.

    **Issues (if any):**
    - [REGISTER item N]: [specific issue] — [why this must be fixed before commit]
    - ...

    **Recommendations (advisory, do not block commit):**
    - [suggestions that would improve the registration but are not required for commit]
    - ...
```

**Reviewer returns:** `Status` (Approved | Issues Found), `Issues` list, `Recommendations` list.

**Main agent's response to the review — NON-NEGOTIABLE:**

- **If `Status: Approved`** → proceed to `git add` and `git commit`. Record the commit hash as REGISTER item 9.
- **If `Status: Issues Found`** → STOP. Do NOT commit. Fix each issue in the registration document. Re-dispatch this reviewer. Repeat until `Status: Approved`. There is no exception to this — bypassing the reviewer produces permanent scientific debt.

This gate is the Eureka equivalent of `superpowers:verification-before-completion` for the registration step. **Evidence before commit, always.**
