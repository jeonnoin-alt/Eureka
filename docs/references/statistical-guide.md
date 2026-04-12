# Statistical Reference Guide

This is a reference document, not a skill. It provides lookup tables for test selection, effect size interpretation, and multiple comparison correction. Referenced by `eureka:hypothesis-first` and `eureka:claims-audit`.

---

## Test Selection Decision Guide

| Data type | Groups | Design | Distribution | Recommended test | Effect size metric |
|---|---|---|---|---|---|
| Continuous | 2 | Independent | Normal, equal variance | Independent t-test | Cohen's d |
| Continuous | 2 | Independent | Normal, unequal variance | Welch's t-test | Cohen's d |
| Continuous | 2 | Independent | Non-normal | Mann-Whitney U | Rank-biserial r |
| Continuous | 2 | Paired | Normal | Paired t-test | Cohen's d (difference) |
| Continuous | 2 | Paired | Non-normal | Wilcoxon signed-rank | Rank-biserial r |
| Continuous | 3+ | Independent | Normal | One-way ANOVA + Tukey | Eta-squared |
| Continuous | 3+ | Independent | Non-normal | Kruskal-Wallis + Dunn | Epsilon-squared |
| Continuous | 3+ | Repeated | Normal | Repeated-measures ANOVA | Partial eta-squared |
| Continuous | 3+ | Repeated | Non-normal | Friedman + Conover | Kendall's W |
| Continuous | — | Association | Normal, linear | Pearson r | r, r-squared |
| Continuous | — | Association | Non-normal/ordinal | Spearman rho | rho |
| Continuous | — | Prediction (1) | Normal residuals | Simple linear regression | R-squared, f-squared |
| Continuous | — | Prediction (many) | Normal residuals | Multiple regression | R-squared, partial R-squared |
| Categorical | 2+ | Frequencies | Expected counts >= 5 | Chi-square | Cramer's V |
| Categorical | 2+ | Frequencies | Expected counts < 5 | Fisher's exact | Odds ratio |
| Binary | — | Prediction | — | Logistic regression | Odds ratio, AUC |
| Survival | — | Time-to-event | — | Kaplan-Meier + log-rank / Cox | Hazard ratio |
| Brain imaging | — | Mass-univariate | — | t/ANOVA per voxel/ROI | Cohen's d per ROI |

**Parametric vs. non-parametric:** Prefer parametric when assumptions are met (greater power). Use non-parametric when normality is violated and n < 30 per group. With large samples, parametric tests are robust to moderate violations — document the justification.

---

## Effect Size Interpretation

| Metric | Small | Medium | Large | Use with |
|---|---|---|---|---|
| Cohen's d | 0.2 | 0.5 | 0.8 | t-tests, mean differences |
| Pearson r | 0.1 | 0.3 | 0.5 | Correlations |
| Eta-squared | 0.01 | 0.06 | 0.14 | ANOVA |
| Partial eta-squared | 0.01 | 0.06 | 0.14 | Factorial ANOVA, ANCOVA |
| Cohen's f-squared | 0.02 | 0.15 | 0.35 | Regression |
| Cramer's V | 0.1 | 0.3 | 0.5 | Chi-square |
| Odds ratio | 1.5 | 2.5 | 4.3 | Logistic regression, Fisher's |

**Caveat:** These are conventions, not thresholds. A "small" effect in medicine can save thousands of lives. A "large" effect in a tiny sample may not replicate. Always interpret relative to: prior literature, clinical/biological significance, and CI precision.

---

## Multiple Comparison Correction

| Situation | Method | Notes |
|---|---|---|
| Single pre-registered comparison | None | Document that it is a single comparison |
| 2-10 independent comparisons | Bonferroni | Conservative; simple |
| 2-10 correlated comparisons | FDR (Benjamini-Hochberg) | More power than Bonferroni |
| > 10 comparisons | FDR (Benjamini-Hochberg) | Bonferroni too conservative |
| ROI-based imaging | FDR across ROIs | N ROIs = N comparisons |
| Voxel-level imaging | FWE (random field theory) or FDR + cluster extent | FSL/SPM defaults |
| Gene expression / omics | FDR or Bonferroni | Report both raw and adjusted p |
| Exploratory analyses | Still correct | Correction prevents inflated claims |

---

## Assumption Checks

| Assumption | How to check | Report |
|---|---|---|
| Normality | Shapiro-Wilk (n < 50) or K-S (n >= 50) | W/D statistic, p-value |
| Homogeneity of variance | Levene's test | F statistic, p-value |
| Independence | Design-level argument | State why observations are independent |
| Sphericity | Mauchly's test (repeated measures) | W, p; Greenhouse-Geisser if violated |
| Linearity | Residual vs. fitted plot | Visual assessment or RESET test |
| Multicollinearity | VIF per predictor | Max VIF; flag if > 10 |

---

## Common Errors

| Error | Problem | Fix |
|---|---|---|
| p-value without effect size | Magnitude unknown | Always report effect size + CI |
| Parametric on non-normal, no justification | Inflated Type I error | Check normality; switch or justify |
| No multiple comparison correction | False positive inflation | Apply FDR or Bonferroni |
| Correlation described as causation | Unsupported inference | Causal language only with RCT/DAG |
| "Marginally significant" (p=0.06) | Threshold violation | p > alpha is a null result |
| Cherry-picking best metric | Inflated Type I error | Pre-register primary outcome |
| Only reporting significant results | Publication bias | Report all pre-registered comparisons |
| Non-significant = no effect | Conflating absence of evidence | Report CI; note insufficient power |
| R-squared without model formula | Uninterpretable | Report full model + adjusted R-squared |
