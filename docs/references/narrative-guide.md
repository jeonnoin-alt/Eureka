# Narrative Guide

This is a reference document, not a skill. It provides lookup material for **manuscript framing** — contribution altitude, story arc patterns, discovery-adjusted framing, negative-result reframing, Intro-Discussion symmetry, and venue-specific altitude tuning. Referenced by `eureka:research-brainstorming` (initial positioning), `eureka:manuscript-writing` (discovery-adjusted framing at Step 2.5), and `eureka:submission-readiness` (venue tuning).

**Core premise**: the same results, framed differently, can be published at top-tier venues or desk-rejected. Framing is **judgment** — Eureka does not enforce it with iron laws, but provides checkpoints at the three phases where framing decisions are made.

---

## 1. When to use this reference

| Phase | Skill that invokes this | What to look up |
|---|---|---|
| **Initial design** (pre-data) | `eureka:research-brainstorming` questions 10-11 | §2 (altitude), §3 (arc) |
| **Post-results, pre-writing** | `eureka:manuscript-writing` Step 2.5 | §4 (discovery-adjustment), §5 (negative reframing) |
| **Pre-submission** | `eureka:submission-readiness` venue check | §7 (venue altitude), §9 (anti-patterns) |
| **Writing Discussion/Conclusion** | `eureka:manuscript-writing` section-reviewer | §6 (Intro-Discussion symmetry) |
| **Stuck** ("paper feels flat") | `eureka:whats-next` | §4, §8 (worked examples), §9 (anti-patterns) |

---

## 2. Contribution altitude — 4 tiers

Altitude = "at what level is your contribution pitched?" Higher altitude = broader impact claim, higher evidence bar. The altitude must match the evidence strength — mismatch is the #1 source of desk rejection.

| Tier | What you're contributing | Evidence required | Typical venue | Red flag |
|---|---|---|---|---|
| **Method improvement** | Better numbers on existing benchmark / task | One benchmark, fair baseline, honest effect size | Domain workshops, specialty journals | Overclaim as "new framework" without reframing the problem |
| **New framework** | New way to cast the problem, with evidence the framing is useful | Multiple datasets OR multiple methods showing the framing works | Society journals, Nat Comm, Science Advances | Claim without baseline comparison; claim when just renaming an old concept |
| **New phenomenon** | You observed something the field hasn't seen / reported | Robust replication (multiple cohorts / preps / seeds); mechanism hint | Nature, Science family | Observation without any mechanism; single-subject / single-run finding |
| **Falsification** | You disproved an assumption the field held | Null result powered to detect the assumed effect; pre-registered | Depends on assumption's reach — can be Nature-tier if widely held | Framing as "our method failed" instead of "the assumption is wrong" |

**Rule of thumb**: work backward from evidence to altitude, not the other way around. If you only have one dataset with a small effect, a "new phenomenon" claim will desk-reject. If you have robust replication across 5 cohorts of a surprising finding, a "method improvement" framing is selling yourself short.

**Altitude mismatch examples:**

- Claim "new framework" with evidence = one experiment. Reviewer: "This is a method comparison, not a framework."
- Claim "new phenomenon" with evidence = N=12, no replication. Reviewer: "Compelling but needs replication — reject."
- Claim "method improvement" with evidence = novel mechanistic insight. Editor: "You're underselling this."

---

## 3. Story arc patterns — 4 shapes

Every paper has a shape. Picking the right arc up front prevents Intro-Discussion drift and gives the Abstract a natural structure.

| Arc | Opening (Intro) | Middle (Methods+Results) | Close (Discussion) | When to use |
|---|---|---|---|---|
| **Problem-driven** | "X is not understood" | "Our approach tested Y" | "Y explains Z, resolving the unknown" | Clear field-level unknown with a clear answer |
| **Opportunity-driven** | "New data / tool / context now allows…" | "We applied it to…" | "Here is what we found, not previously possible" | New capability, underexplored territory, first-of-kind dataset |
| **Surprise-driven** | "Conventional view says X" | "But we observed Y" | "Revising the view to Z" | Unexpected finding that contradicts existing models |
| **Falsification-driven** | "Community assumes X is necessary / sufficient / general" | "We show X is not…" | "Field should reconsider…" | Solid null result against a strong, widely-held assumption |

**Arc mismatch examples:**

- Using **problem-driven** when your result is a surprise reveals no tension, producing a flat narrative
- Using **surprise-driven** without stating the conventional view clearly confuses readers — they don't know why your finding is surprising
- Using **opportunity-driven** when competing work exists makes the paper look incremental — should be **problem-driven** or **surprise-driven**

