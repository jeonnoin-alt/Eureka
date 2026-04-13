# Research Journal Entry Template

This is the template used by `eureka:research-journal` for every journal entry. One entry per session. Entries are appended to `docs/eureka/journal/YYYY-MM-DD.md`.

Sections marked **required** must be present. All others are optional — omit them if the category had nothing in it.

---

## Template

```markdown
## [HH:MM] Session — [one-sentence summary]

### Worked on **(required)**
- [1–3 bullets of actual work done this session]

### Decisions
- **[Decision]**: [rationale, alternatives considered, why rejected]

### Failed attempts
- **[What was tried]**: [outcome], [likely reason], [what to avoid next time]

### Surprises
- [Expected X, got Y, probable explanation Z]

### Insights
- [Cross-project lessons worth remembering — may graduate to auto-memory]

### Blockers
- [What is preventing progress right now]

### Next session starts with **(required)**
- [Concrete first action when returning]

### References
- [Files touched, commits made, result files generated]
```

---

## Example

```markdown
## 14:30 Session — Baseline model comparison, Model A underperformed

### Worked on
- Ran Model A and Model B baselines on held-out test set (N=47)
- Computed per-subject Pearson r for both

### Decisions
- **Chose paired t-test over Wilcoxon**: residuals from both models passed Shapiro-Wilk (p=0.61, 0.48), so parametric test is appropriate and has more power. Registered in `docs/eureka/registrations/2026-04-10-...md`.

### Failed attempts
- **Ran Model A without per-subject normalization**: r=0.42, expected ~0.60 based on prior literature. Likely cause: inter-subject feature scale differences dominate the learned weights. Fix: normalize features per subject before fitting.

### Surprises
- Model B converged in 30 epochs instead of the expected 100+. May indicate the task is easier than assumed — worth checking if Model B is underfitting the harder examples.

### Insights
- When features are acquired at subject-level scale, per-subject normalization is a prerequisite for any baseline comparison — not an optional preprocessing step. This generalizes across datasets of this type.

### Blockers
- Need to decide whether the Model A result (r=0.42 un-normalized) is still worth reporting as "what not to do" or should be omitted. Will discuss with PI.

### Next session starts with
- Re-run Model A with per-subject normalization, compare to Model B on identical splits.

### References
- `results/run_20260413_1430/model_a_baseline.json`
- `results/run_20260413_1430/model_b_baseline.json`
- Commit: `0434e2a` — `run: baseline comparison Model A vs B`
```

---

## Rules

- **Worked on** must exist even if brief (single line is OK).
- **Next session starts with** must exist — this is the handoff to `eureka:whats-next`.
- All other sections: include only if there is substance. Do not write empty sections like "None" or "N/A".
- Total length target: 10–25 lines of content. Over 50 lines means you are over-writing — the journal is curated, not a transcript.
- Use concrete specifics: file paths, exact metric values, exact commit hashes — not vague descriptions.
- Capture rationale, not just facts. "Chose X because Y" beats "chose X."
