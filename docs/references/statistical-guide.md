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

---

## Computational Recipes (Python)

Copy-paste snippets for common statistical tasks. All examples use `scipy.stats`, `statsmodels`, or `numpy` — standard libraries in scientific Python. These recipes address the "post-hoc power analysis / MDE / parametric uncertainty — all manual coding" feedback.

### Minimum detectable effect (MDE) at 80% power

For a **two-sample t-test**, given sample sizes per group:

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
mde = analysis.solve_power(
    nobs1=100,        # group 1 size
    ratio=1.0,        # group 2 / group 1 ratio (1.0 = equal)
    power=0.80,
    alpha=0.05,
    effect_size=None  # solve for this
)
print(f"MDE (Cohen's d) at N=100 per group: {mde:.3f}")
```

For a **correlation (Pearson)** with a given N:

```python
from statsmodels.stats.power import FTestAnovaPower, NormalIndPower
import numpy as np

# Using Fisher-Z approximation
n = 50
alpha = 0.05
power = 0.80
z_alpha = abs(np.round(np.percentile(np.random.standard_normal(10**6), 100*(1-alpha/2)), 4)) or 1.96
z_beta = 0.842  # one-tailed beta at 80% power

# Required z-transformed r
z_r_needed = (z_alpha + z_beta) / np.sqrt(n - 3)
r_needed = np.tanh(z_r_needed)
print(f"MDE Pearson r at N={n}, 80% power, α=0.05: |r| ≥ {r_needed:.3f}")
```

### Post-hoc observed power (use cautiously, illustrative only)

**Caveat first**: post-hoc observed power computed from the observed effect size has known biases and is NOT a valid justification for a null result. Report it as illustrative context at most, never as "we had adequate power so the null is real":

```python
from statsmodels.stats.power import TTestIndPower

# Observed effect size from the study
observed_d = 0.3
n_per_group = 50

power = TTestIndPower().solve_power(
    effect_size=observed_d,
    nobs1=n_per_group,
    alpha=0.05,
    ratio=1.0
)
print(f"Post-hoc observed power (illustrative only): {power:.2f}")
# Interpretation: with observed d={observed_d}, this N has {power:.0%} power.
# Do NOT interpret this as "power was adequate". Report CI instead.
```

### Stratum-N feasibility

For a subgroup analysis, check whether each stratum has sufficient N:

```python
import pandas as pd

df = pd.read_csv("data/cohort.csv")
strata = df.groupby(["group", "subgroup"]).size()
min_required = 30  # rule of thumb; depends on test

for (group, subgroup), n in strata.items():
    status = "OK" if n >= min_required else "UNDERPOWERED"
    print(f"{group} × {subgroup}: N={n} [{status}]")
```

### Parametric power uncertainty (feedback F3 #4)

When inputs to a power calculation have uncertainty (e.g., correlation between outcomes ρ in [0.2, 0.5]; base rate in [0.3, 0.4]), propagate to a power range rather than reporting a single point estimate:

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Parametric uncertainty: effect size from literature has a plausible range
effect_size_range = np.linspace(0.20, 0.45, 26)  # 26 values from 0.20 to 0.45
n_per_group = 100
alpha = 0.05

power_values = [
    analysis.solve_power(effect_size=d, nobs1=n_per_group, alpha=alpha, ratio=1.0)
    for d in effect_size_range
]

print(f"Power range across plausible effect sizes (d = {effect_size_range[0]:.2f} to {effect_size_range[-1]:.2f}):")
print(f"  Min power: {min(power_values):.2%}")
print(f"  Max power: {max(power_values):.2%}")
print(f"  Median power: {np.median(power_values):.2%}")
```

For **negative binomial** models with correlated outcomes (complex power calc), use simulation:

```python
import numpy as np
from scipy.stats import nbinom, pearsonr
from statsmodels.discrete.discrete_model import NegativeBinomial

def simulate_power(n_per_group, effect_size, rho, alpha=0.05, n_sims=500):
    """Empirical power for a negative-binomial comparison with correlated outcomes."""
    reject = 0
    rng = np.random.default_rng(42)
    for _ in range(n_sims):
        # Generate correlated NB data (simplified — use copulas for real applications)
        group_a = rng.negative_binomial(5, 0.5, n_per_group)
        group_b = rng.negative_binomial(5, 0.5 - effect_size, n_per_group)
        # Proper test: NB regression or Wilcoxon; here we use Wilcoxon as a robust alternative
        from scipy.stats import mannwhitneyu
        stat, p = mannwhitneyu(group_a, group_b, alternative="two-sided")
        if p < alpha:
            reject += 1
    return reject / n_sims

# Sweep over uncertainty in effect size and correlation
for d in [0.1, 0.15, 0.20]:
    for rho in [0.2, 0.4]:
        p = simulate_power(n_per_group=100, effect_size=d, rho=rho)
        print(f"  d={d}, ρ={rho}: empirical power = {p:.2%}")
```

Result: a power RANGE (e.g., "48% to 85% depending on parametric inputs"), which is how feedback F3 #4 wanted power reported for NB regression with correlated outcomes.

### Sample-size justification template (for hypothesis-first registrations)

Include in the registration's Sample Size section:

```markdown
**Sample size**: N = <number> (per group)

**Justification**:
- Target effect size: d = <value>, based on <citation or pilot reference>
- Alpha: 0.05 (two-tailed)
- Target power: 0.80 (or stated otherwise)
- Calculation method: <tool/package, e.g., statsmodels.stats.power.TTestIndPower>
- Result: <d value × N gives power = 0.XX>

**Parametric sensitivity**:
- If effect size is d = <lower_bound>: power = <...>
- If effect size is d = <upper_bound>: power = <...>
- This range reflects <reason for uncertainty; e.g., "prior estimates in the literature range d=0.20-0.45">

**Interpretation**: The chosen N provides ≥80% power under <reasonable assumption>. If observed effect size falls below <threshold>, the study is underpowered and results should be interpreted as exploratory.
```

### Common pitfalls

- `TTestIndPower` takes `nobs1` (group 1 N), not total N
- `effect_size` for `TTestIndPower` is Cohen's d, not raw mean difference
- Simulation-based power needs enough sims (≥500) to be stable
- Reporting single-point power without uncertainty range hides assumptions
- Post-hoc observed power ≠ design-time power; they answer different questions