**Selection rule**: write the one-sentence headline first. The arc is dictated by whether that sentence answers "X was unknown, now we know" (problem), "this was not previously possible" (opportunity), "conventional view was wrong" (surprise), or "assumption X is false" (falsification).

---

## 4. Discovery-adjusted framing — the post-results pivot

The most important framing phase is **after results exist, before writing begins**. The interesting story is often not what was originally hypothesized. This is where `manuscript-writing` Step 2.5 fires.

### Checklist

1. What is the **strongest finding** in `results/` (by effect size, novelty, or surprise)?
2. Does the original hypothesis (from the design doc + hypothesis-first registration) capture that finding?
3. If a side finding is stronger than the primary outcome, would the paper be better centered on the side finding?
4. If the predicted effect was null but the null is informative (against a strong assumption), should the paper reframe as falsification?
5. Based on answers 1-4, **choose the final altitude (§2) and arc (§3)**.

### Guardrails — what must not change

Discovery-adjustment is **not** HARKing. The rule: **pre-registration constrains the hypothesis; it does not constrain the story**.

| Must stay pinned to pre-registration | Can shift with discovery |
|---|---|
| Hypothesis text (H1, H0) in Methods | Framing emphasis in Intro |
| Statistical test, threshold, correction | Contribution altitude claimed in Discussion |
| Primary outcome definition | Which result gets Figure 1 vs Supplementary |
| Reported p-values, effect sizes | Which arc shape the paper takes |
| Reported null results | How the gap is stated in Intro |

**Test for HARKing vs honest reframing:** if a reader of the Methods section sees the pre-registered hypothesis clearly, and the Results report exactly what that hypothesis predicted (pass or fail, faithfully), then a reframe in the Intro/Discussion is honest narrative. If the Methods retroactively describes an analysis you didn't pre-register, that's HARKing.

### Concrete workflow (Step 2.5 of `manuscript-writing`)

1. Re-read the approved design document — note the altitude + arc brainstorming committed to
2. Scan actual result files — note the strongest finding and whether it matches the prediction
3. Decide: keep original framing, or discovery-adjust?
4. If adjusting: write a one-paragraph framing decision in `docs/eureka/journal/YYYY-MM-DD.md` (research-journal) — altitude, arc, one-sentence contribution, what changed vs design, why
5. Commit the framing decision — all section writing flows from this

---

## 5. Negative result reframing

Null results and "method didn't work" outcomes are scientifically valuable **when framed correctly**. The framing converts "failure" into "informative constraint."

| Raw framing (desk-reject risk) | Reframed (informative) | Why the reframe works |
|---|---|---|
| "We failed to show X" | "We bounded X's contribution to < Y" | Converts null into a numeric upper bound — useful for field |
| "Our method didn't work" | "These boundary conditions limit the method's applicability" | Converts a failure into a scope-defining finding |
| "Hypothesis H1 rejected" | "Evidence against H1, consistent with H2" | Converts rejection into support for an alternative |
| "The correlation was weak" | "The effect, if present, is smaller than 0.X with 95% CI" | Converts a non-significant result into an effect-size ceiling |
| "Replication failed" | "Under pre-registered conditions, the effect is not replicable" | Converts failure into a specific replication-failure finding |

**Rule**: the reframe must be **true** — you can't claim an informative constraint if the study wasn't powered to provide one. Check: was the study powered to detect the effect you're now bounding? If yes, the bound is informative. If no, the null is uninformative and no amount of reframing helps.

**Falsification-driven arc** (§3) is specifically for the strongest negative results — ones that disprove a widely-held assumption. If your null result is against a weakly-held assumption, the falsification frame is itself overclaim.

---

## 6. Intro ↔ Discussion symmetry

Top-journal peer reviewers consistently flag "Discussion drift" — a Discussion that introduces contributions or claims not foreshadowed in the Introduction. This check fires in `section-reviewer-prompt.md` when reviewing a Discussion or Conclusion section.

### The symmetry rules

1. **Question closure**: the Introduction poses question Q; the Discussion closes by answering Q
2. **Contribution enumeration**: if the Introduction lists contributions {C1, C2, C3}, the Discussion restates each with the evidence collected
3. **Gap closure**: the Introduction cites gap papers (prior work that approaches but does not fill the gap); the Discussion cites the same papers to show the gap is now filled
4. **No new threads**: the Discussion does NOT introduce contributions, claims, or implications that were not foreshadowed in the Introduction

### Discussion drift anti-patterns

