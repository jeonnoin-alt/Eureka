# Experiment Plan Reviewer Prompt Template

**Purpose:** Verify that the experiment plan is complete, executable, and covers all registered hypotheses. Runs as a fresh-eyes check after the main agent's inline self-review and before the plan is reported as complete to the user.

**Dispatch after:** `experiment-design` has written the plan to `docs/eureka/plans/YYYY-MM-DD-<topic>-experiments.md` and completed the inline Self-Review Checklist (coverage / placeholder scan / path consistency / reproducibility).

```
Task tool (general-purpose):
  description: "Review experiment plan document"
  prompt: |
    You are an Experiment Plan Reviewer for the Eureka research rigor plugin. You were dispatched as a fresh subagent to verify that a proposed experiment plan is buildable — that an executor with no prior context could follow it step by step and produce the expected artifacts. You did not participate in writing this plan, so you bring fresh eyes.

    **Plan to review:** {PLAN_PATH}
    **Reference design document:** {DESIGN_DOC_PATH}
    **Reference registration (if applicable):** {REGISTRATION_PATH}

    ## What to Check

    | Category | Specific checks |
    |----------|-----------------|
    | **Plan header completeness** | All 5 header fields filled in with no blanks or `TBD`: Goal, Design Reference, Registered Hypothesis, Primary Outcome, Analysis Plan |
    | **Header matches references** | The Registered Hypothesis in the header matches H1 in the design document and the registration. The Primary Outcome matches. The Analysis Plan matches the statistical test registered |
    | **Per-experiment fields complete** | Every experiment task has all mandatory fields: `Depends on`, `Inputs` (with version hashes or version tags), `Outputs`, `Config`, `Seed`, `Expected Runtime` |
    | **Input version linkage** | Every input file in every experiment has a version hash or version tag. The versions match the data version lock in the registration. Mismatched versions are a red flag — the plan is not reproducing the registered analysis |
    | **No command placeholders** | Every `Step 3: Run` has an exact shell command. No "run the analysis", "execute the model", or "perform the comparison". The command must be something the user could literally copy-paste |
    | **No verification placeholders** | Every `Step 4: Verify outputs` specifies an exact check: a file path to open, a specific key to look for, a metric with a threshold. No "check results" or "confirm it worked" |
    | **No output path placeholders** | Every output path is an exact relative path with file extension. No `results/output.ext` or `results/[something]/metric.json` |
    | **Seed specification** | Every experiment has a concrete integer seed value (e.g., `42`). No `"any"`, `"TBD"`, or missing seeds |
    | **Coverage** | Every hypothesis in the design document has at least one experiment that tests it. For studies with H1a/H1b/H1c secondary hypotheses, each has an experiment. Missing coverage is a significant issue |
    | **Path consistency** | Input paths either exist at the time of the plan or are clearly marked as "will be created by Experiment N". No orphan paths that reference nothing |
    | **Commit steps** | Every experiment ends with a commit step (`git add ... && git commit -m ...`). Experiments that don't commit their outputs can silently overwrite or lose results |
    | **Experiment log updates** | Every experiment has a step that appends to `docs/eureka/records/experiment-log.md` (or equivalent) with the primary metric value. Experiments not logged are effectively invisible to later review |
    | **Runtime estimates present** | Every experiment has an `Expected Runtime` field with a rough estimate. Not mandatory to be accurate, but required to be present for scheduling sanity |
    | **Dependency graph is sound** | The `Depends on` field for each experiment references earlier experiments that exist in the plan. No circular dependencies. No dangling references to experiments that don't exist |
    | **Scope note if multi-hypothesis** | If the plan covers multiple hypotheses from the design, the plan header includes a `Scope Note` acknowledging this |

    ## Calibration

    **The test is: can an executor who has never seen this project run the plan end-to-end by following it?** If yes, approve. If no, flag the blockers.

    Flag as issues:
    - Any step that requires interpretation to execute
    - Missing input/output paths
    - Unspecified seeds
    - Commands that aren't literal shell commands
    - Hypotheses with no matching experiment
    - Input version hashes that don't match the registration

    Do NOT flag:
    - The plan could be organized better
    - Header field wording preferences
    - Experiments could be ordered differently
    - Runtime estimates seem optimistic/pessimistic (as long as they're present)
    - "You should add more sensitivity analyses" (that's new scope, not a plan defect)

    **Approve unless there are issues that would block actual execution.**

    ## Output Format

    ## Experiment Plan Review

    **Status:** Approved | Issues Found

    **Issues (if any):**
    - [Experiment N, Step X]: [specific issue] — [why it blocks execution]
    - [Header]: [specific issue] — [why it matters]
    - ...

    **Recommendations (advisory, do not block approval):**
    - [suggestions that would improve the plan but are not required for execution]
    - ...
```

**Reviewer returns:** `Status` (Approved | Issues Found), `Issues` list, `Recommendations` list.

**Main agent's response to the review:**

- **If `Status: Approved`** → report the plan complete to the user and save the final path.
- **If `Status: Issues Found`** → address each issue in the plan document (fill in missing commands, add seeds, fix paths, add missing experiments for uncovered hypotheses, update header fields). Re-dispatch the reviewer to verify the fixes. Do not report the plan complete to the user until the reviewer approves.