| Drift type | What it looks like | Fix |
|---|---|---|
| **New contribution introduced in Discussion** | Intro lists {C1, C2, C3}; Discussion enthusiastically discusses C4 that was never foreshadowed | Add C4 to Intro contributions, OR drop C4 from Discussion |
| **Orphan Intro contribution** | Intro claims C2 will be shown; Discussion never revisits C2 | Add a C2 paragraph to Discussion, OR drop C2 from Intro contributions |
| **Question left unanswered** | Intro opens with "How does X produce Y?"; Discussion never states an answer | Add explicit answer paragraph, OR rephrase Intro to match what Discussion actually shows |
| **Gap drift** | Intro cites papers {A, B, C} as the gap; Discussion cites {D, E} instead | Reconcile — usually the Intro should cite what Discussion ends up using |

### Template for Discussion opening (closes Intro's question)

```
[Intro opened by asking Q; Results showed R.]

We asked whether [Q as stated in Intro]. Our findings demonstrate [A]: [one
sentence summarizing the headline result R]. This directly addresses the gap
identified by [Citations A, B, C from Intro gap paragraph], which had shown
[what they showed] but not [the specific gap this paper fills].

We now discuss three implications: [C1, C2, C3 — matching Intro contributions].
```

This template forces symmetry by construction.

---

## 7. Venue-specific altitude tuning

Different journal families reward different framing altitudes. The same contribution can be pitched at different altitudes for different venues — but the altitude must match the evidence strength (§2) AND the venue's expectations.

| Venue family | Expected altitude | Typical opening sentence pattern | Key framing priority |
|---|---|---|---|
| **Nature, Science** | Broad impact / new phenomenon | "A fundamental question in [field] is whether [question]." | General readership; why the non-specialist cares |
| **Nat Comm, Science Adv, Cell Reports** | New framework / strong result with mechanism | "Understanding [X] requires [approach]. Here we show [finding]." | Scholarly audience; mechanism + implication |
| **Neuron, Cell, Current Biology** | Mechanism | "How does [X] produce [Y]? We find [causal chain]." | Mechanistic detail; causal chain over correlation |
| **NeuroImage, Brain, HBM** | Methodological rigor + clinical relevance | "Reliable measurement of [X] is essential for [clinical / scientific] use." | Methods rigor; reproducibility; validated in-domain |
| **JAMA, NEJM, Lancet** | Clinical actionability | "Whether [X] affects patient outcomes remains unclear." | Bedside impact; generalizability; hard endpoints |
| **IEEE Transactions, ACM, NeurIPS, CVPR** | Technical novelty + benchmarks | "Existing methods do X; we propose Y achieving Z on benchmark B." | Systems impact; benchmark advance; reproducibility of code |
| **PNAS, eLife** | Broad scientific interest, middle altitude | "A long-standing question is [Q]. Here we address it by [approach]." | Scholarly audience, breadth + rigor |

### Altitude tuning example (same work, different pitches)

Suppose the work is: "We trained a deep learning model on graph-structured input and showed it predicts outcome Y across two independent datasets at r=0.88, outperforming prior methods that required auxiliary feature X."

- **Broad-impact journal pitch**: "A fundamental question in [field] is whether auxiliary feature X is necessary for predicting Y. Here we show that a model trained without X predicts Y across two independent datasets at the highest reported accuracy, demonstrating that X is sufficient but not necessary — reframing the canonical assumption in the field." *(New framework altitude — "X is not necessary" is the reframe.)*

- **Specialty / methods journal pitch**: "Reliable prediction of Y is essential for [applied use case]. We validate a deep learning approach on two independent datasets, achieving cross-dataset transfer at r=0.88 — the highest reported generalization in this class of models." *(Method improvement altitude — benchmarks and reproducibility.)*

- **Mechanism-oriented journal pitch**: "Understanding how Y emerges requires validated computational models. Our model reveals that the graph topology alone captures the principal axis of Y, consistent across datasets, suggesting that [mechanism] is the load-bearing feature." *(Mechanism altitude — what the model reveals about the underlying process.)*

Each pitch uses the same data; the altitude, arc, and emphasis differ. The right choice depends on: evidence strength, venue reader, what the authors most want known.

---

## 8. Before / after framing examples

### Example 1 — model comparison paper

**Before (flat framing):**
> We compared three models (A, B, C) on a cross-validation benchmark. Model C achieved the best accuracy (0.86). The models differ in their handling of temporal dynamics. Our results show that Model C outperforms A and B.

*Problem*: No arc. No contribution altitude. Reader asks "so what?" — desk-reject.

**After (framework-altitude, surprise-driven arc):**
> Conventional methods for [task] rely on [approach X], which assumes [assumption Y]. We show that this assumption is unnecessary: a simpler model (Model C) that omits Y matches or exceeds the performance of methods that incorporate it, across 5 held-out cohorts. This reframes [task] as a problem where [Y] is a statistical artifact rather than a necessary feature, opening a path to [downstream simplification].

*Result*: Clear altitude (framework, §2). Clear arc (surprise-driven, §3). Contribution is obvious: "Y is not necessary."

### Example 2 — null result paper

**Before (failure framing):**
> We tested whether method M predicts outcome Y. We found no significant correlation (r=0.09, p=0.42). Future work may benefit from larger sample sizes.

*Problem*: Reads as "we failed." No informative bound. No contribution.

**After (falsification-driven arc, informative constraint):**
> Recent work has proposed that [M] is a necessary feature for predicting [Y], based on [citations]. We conducted a pre-registered test with N=500 subjects (80% power to detect r=0.25). We find that [M] explains less than 1% of variance in [Y] (r=0.09, 95% CI: -0.01 to 0.19), bounding its contribution well below proposed estimates. This argues against [M]'s role as a necessary predictor and suggests the field focus predictive effort on [alternative features].

*Result*: Same data. Now a falsification result with an informative numeric bound, against a named assumption, with a constructive next step.

---

## 9. Common framing anti-patterns

Patterns that reliably trigger reviewer / editor rejection. Check your draft against this list before submission.

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| **Buried lede** | Most interesting result appears in the 4th Results subsection or Supplementary | Restructure so the headline result is Figure 1 / first Results paragraph |
| **Oversold gap** | "Never before studied" when a search returns 20+ similar papers | State the gap precisely — what's the specific uncovered angle, not the general topic |
| **Triple contribution** | Intro lists 3 contributions, only 1 is substantive | Pick the strongest; demote the others to Methods or drop entirely |
| **Altitude mismatch** | "New phenomenon" claim with N=12 single-cohort evidence | Drop altitude OR add replication before submission |
| **Discussion drift** | Discussion introduces claims/contributions absent from Intro | Fix Intro OR fix Discussion (see §6) |
| **Hedged abstract** | "Our results suggest that perhaps X may contribute to Y" | State the finding directly; hedging in Abstract is desk-reject |
| **Jargon opening** | First sentence requires 3 domain-specific terms | Open at non-specialist altitude; ramp to specifics |
| **No-question Intro** | Intro recites background but never poses a specific research question | Force a single sentence: "We ask whether…" or "Here we test…" |
| **Contribution-less Abstract** | Abstract describes methods and results but never names the contribution | Add a "Our contribution is…" sentence |
| **Venue-abstract mismatch** | Nature-audience Abstract submitted to IEEE venue (or vice versa) | Re-pitch Abstract per §7 for the target venue |
| **Arc mismatch to result** | Problem-driven opening but the result is a surprise | Rewrite Intro to surprise-driven arc (§3); surprise is wasted if not set up |
| **Negative result as failure** | "Our method did not work" | Apply §5 reframing — informative constraint, not failure |

---

## 10. Further Reading

**On scientific narrative craft:**

- Gopen, G. D. & Swan, J. A. (1990). *The Science of Scientific Writing*. American Scientist — foundational text on sentence-level narrative
- Schimel, J. (2012). *Writing Science: How to Write Papers That Get Cited and Proposals That Get Funded*. Oxford — introduces the **ABT structure** (And, But, Therefore) for paper arcs
- Olson, R. (2015). *Houston, We Have a Narrative*. University of Chicago — narrative structure for scientists, includes ABT template
- Heard, S. B. (2016). *The Scientist's Guide to Writing*. Princeton — comprehensive modern treatment

**On editorial / desk-rejection perspectives:**

- Nature editorial guidelines: [https://www.nature.com/nature/for-authors](https://www.nature.com/nature/for-authors)
- eLife editorial transparency: [https://elifesciences.org/inside-elife](https://elifesciences.org/inside-elife)
- Nature Communications "The editorial decision" series
- Retraction Watch (commentary on post-publication narrative issues)

**On the ABT structure specifically:**

The Schimel / Olson ABT template compresses narrative arc into three beats:

```
AND — the stable, known context (agreement)
BUT — the tension, gap, or contradiction that motivates the work
THEREFORE — what you did / found that resolves the tension
```

ABT maps onto the arcs in §3:
- Problem-driven ABT: "Field agrees X is known AND Y is the standard approach, BUT Y fails in case Z, THEREFORE we tested alternative W"
- Surprise-driven ABT: "Conventional view says X AND this view is well-supported, BUT we observed Y inconsistent with X, THEREFORE we revise the view to Z"
- Falsification-driven ABT: "Community assumes X is necessary AND this has guided method design, BUT we show X-free methods perform equally, THEREFORE X is not necessary"

ABT is a useful self-check tool: if you can't compress your paper into AND/BUT/THEREFORE in one sentence each, the narrative is not yet tight.
