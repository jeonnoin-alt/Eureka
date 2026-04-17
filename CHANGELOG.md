# Changelog

All notable changes to Eureka will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.10.1] - 2026-04-17

### Added

- **`hooks/freshness-hash.sh`** — New shell helper that computes canonical SHA-256 hashes for the `manuscript_hash` and `results_hash` YAML frontmatter fields defined in v1.10.0's freshness protocol. Three modes: `manuscript <path>` (hashes a single file), `results <dir>` (content digest of all files in a results directory, excluding build artifacts), and `both <manuscript> <results>` (emits two YAML-ready lines). Without this helper, the v1.10.0 freshness protocol was theoretical — users had no shipped way to populate the hash fields. The helper uses only `sha256sum`, `find`, `sort` (standard coreutils) and is deterministic across filesystems (files sorted by relative path before hashing). Excluded from the `results/` digest: `.aux`, `.log`, `.out`, `.toc`, `.synctex.gz`, `.fdb_latexmk`, `.fls`, `.bbl`, `.blg`, `.DS_Store`, editor swap files (`~`, `.swp`) — these drift with every LaTeX recompile without representing actual result changes. Addresses v1.10.0 review item 1.

- **`README.md` "Consumer Paths" section** — New navigation aid explaining where Eureka skill artifacts live in a user's research project vs. in Eureka's own plugin repo. Resolves the "new user greps Eureka's repo for `docs/eureka/registrations/INDEX.md` and finds nothing" confusion. Table enumerates 9 canonical consumer paths (`docs/eureka/designs/`, `docs/eureka/registrations/`, `docs/eureka/plans/`, `docs/eureka/audits/`, `docs/eureka/reviews/`, `docs/eureka/novelty-audits/`, `docs/eureka/verifications/`, `docs/eureka/journal/`, and `docs/eureka/registrations/INDEX.md`) with their producing skill and purpose. Explicit rationale: these are the user's project state (decisions, hypotheses, reviews for their research), so `docs/eureka/` is gitignored in Eureka's plugin repo to prevent accidental example artifacts from confusing new users about what belongs to the plugin vs. their project. Addresses v1.10.0 review item 5.

### Changed

- **`skills/claims-audit/traceability-auditor-prompt.md`** — Step 1 regex patterns clarified. Added explicit "How to read the pattern table" block stating that patterns are illustrative starting points (not exhaustive or literal copy-paste), `...` means "extend with the same numeric-capture shape" (not literal ellipsis), Unicode characters (`ρ`, `η²`, `±`, `–`) appear as-is in both patterns and manuscripts (don't escape them), and LaTeX math-mode delimiters should be stripped before matching. The pattern table gained a third column of "Unicode / variant notes" covering `ρ/\rho`, `R²/R^2/R-squared`, `±`/en-dash variants, LaTeX `$...$` math-mode, and domain-specific count units (cells, mice, runs, seeds). Two new rows added: "Durations / rates" and "Scientific notation". Addresses v1.10.0 review item 2.

- **`skills/using-eureka/SKILL.md`** — Canonical Output Paths section gains a "Computing the hashes" subsection with three example invocations of `hooks/freshness-hash.sh`. Notes the design decisions behind `results_hash` content digest (sorted per-file sha256 concatenation, build artifacts excluded). Makes the freshness protocol practical rather than documentary.

### Rationale

Cleanup release addressing the three substantive items from the v1.10.0 code review:

- **Item 1 (HIGH)**: the v1.10.0 freshness protocol was theoretical without automation. v1.10.1 ships a `freshness-hash.sh` helper so populating the YAML frontmatter is a one-line shell call, not manual sha256 computation. The protocol now has teeth.
- **Item 2 (MEDIUM)**: the traceability-auditor's regex pattern table had implicit assumptions (escape `R^2` vs Unicode `R²`; `...` as placeholder vs literal) that could produce false negatives if interpreted narrowly. The clarifications make the pattern table a proper starting point while keeping the "adapt for your manuscript" flexibility.
- **Item 5 (MEDIUM)**: new users grep Eureka's plugin repo for `docs/eureka/` artifacts and find nothing because the directory is gitignored for consumers-vs-plugin-repo reasons. The new README section removes this friction with an explicit table and architectural explanation.

Items 3, 4, 6, 7 from the v1.10.0 review are deferred (tracking/stylistic, non-blocking).

Semver: PATCH. No new features, no breaking changes, no behavior changes beyond making an existing convention practical.

## [1.10.0] - 2026-04-17

### Added

- **`skills/claims-audit/traceability-auditor-prompt.md`** — New **computational subagent** (Eureka's first). Dispatched by `claims-audit` as Step 0 of its workflow. Regex-extracts every quantitative claim from the manuscript, scans `results/` files, produces a machine-readable diff (exact / approximate / untraceable). Eliminates the "23 numbers manually cross-referenced to CSV rows" cognitive load surfaced in external feedback. Uses 3-tier severity (Must-fix / Should-fix / Advisory). **Architectural shift**: differs from the 6 existing qualitative reviewer subagents — those judge, this computes. Sets the pattern for future computational subagents (figure regeneration auditor, citation-graph auditor, reproducibility smoke-test).

- **`docs/references/registration-lifecycle.md`** — New reference document (11 sections) unifying registration evolution concerns that were previously scattered across feedback: amendment vs supersede vs new registration decision tree with worked examples (Examples 1-3); `active / amended-by / superseded-by / archived` state machine; YAML frontmatter schema (`registration_id`, `status`, `supersedes`, `parent`, `created`, `last_modified`, `target_venue`); filename convention; `docs/eureka/registrations/INDEX.md` template for machine-readable chain tracking; **6-tier HARKing severity spectrum** (observation-noted → silent edit) with point-deduction mapping to research-reviewer D3/D4; data-discovery → registration feedback workflow (Option A/B/C/D decision tree for when observed data violates pre-registration assumption); plan ↔ registration contingency inheritance rules. Addresses F2 #4, F3 #3/#5/#6/#7.

- **`docs/templates/registrations-index-template.md`** — New template file shipped with Eureka as a seed. Users copy to `docs/eureka/registrations/INDEX.md` in their project repo when starting registration tracking; `hypothesis-first` maintains it thereafter. Prevents the "3 months after a pivot, no one knows which registration is authoritative" failure mode. (The consumer path `docs/eureka/registrations/INDEX.md` is gitignored in Eureka's own repo because `docs/eureka/` is reserved for Eureka CONSUMERS, not Eureka itself.)

- **Research-reviewer scoring anchors for D1-D4, D6, D7** — `agents/research-reviewer.md` previously had anchors only for D5 (Novelty & Contribution). v1.10.0 adds worked-example anchors for every sub-criterion across all 7 dimensions. Each anchor describes score bands (e.g., 0-8, 9-14, 15-18, 19-20 for a /20 sub-criterion). Improves inter-run reliability — two independent review runs on the same project should now produce similar scores because the rubric is less interpretive. Addresses F2 #2.

- **Severity-tier rollout to 6 existing reviewer subagents**: all subagent prompts now use **Advisory / Should-fix / Must-fix** output format, matching the v1.9.0 `novelty-audit-reviewer` pattern. Files updated:
  - `design-document-reviewer-prompt.md` (research-brainstorming)
  - `registration-reviewer-prompt.md` (hypothesis-first — most severe; Must-fix covers almost all substantive issues due to pre-commit gate importance)
  - `experiment-plan-reviewer-prompt.md` (experiment-design — includes new "contingency inheritance check" Must-fix dimension)
  - `section-reviewer-prompt.md` (manuscript-writing)
  - `figure-reviewer-prompt.md` (figure-design)
  - `research-reviewer-prompt.md` (requesting-research-review — maps to D3/D4 CRITICAL deductions)

  `Status: Approved` is preserved for backward compat (Approved ≡ Must-fix count = 0). Resolves v1.9.0 review item 3.

- **Red-team mode default-on for all 7 subagents**: each reviewer now has an explicit "Red-team mode (default on)" section directing it to actively hunt for hidden assumptions, overlooked alternatives, and substantive gaps — fresh-eyes means fresh *scientific critique*, not fresh read. If a reviewer passes without finding any Should-fix or Advisory item, it must document its red-team search strategy (3-5 sentences). Addresses F3 #1 ("reviewers almost always return Approved = compliance theater").

- **Plan ↔ Registration contingency inheritance**: `experiment-design` SKILL.md gains a new "Contingency Inheritance from Registration" section (Step 2 of its workflow). Rules: plan may ADD task-level operational contingencies but MAY NOT weaken or contradict registration contingencies. Silent override is a `Must-fix` flag in `experiment-plan-reviewer`. Resolves F3 #2.

- **`whats-next` resume mode** — new parallel mode alongside the existing Diagnostic Mode. Trigger phrases include "resume", "continue", "last session", "어디서부터", "이어서". Reads the most recent `docs/eureka/journal/` entry + `git log -20` + `docs/eureka/` subdirectory recent-modifications, then synthesizes "Last session ended at [phase]; next step is [skill]; context in 3 sentences; proceed?". Falls back to Diagnostic mode if journal is ambiguous or >2 weeks old. Addresses F2 #7.

- **Computational recipes in `docs/references/statistical-guide.md`** — new "Computational Recipes (Python)" section (~150 lines). Copy-paste snippets using `statsmodels`, `scipy.stats`, `numpy` for: MDE at 80% power (t-test, correlation), post-hoc observed power (with explicit caveat), stratum-N feasibility, **parametric power uncertainty** (F3 #4 — power range across plausible effect-size ranges, and NB regression simulation for correlated outcomes), sample-size justification template for hypothesis-first registrations, common pitfalls. Addresses F2 #8 and F3 #4.

- **Canonical output paths + freshness protocol** — new `using-eureka` sections defining canonical paths for each skill's durable artifacts (`docs/eureka/{designs,registrations,plans,audits,reviews,novelty-audits,verifications,journal}/`), YAML frontmatter with `generated_at` / `manuscript_hash` / `results_hash` / `status`. `verification-before-publication` and `submission-readiness` perform **soft-warn freshness checks** when upstream artifact hashes don't match current manuscript/results state. Hard block only if prerequisite artifact is missing entirely or has `status: failed`. Addresses F2 #3.

- **Korean/multi-locale announce allowance** — `using-eureka` relaxes the "announce at start" requirement to allow the announcement in the user's ambient language. Skill body and structured output (design docs, YAML frontmatter, review reports) remain in English for portability and CI parsing. Addresses F2 #6 and F3 #9.

- **Manuscript-writing figure-design auto-trigger hardened** — Writing Discipline Rule 3 now declares a **HARD-RULE**: when a section cites a figure that does not exist OR needs revision, you MUST invoke `eureka:figure-design` before continuing to write prose that depends on the figure. Addresses F2 #9.

### Fixed

- **v1.9.0 review item 1** — consolidated the two separate `**Pairs with:**` lines in `manuscript-writing` Integration section into a single nested bullet list.
- **Pre-existing domain leaks** opportunistically fixed while editing: "ADNI" removed from `design-document-reviewer-prompt.md` and `registration-reviewer-prompt.md` (generalized to `<dataset-name> v3.1` pattern); "NDM / ESM / AND" removed from `claims-audit` Completeness example table (generalized to "method A / method B / proposed method"); "NACC transfer" removed from `traceability-auditor` example row.

### Changed

- **`claims-audit` SKILL.md** — Audit Process now has a Step 0 that dispatches the `traceability-auditor` computational subagent first, consuming its table as input for Steps 1-3. Canonical output path: `docs/eureka/audits/YYYY-MM-DD-claims-audit.md`.
- **`hypothesis-first` SKILL.md** — Integration gains a "Lifecycle upkeep" subsection pointing to `registration-lifecycle.md`, an "INDEX.md upkeep (mandatory)" section declaring that every registration change must update `docs/eureka/registrations/INDEX.md` in the same commit, and a "HARKing severity spectrum" subsection. Reference line added for `registration-lifecycle.md`.
- **`experiment-design` SKILL.md** — new "Contingency Inheritance from Registration (Do This Second)" section added to the pre-task workflow. Reference line added for `registration-lifecycle.md`.
- **`manuscript-writing` SKILL.md** — Writing Discipline Rule 3 strengthened from "invoke when needed" to HARD-RULE "MUST invoke before continuing prose that depends on the figure". Integration section Pairs-with list consolidated into single nested bullet structure (v1.9.0 review item 1 fix).
- **`submission-readiness` SKILL.md** — Step 1 gains "Freshness verification (canonical output paths)" sub-table reading upstream artifact frontmatter. Soft-warn on hash mismatch; hard block only if artifact missing or status=failed.
- **`verification-before-publication` SKILL.md** — Publication Verification Checklist gains 2 new items: freshness check on claims-audit, upstream artifact presence verification.
- **README.md** — Reference Documents section adds `registration-lifecycle.md`. New "### Subagents" section enumerating all 7 subagent prompts with descriptions (including the distinction between qualitative reviewers and the new computational traceability-auditor).
- **`research-reviewer.md` agent** — "Dimensions 1-4, 6, 7" each gain a `**Scoring anchors (per sub-criterion)**` block with score-band descriptions for every sub-criterion. D5 anchors (which already existed) unchanged.

### Rationale

**Second of a 2-release roadmap** responding to April 2026 external feedback from AI agents using Eureka on real research projects. v1.9.0 (F1) closed the external competitiveness gap. v1.10.0 closes the F2+F3 cluster:

- **F2 underlying**: "discipline is excellent, but its cost is offloaded to cognitive load" → automation track (traceability-auditor + freshness protocol + scoring anchors + statistical recipes + Korean locale + whats-next resume)
- **F3 underlying**: "workflow skeleton solid, but ceremony-to-effect ratio low" → substance track (severity tiers + red-team mode default-on) + lifecycle track (registration-lifecycle.md)

**Architectural shift**: introducing the **computational subagent pattern**. Until v1.9.0, all 6 reviewer subagents performed qualitative judgment. `traceability-auditor` (v1.10.0) performs structural computation — regex + filesystem scan + numeric diff. This keeps Eureka's "markdown + subagent" architecture while automating the biggest cognitive-load complaint. Sets the pattern for future computational subagents.

**Severity-tier discipline**: the 3-tier format (Advisory / Should-fix / Must-fix) now runs across all 7 subagents uniformly. Prior 2-tier format (Approved / Issues Found) bundled nuance — every issue blocked approval, even stylistic. The 3-tier format preserves strict blocking (Must-fix → commit/submission blocked) while letting non-blocking concerns be reported without halting progress. Red-team mode default-on raises the substance floor — fresh-eyes reviewers now must actively hunt for hidden assumptions rather than passively reviewing.

**Registration lifecycle**: F2 #4 ("amendment vs new registration unclear"), F3 #3 ("redesign pivot cost 4 subagent runs + 2 rewrites"), F3 #5 ("data-discovery → registration feedback path absent"), F3 #6 ("superseded registration index absent"), F3 #7 ("HARKing prevention severity blunt") were all symptoms of one missing artifact: a formal registration lifecycle. `registration-lifecycle.md` consolidates them with YAML frontmatter state-machine, filename conventions, INDEX.md tracking, HARKing severity spectrum, data-discovery feedback workflow, and contingency inheritance rules.

**No new skills**: v1.10.0 adds 1 new subagent (`traceability-auditor`), 1 new reference doc (`registration-lifecycle.md`), and 1 new INDEX template, but **no new skills**. Skill count stays at 16 (v1.9.0's novelty-competitive-audit was the last addition). The restraint is deliberate: F2/F3 feedback was not about missing skills but about friction within existing ones.

**No breaking changes**: `Status: Approved` preserved in all subagent outputs (≡ Must-fix = 0); freshness checks are soft-warn not hard-block; canonical output paths are convention (skills still work with arbitrary paths if user overrides); Korean locale is allowance not requirement. Projects built on v1.9.0 work unchanged on v1.10.0.

## [1.9.0] - 2026-04-17

### Added

- **`skills/novelty-competitive-audit/SKILL.md`** — New **RIGID** skill that fires pre-submission to verify the manuscript's contribution is still novel against recent literature. Core premise: internal rigor gates (`claims-audit`, `research-reviewer`, `figure-design`) check internal consistency; they do NOT check whether the field moved in the 6-12 months between design approval and submission. Editors' first desk-reject filter ("does this advance the field?") is outside the other gates. This skill is the external competitiveness gate. Structure: 10-item checklist, HARD-GATE verdict table (PASS / CONCERN / BLOCK), 9-step per-audit workflow (extract headline claims → define search strategy → perform search → record candidates → 4-dim rubric evaluation → differentiation test → altitude recheck → verdict → dispatch reviewer subagent), rationalizations and red-flags tables, orthogonality matrix with existing skills. Korean triggers in description field ("출판 전 경쟁 검토", "preemption 체크", "novelty 감사").

- **`skills/novelty-competitive-audit/novelty-audit-reviewer-prompt.md`** — New subagent prompt template. Reviews the audit report across 9 dimensions: search scope honesty, candidate evaluation fairness, differentiation rigor, altitude-evidence match post-audit, verdict calibration, **red-team search** (reviewer independently hunts for 2-3 preempts the author may have missed), manuscript-claim consistency, pre-emptive citation check, action-menu consistency. Uses **3-tier severity output** (Advisory / Should-fix / Must-fix) — anticipates the v1.10.0 severity-tier rollout to all reviewer subagents; starting this new subagent with 3-tier from day one is cheaper than retrofitting.

- **`docs/references/novelty-audit-guide.md`** — New reference document (same pattern as `figure-guide.md`, `narrative-guide.md`). 11 sections: when-to-use matrix across 5 phase/skill entry points, search strategy by field (10-row table: medical/biology/neuroscience/CS-ML/physics/chemistry/social/economics/engineering/general), time-window guidance (2-year default with adjustment rules by field velocity), 4-dimensional preemption assessment rubric (primary claim / method / data / date × high / partial / low) with flagging rules, differentiation test template with bad/good examples, 3 worked preemption examples (BLOCK→CONCERN→PASS narrowing, BLOCK→venue change, partial overlap→pre-emptive citation), PASS/CONCERN/BLOCK decision tree, 5-option action menu for CONCERN/BLOCK verdicts (narrow claim / venue change / expand evidence / re-frame altitude / abandon), 10 common anti-patterns, search log template, further reading.

- **`manuscript-writing` Step 3 re-fire triggers** — the narrative-arc lock (v1.8.0) was "once per manuscript" by default. v1.9.0 adds 5 explicit re-fire triggers: (1) novelty-competitive-audit returns CONCERN or BLOCK, (2) target venue changes mid-project, (3) major result added/removed after initial draft, (4) reviewer response revision, (5) explicit user request. HARKing guardrail unchanged across re-runs: pre-registered hypothesis stays pinned in Methods+Results, only narrative framing shifts.

- **`narrative-guide.md` "When to re-run" subsection** in §4 (Discovery-Adjusted Framing) — table form of the 5 re-fire triggers with why/action columns.

- **`submission-readiness` Step 1 prerequisite #5** — `novelty-competitive-audit: PASS?` added as the new first prerequisite before the existing 4 gates (verification-before-publication, research-reviewer ≥95, claims-audit, venue-framing). Rationale: external novelty is the gate the others cannot check.

- **`verification-before-publication` Integration "Requires"** — `novelty-competitive-audit` PASS added as a required prerequisite alongside existing claims-audit, research-reviewer ≥95, hypothesis-first.

- **`using-eureka` Research Lifecycle diagram** — new `novelty` node between `write` and `audit`, with `novelty → write` backedge for CONCERN/BLOCK re-framing. New routing rule ("worried about preemption" → novelty-competitive-audit). New Red Flag ("Internal scores are high, we're ready to submit" → internal scores don't check external preemption). Added to RIGID skill types.

- **`whats-next` Common Stuck States** — 2 new rows: "The paper is rigorous but I'm not sure it's still novel" → `novelty-competitive-audit`; "Reviewer/editor surfaced a preempt paper" → `novelty-competitive-audit` first, then narrative-arc re-fire.

- **`README.md` Skills Library and Reference Documents** — `novelty-competitive-audit` listed under Publication Gates; `novelty-audit-guide.md` listed under Reference Documents.

### Rationale

Prompted by external feedback collected April 2026 from AI agents using Eureka on real research projects. The headline finding: **"Eureka checks if the paper is rigorous; it does not check whether it is worth publishing."** Concrete failure mode described: an agent reached a 96/100 research-reviewer PASS on a submission-ready manuscript, then caught a recent (2025) competitor paper that preempted the work through the agent's own critical questioning — not through any Eureka gate. None of claims-audit, research-reviewer, verification-before-publication would have caught the preempt. The gap was structural: Eureka enforces **internal rigor** but not **external competitiveness**.

v1.9.0 closes that gap with a new pre-submission gate. Design choices:

- **Structured review, not WebSearch automation** — per user decision. The skill structures the evaluation; the agent or user performs the actual literature search. Keeps domain judgment with the human+agent pair, avoids false confidence from brittle automation.
- **Multi-phase novelty** — `research-brainstorming` Step 3 already handles design-time novelty. This skill is the same concern at submission time, covering the 6-12 months of field drift since design approval. Both fire; they do not substitute for each other.
- **Separation of concerns preserved** — `claims-audit` still owns number traceability; this skill owns external novelty. Distinct scopes, distinct verdicts.
- **3-tier severity from day one** — the new subagent uses Advisory/Should-fix/Must-fix, anticipating v1.10.0's rollout of this pattern to the 6 existing reviewer subagents. Retrofitting later is more expensive than starting right.
- **Re-fire pattern for narrative-arc lock** — v1.8.0's "once per manuscript" default was correct as initial behavior, but the need for re-fire on specific triggers (venue change, preempt, major result shift) surfaced in feedback. v1.9.0 adds explicit re-fire conditions without changing the default behavior.

v1.9.0 is the **first of a 2-release roadmap responding to the feedback**. v1.10.0 (next release) addresses a cross-cutting cluster of concerns from the same feedback batch: traceability-auditor subagent (Eureka's first computational subagent pattern), registration-lifecycle reference doc with amendment/supersede/INDEX.md conventions, research-reviewer scoring anchors for inter-run reliability, severity-tier rollout to the 6 existing reviewer subagents, Korean/multi-locale announce allowance, `whats-next` resume mode, statistical recipes (MDE / post-hoc power / parametric uncertainty) in `statistical-guide.md`, experiment-design plan ↔ registration contingency inheritance, red-team mode default-on for existing reviewers.

Skill count: **15 → 16** (first skill addition since v1.3.0 manuscript-writing). Justified because novelty-competitive-audit is a distinct phase/gate with its own HARD-GATE verdict — not a pattern that fits inside an existing skill.

## [1.8.1] - 2026-04-17

### Changed

- **Cross-references by section title, not section number (regression fix from v1.8.0)** — v1.7.1 established the pattern of citing `docs/references/figure-guide.md` sections by **title** rather than number, because section numbers drift when the reference doc is renumbered. v1.8.0 introduced 9 new hard-coded `narrative-guide.md §N` references across 6 files, reproducing the bug. All 9 occurrences now cite stable section titles (e.g., **"Contribution altitude — 4 tiers"**, **"Discovery-Adjusted Framing"**, **"Venue-specific altitude tuning"**) across `research-brainstorming/SKILL.md`, `design-document-reviewer-prompt.md`, `manuscript-writing/SKILL.md`, `section-reviewer-prompt.md`, `submission-readiness/SKILL.md`, `whats-next/SKILL.md`.
- **`manuscript-writing` narrative-arc lock step renumbered** — v1.8.0 introduced the lock step as "Step 2.5" (mid-workflow fractional step), which broke the integer-step convention used by every other skill. The step is now **Step 3**; subsequent steps renumbered 3→4, 4→5, 5→6, 6→7, 7→8 in the Per-Section Workflow. Top-level Checklist and Integration references updated accordingly. `docs/references/narrative-guide.md` references to "Step 2.5" also updated to "narrative-arc lock step" (skill-version-agnostic phrasing to avoid future renumbering breakage).
- **`manuscript-writing` Step 3 HARD-GATE wording clarified** — v1.8.0's description mixed two rules ("before the FIRST section" + "do NOT write Introduction or Discussion before") that implied different scopes. The gate is now unambiguously universal: **before writing any section** (Introduction, Methods, Results, Discussion — all draw on the framing decision). Fires once per manuscript; subsequent sections skip if arc is locked and unchanged. Resolves the checklist-vs-step contradiction flagged in the v1.8.0 review.
- **`section-reviewer-prompt.md` Intro-Discussion symmetry rule now handles monolithic Markdown** — v1.8.0's rule assumed the Introduction was in a sibling file (correct for LaTeX `paper/sections/NN-*.tex` layouts). Monolithic Markdown manuscripts (single `.md` file with all sections) were unsupported. The rule now covers both: sibling file for LaTeX section-split layouts, earlier section in the same document for monolithic Markdown.
- **`research-journal` logging in the narrative-arc lock step is now optional** — v1.8.0 said "Write this paragraph to `docs/eureka/journal/YYYY-MM-DD.md` (via `eureka:research-journal`)", creating a soft dependency. v1.8.1 marks it "recommended but not required" and accepts alternatives (working notes, a top comment in the manuscript entry point) — the framing decision must be captured *somewhere*, not specifically in research-journal.
- **`narrative-guide.md` Hedged Abstract and Contribution-less Abstract anti-patterns now cross-reference `manuscript-writing`'s "Abstract written last" rule** — writing the Abstract after all other sections pass section-reviewer structurally prevents both anti-patterns (the findings are finalized, so there's nothing to hedge).

### Added

- **New research-brainstorming rationalization** — "I can't state an opposite-outcome headline (Q11) — it's an exploratory observational study" is now addressed in the Common Anti-Patterns table. The fix: for truly exploratory or first-of-kind studies, an honest opposite-outcome answer may be "we observed no systematic pattern"; if that is a field-informative null, frame the arc as **opportunity-driven** or **falsification-driven** rather than problem-driven. If the opposite outcome yields no reportable finding at all, flag as a design concern — the study may not be worth running.

### Rationale

Cleanup release addressing all 7 items from the v1.8.0 code review. High-severity (section-number regression) and medium-severity (checklist/step contradiction, fractional step numbering) items are fixed; four low-severity items (Q11 rationalization, research-journal softening, monolithic Markdown support, abstract cross-reference) are also resolved. No new features, no breaking changes.

## [1.8.0] - 2026-04-17

### Added

- **`docs/references/narrative-guide.md`** — New reference document (lookup, not a skill) covering **manuscript framing**. 10 sections: (1) when to use, (2) contribution altitude 4-tier table (method improvement / new framework / new phenomenon / falsification) with evidence-to-altitude match rules, (3) story arc patterns (problem / opportunity / surprise / falsification-driven), (4) **Discovery-Adjusted Framing** — the post-results narrative pivot with explicit HARKing guardrails (pre-registration constrains the hypothesis, not the story), (5) negative-result reframing (null → informative constraint), (6) Intro ↔ Discussion symmetry rules + template, (7) venue-specific altitude tuning for 7 journal families (Nature/Science, Nat Comm, Neuron/Cell, NeuroImage/Brain, JAMA/NEJM, IEEE/ACM, PNAS/eLife), (8) before/after framing examples, (9) common framing anti-patterns table (buried lede, oversold gap, triple contribution, altitude mismatch, discussion drift), (10) further reading with ABT structure (And/But/Therefore) from Schimel/Olson.

- **`research-brainstorming` SKILL.md** — Nine-question Socratic design refinement extended to **11 questions**. New Q10: "At what contribution altitude will this sit?" (altitude must match evidence strength). New Q11: "What is the one-sentence story arc, stated for both the predicted and opposite outcomes?" (if the opposite outcome leaves no honest story, the study or framing needs revision). New reference line added to Integration section pointing to `narrative-guide.md`.

- **`research-brainstorming/design-document-reviewer-prompt.md`** — Subagent checklist expanded from 9 to 11 mandatory questions. Two new review rows: **altitude-evidence match** (flags "new phenomenon" with single-dataset evidence, "framework" without baseline comparison, etc.) and **story arc falsifiability** (flags Q11 answers where the opposite-outcome headline is empty — a signal the study may not be worth running or needs a falsification-arc reframe).

- **`manuscript-writing` SKILL.md** — New **Step 2.5: Lock the narrative arc (Discovery-Adjusted Framing)** between Step 2 (read sources) and Step 3 (write). HARD-GATE: must complete before writing Introduction or Discussion. 5-question check (strongest finding / frame match / arc fit / altitude validity / commit). Explicit HARKing guardrail table distinguishing what must stay pinned to pre-registration (hypothesis text, statistical test, primary outcome, reported results) from what can shift with discovery-adjustment (framing emphasis, altitude, figure ordering, arc shape). Checklist extended from 7 to 8 items; Integration section adds `narrative-guide.md` reference.

- **`manuscript-writing/section-reviewer-prompt.md`** — New **Intro-Discussion symmetry** review dimension that fires only when reviewing a Discussion or Conclusion section. Checks 4 symmetry conditions: (a) research-question closure, (b) contribution restatement with evidence, (c) gap-paper revisitation, (d) no new threads (Discussion drift detection). Two new entries in the "Flag as issues" list. New "Narrative Symmetry Check" subsection in the output format.

- **`submission-readiness` SKILL.md** — New 4th prerequisite check in Step 1 before the existing 3 gates: **venue-specific framing tuned?** Flags altitude/venue mismatch (Nature-family claim with specialty-journal evidence, or vice versa) before the 4-option submission gate. Integration section references `narrative-guide.md` §2, §7, §9.

- **`whats-next` SKILL.md** — Two new entries in the Common Stuck States table: "Results are technically fine but the paper feels flat" → routes to `manuscript-writing` Step 2.5; "Not sure if this is Nature-level or specialty-journal-level" → routes to `submission-readiness` venue-framing check.

- **`README.md`** — Reference Documents section gains `narrative-guide.md` entry.

### Rationale

Eureka has always enforced **data integrity** (claims-audit), **statistical rigor** (hypothesis-first, research-reviewer), and now **figure discipline** (figure-design + multi-gate). But the same results, framed differently, can be published at a top-tier venue or desk-rejected. Narrative framing — contribution altitude, story arc, discovery-adjusted emphasis, venue-appropriate pitch, Intro-Discussion symmetry — is the axis Eureka previously did not address, producing manuscripts that were technically correct but narratively flat.

Framing is **judgment, not discipline**, which is architecturally different from everything else Eureka enforces. Framing also spans **three distinct phases** — initial positioning (brainstorming, pre-data), discovery-adjusted framing (post-results, pre-writing), and venue-specific tuning (pre-submission). A single skill cannot serve all three phases without phase-mismatch. Instead of adding a 16th skill (which would either fire at the wrong time or require awkward multi-invocation), this release adopts **distributed framing checkpoints** across 3 existing skills (research-brainstorming, manuscript-writing, submission-readiness) plus 1 new reference document. The pattern mirrors v1.5.0 (`latex-guide.md`) and v1.6.0 (`figure-guide.md`) — reference docs as lookups, enforcement at phase-appropriate existing gates.

Critical design property: the Discovery-Adjusted Framing checkpoint in `manuscript-writing` Step 2.5 includes explicit HARKing guardrails. Pre-registered hypotheses remain unchanged in Methods and Results (reporting discipline). Only the narrative framing (Intro emphasis, Discussion interpretation, contribution altitude claim) shifts to match what the data actually showed. This is honest reframing, not HARKing — the distinction is made explicit in both the SKILL.md step description and `narrative-guide.md` §4.

Skill count unchanged at 15. No new iron laws (framing is judgment). No changes to `claims-audit`, `hypothesis-first`, `figure-design`, `verification-before-publication`, or `research-reviewer` — their discipline scopes remain distinct from narrative framing.

## [1.7.1] - 2026-04-17

### Changed

- **Cross-references by title instead of section number** — `agents/research-reviewer.md` D4.5, `skills/verification-before-publication/SKILL.md`, and `skills/manuscript-writing/section-reviewer-prompt.md` previously referenced `docs/references/figure-guide.md` "section 5a" and "section 10". Section numbers drift when the reference doc is renumbered (as happened mid-edit during v1.7.0). All three cross-references now cite the section **titles** ("Figure Legend Requirements (Reviewer-Grade)", "Common Reviewer Rejection Reasons for Figures") — stable even if the doc is renumbered.
- **Deduction cap added to D4.5 (research-reviewer agent)** — the three new v1.7.0 figure-reporting deductions (-5 legend / -5 dynamite plot / -5 unlabeled representative image) now cap at **-15 per figure** rather than stacking to -45. Multiple figures each deduct independently up to the per-figure cap. Prevents a single unusually bad figure from sinking Dimension 4 on its own while still punishing systematic reporting failures.
- **Domain-neutral sample-independence phrasing** — v1.7.0's "biological vs technical replicates" language was biology-centric; an ML, physics, or HCI paper has different sample structure. Reworded across `figure-design/SKILL.md`, `figure-reviewer-prompt.md`, `section-reviewer-prompt.md`, `figure-guide.md`, and `research-reviewer.md` to reference **sample independence** generically, with field-specific examples listed: biology (biological vs technical replicates), ML/physics (independent vs repeated random seeds), psychology/HCI (subjects vs trials), clinical (patients vs scans), imaging (cells vs slices vs animals).

### Fixed

- **`docs/templates/research-review-report.md`** — updated stale dimension name from "4.5 Figure Integrity" to "4.5 Figure Integrity & Reporting" to match the v1.7.0 expansion of D4.5 in the `research-reviewer` agent.

### Rationale

Cleanup release addressing the v1.7.0 review's minor items. No new features, no breaking changes, no behavior changes beyond the D4.5 deduction cap (which makes scoring slightly more forgiving while preserving the reporting-compliance signal).

## [1.7.0] - 2026-04-17

### Added

- **`figure-design` SKILL.md** — 3 new Iron Laws:
  - **#9 Legend self-containment** — figure + legend alone must be interpretable without the main text
  - **#10 Statistical reporting in legend** — mandatory 7 elements: `n` per group, `n` definition, test name, error bar type (SEM/SD/95%CI), center value, p-value convention, biological vs technical replicates
  - **#11 Raw data visibility** — no dynamite plots (bar+whisker of mean alone) when N per group ≤ 50; overlay raw points via violin/strip/box/raincloud
- **`figure-design` SKILL.md** — "Dynamite plot" added to Chart Type anti-patterns list with eLife Top-10 reference; 5 new inline self-check items for legend and replicates; 4 new Common Rationalizations rows ("n is in Methods — don't need in legend"); 3 new Red Flags (missing n/test/error-bar; dynamite plots; unlabeled representative images).
- **`figure-reviewer-prompt.md`** — 2 new review dimensions added to the "What to Check" table: (1) **Legend compliance (reviewer-grade)** with 9 sub-checks mirroring top-journal reporting standards, (2) **Raw data visibility** with the N ≤ 50 dynamite-plot threshold. New Legend Compliance Check and Raw Data Visibility Check sections in the output format.
- **`docs/references/figure-guide.md`** — New **Section 5a "Figure Legend Requirements (Reviewer-Grade)"** covering what reviewers check, a copy-paste-ready figure legend template, bad vs good legend examples, and the dynamite-plot anti-pattern with a sample-size-to-chart-type decision table. New **Section 10 "Common Reviewer Rejection Reasons for Figures"** — lookup table mapping 14 real reviewer comments ("Statistical test not clear", "Error bars undefined", "Representative of what?", "Cannot assess variability from bar chart", etc.) to their root causes and fixes.
- **`section-reviewer-prompt.md`** — New "Figure legend reporting compliance" row added to the "What to Check" table: for each figure referenced in the section, verifies that the caption/legend states n, test, error bar type, center value, replicate type, and representative/quantification labeling. New Figure Legend Check subsection in the output format.
- **`research-reviewer.md` (agent)** — **Dimension 4.5 "Figure Integrity"** expanded to **"Figure Integrity & Reporting"**: now /10 integrity + /10 reporting, still /20 total. Reporting sub-criterion covers legend compliance per top-journal standards. 3 new deductions added to Dimension 4: legend missing n/test/error-bar/center (-5/figure), dynamite plot with raw overlay feasible (-5/figure), unlabeled representative image (-5/figure).
- **`verification-before-publication` SKILL.md** — 4 new items added to the Figures sub-section of the Publication-Specific Verification Checklist: legend completeness, p-value convention, representative/quantification labeling, no-dynamite-plot rule. `figure-guide.md` added as a reference in the Integration section.

### Rationale

v1.6.0 added design-level enforcement for figures (chart type, typography, colorblind palette, export format) via the `figure-design` skill and its `figure-reviewer` subagent. Real journal reviewers, however, flag **content-level reporting issues** far more aggressively than design issues — legend completeness (n, test, error bars, center value, biological vs technical replicates) and dynamite plots are the #1 and #2 most-cited figure problems per [eLife's Ten common statistical mistakes](https://elifesciences.org/articles/48175) and [Nature Cell Biology's reporting standards](https://www.nature.com/articles/ncb2964).

Moreover, single-gate enforcement at `figure-design` is leaky: a user who skips `figure-design` and goes straight to `requesting-research-review` or `manuscript-writing` would bypass the check entirely. v1.7.0 therefore uses **defense in depth** — the same reporting requirements are enforced at **4 independent review gates**, each with scope-appropriate granularity:

| Gate | Scope | Check depth |
|---|---|---|
| `figure-reviewer` subagent | Per figure, at creation | Full 12-dimension review including legend and raw-data visibility |
| `section-reviewer` subagent | Per manuscript section | For each figure referenced in the section, legend completeness only |
| `research-reviewer` 7-dim agent | Phase-level, holistic | Dimension 4.5 — integrity + reporting in aggregate with deductions per non-compliant figure |
| `verification-before-publication` | Pre-submission final gate | 4 legend-related checklist items must all pass |

`claims-audit` is intentionally unchanged — it owns number traceability (do the numbers in the text match the source files?), which is a separate concern from legend reporting compliance. Keeping the separation of concerns sharp prevents overlap and contradictions between skills.

## [1.6.0] - 2026-04-17

### Added

- **`skills/figure-design/`** — New skill covering research figure design (chart type selection, typography, colorblind-safe palette, layout, journal-specific export). Complements `claims-audit` Part B (figure integrity) — `figure-design` owns design, `claims-audit` owns integrity. Follows the same shape as `manuscript-writing`: iron law, checklist, hard-gate chart-type selection table, per-figure workflow, rationalizations table, red flags. Dispatches a `figure-reviewer` subagent after every figure renders.
- **`skills/figure-design/figure-reviewer-prompt.md`** — New subagent prompt template for per-figure review. Placeholders: `{FIGURE_PATH}`, `{SCRIPT_PATH}`, `{FIGURE_PURPOSE}`, `{TARGET_JOURNAL}`, `{CAPTION_TEXT}`. Ten review dimensions: chart-type fit, typography, color palette, axes/labels, legend, layout/chart junk, export format, journal compliance, script hygiene, reproducibility red flags. Output format matches the other five reviewer subagents (`Status: Approved` | `Issues Found`).
- **`docs/references/figure-guide.md`** — New reference document (same pattern as `statistical-guide.md` / `latex-guide.md` — lookup, not a skill). Sections: chart type selection flowchart, typography by journal, colorblind-safe palette hex codes (Okabe-Ito, tol-bright, viridis/cividis/plasma/inferno, RdBu_r/coolwarm/PuOr), journal-specific export spec table for 12 top journals (Nature, Nat Comm, Science, Science Advances, Cell, Neuron, JAMA, NEJM, IEEE Transactions, PNAS, NeuroImage, Brain), matplotlib style recipe (copy-paste `apply_paper_style()` function with TrueType embedding and Okabe-Ito palette), accessibility tools (Coblis, Color Oracle, WebAIM), common matplotlib pitfalls, export workflow for matplotlib/seaborn/ggplot2/Plotly, Tufte principles brief, and further reading.

### Changed

- **`manuscript-writing` SKILL.md** — Writing Discipline Rule 3 (figure references) now invokes `eureka:figure-design` when a cited figure needs to be created or updated. Integration section gains `figure-design` as a pairing skill and a reference line for `docs/references/figure-guide.md`.
- **`using-eureka` SKILL.md** — Research Lifecycle diagram adds `figure-design` node between Manuscript Writing and Claims Audit (writes text cites figure → figure-design creates/revises figure → returns to writing). Stuck-state routing adds a figure-design branch. Skill Priority section adds a "Make a figure / the figure looks wrong" routing rule. FLEXIBLE skill list adds `figure-design`.
- **`whats-next` SKILL.md** — Common Stuck States table adds two new entries: "The figure looks wrong / won't pass journal review" and "I need to make a figure for Results" both routing to `figure-design`.

### Rationale

Eureka v1.5.0 enforced figure **integrity** via `claims-audit` Part B (script-generated, no manual edits, traceable to a results file) but provided zero guidance on figure **design** — chart-type selection, typography, colorblind-safe palettes, journal-specific column widths, export format. The user feedback that prompted this release was concrete: agents produced figures that passed claims-audit but were rejected at top-journal submission for soft-failure reasons (Type 3 fonts, red/green-only contrast, default matplotlib rainbow cmap, sub-5pt axis labels, JPEG exports, 3D bar charts). This release closes that gap with the same skill-level enforcement pattern Eureka uses elsewhere: a skill with iron laws, a hard-gate for chart-type selection, a journal-export gate, and a fresh-eyes subagent review after every figure renders. Reference material lives in `docs/references/figure-guide.md` (same pattern as `statistical-guide.md` and `latex-guide.md`), keeping the skill itself focused on workflow and principles while the reference holds the lookup tables.

## [1.5.0] - 2026-04-17

### Added

- **`docs/references/latex-guide.md`** — New reference document covering LaTeX conventions for research manuscript writing. Same pattern as `statistical-guide.md` and `data-checklist.md` — lookup-oriented, not a skill. Sections cover: when to use LaTeX vs alternatives, recommended `main.tex` structure with common research-paper packages, section file organization (`paper/sections/NN-sectionname.tex`), BibTeX conventions (key format `FirstAuthorYear`, DOI mandatory, preprint-to-published replacement), natbib citation commands, math notation table (vectors bold lowercase, matrices bold uppercase, scalars italic), figure/table commands (`booktabs` tables, colorblind-safe palettes, script-generated figures enforced by `claims-audit`), abbreviation rules (spell out independently in abstract and main text), LaTeX compile workflow (`latexmk -pdf`), section-specific LaTeX patterns (contribution lists, equations, algorithms, limitations), common mistakes to avoid, and journal-specific conversion at submission time. Generalized from the neuroscience-specific conventions in a reference project — all domain-specific terminology removed.

### Changed

- **`manuscript-writing` SKILL.md** — Format Agnosticism section now recommends LaTeX as the default for STEM research targeting top-tier journals (Nature family, Science family, Cell family, Brain, NeuroImage, JAMA, IEEE Transactions). Markdown and other formats remain fully supported. The skill links to the new `docs/references/latex-guide.md` for users who choose LaTeX. Integration section adds a reference line for the LaTeX guide alongside the existing reference to `statistical-guide.md`.

### Rationale

Eureka v1.4.0's `manuscript-writing` skill was format-agnostic — it supported LaTeX, Markdown, and other formats equally, with no opinion on which to use. But in practice, most top-tier STEM journals accept or require LaTeX submissions, BibTeX is the de facto standard for citation management in the sciences, and the section-file split pattern (`paper/sections/NN-sectionname.tex`) aligns naturally with the per-section writing workflow this skill enforces. "No opinion" meant users got abstract guidance rather than concrete conventions. This release keeps the format-agnostic principle (humanities, preprint-first workflows, and Word-mandated collaborations are all still supported) but adds a strong LaTeX default recommendation and a concrete conventions reference for users who choose LaTeX.

## [1.4.1] - 2026-04-16

### Changed

- **Renamed** `skills/requesting-research-review/research-reviewer-template.md` → `research-reviewer-prompt.md` for consistency with the other four subagent reviewer prompt files (`design-document-reviewer-prompt.md`, `registration-reviewer-prompt.md`, `experiment-plan-reviewer-prompt.md`, `section-reviewer-prompt.md`). Updated the two references in `skills/requesting-research-review/SKILL.md`.
- **README manual install section** no longer hardcodes `1.0.0` in the path. New instructions detect the latest release tag via `git ls-remote` and use the correct `eureka-marketplace/Eureka/<version>/` cache path structure (aligning with v1.1.2's Windows EPERM fix).
- **README FAQ** gains a question about non-English trigger phrases. Documents that `research-journal` and `whats-next` include Korean trigger phrases in their `description` field (e.g., "기록해둬", "어디쯤이지") so native Korean speakers can trigger skills naturally. Notes that the mechanism is trivial to extend for additional languages.
- **`.gitignore`** comment for `docs/eureka/` is now explicit: the entry is defensive — those paths are produced by Eureka skills in projects that USE this plugin, not in the plugin repo itself.

### Fixed

- **v1.3.0 GitHub Release** — The `research-ideation` skill was committed and the CHANGELOG updated, but the `v1.3.0` git tag and GitHub Release page were never created in the previous session. Retroactively created the tag on commit `ae8e040` ("chore: release v1.3.0") and published the corresponding release page.

## [1.4.0] - 2026-04-16

### Added

- **`manuscript-writing` skill** — Guides section-by-section manuscript writing with prerequisite gates (no Results before results exist, no Discussion before Results is finalized, Abstract written last), citation discipline (every claim cited at write-time), number traceability (every quantitative value traced to a source file with inline comments), figure/table cross-reference validation, variable definition enforcement, and a per-section subagent review via `section-reviewer`. Format-agnostic: works with LaTeX, Markdown, or other formats. The user specifies their format at session start or in `CLAUDE.md`. Fills the gap between `requesting-research-review` (PASS) and `claims-audit` — previously there was no Eureka skill governing the writing process itself.
- **`section-reviewer` subagent prompt** (`skills/manuscript-writing/section-reviewer-prompt.md`) — Fresh-eyes per-section review dispatched during manuscript writing (step 5 of the per-section workflow). Checks citation completeness (every `\cite{}` key verified against bibliography), figure/table cross-references (every `\ref{}` has a corresponding file), number traceability (every quantitative value traced to results/), variable definitions, logic flow, prerequisite compliance, fabrication signals, and placeholders. Returns structured output with citation check counts, number traceability counts, and figure check counts alongside the standard `Status: Approved | Issues Found` format. Different from `claims-audit` (full-manuscript, post-writing) and `research-reviewer` (7-dimension publication readiness).

### Changed

- **`using-eureka`** lifecycle diagram — `manuscript-writing` is now an explicit node between `requesting-research-review` (PASS) and `claims-audit`. The old single "Manuscript Writing (your work + claims-audit)" node is split into two: `manuscript-writing` (section-by-section with reviewer) → `claims-audit` (full-manuscript audit). Added `audit → write` feedback loop for claims-audit failures. Journal dashed edges now include `audit` node. FLEXIBLE skill types list gains `manuscript-writing`.
- **README** — Research Workflow section adds `manuscript-writing` as step 6 (renumbering remaining steps). Skills Library gains "Writing" category with `manuscript-writing` entry.

## [1.3.0] - 2026-04-16

### Added

- **`research-ideation` skill** — New optional entry point for the research workflow. Generates 3-10 concrete research ideas from keywords, datasets, and/or papers, each with metadata (difficulty, data needs, estimated duration, core methodology). Recommends one idea and suggests handing off to `research-brainstorming` to shape it into a rigorous study design. Sits before `research-brainstorming` in the lifecycle: ideation (diverge) → brainstorming (converge) → hypothesis-first (register) → experiment-design (plan).

### Changed

- **`using-eureka`** — Lifecycle diagram adds `research-ideation` node before `research-brainstorming`. Routing flowchart adds "Has formed research question?" decision diamond. Skill Priority adds `research-ideation` to process skills. Flexible list updated.
- **`whats-next`** — Routing table splits former "Pre-design" row into "Pre-ideation" (→ `research-ideation`) and "Pre-design" (→ `research-brainstorming`) with a discriminating rule. Two new Common Stuck States added.
- **`README.md`** — Research Workflow adds step 0 (`research-ideation`). New "Which skill do I need?" guide distinguishes ideation from brainstorming. Skills Library adds "Ideation" category.

## [1.2.0] - 2026-04-14

### Added

- **Three subagent document reviewers** — Eureka now dispatches a fresh subagent reviewer at the end of each design-phase skill, matching the pattern Superpowers uses with its `spec-document-reviewer` and `plan-document-reviewer`. Previously Eureka relied on inline self-reviews, which miss blind spots because the writer reviews their own work in the same context.
  - **`design-document-reviewer`** (`skills/research-brainstorming/design-document-reviewer-prompt.md`) — dispatched from `research-brainstorming`. Verifies all 9 mandatory questions are answered, H0 is specific, falsifiability is concrete, confounds have named control mechanisms, data provenance is locked, and no placeholders remain. Runs between the inline self-review and the user approval gate.
  - **`registration-reviewer`** (`skills/hypothesis-first/registration-reviewer-prompt.md`) — the critical gate. Verifies all 9 REGISTER items are complete, specific, and consistent with the approved design document BEFORE the VCS commit. This reviewer is intentionally stricter than the others because registrations are immutable post-commit — errors become permanent scientific debt that cannot be corrected without HARKing disclosures. Blocks commit on `Issues Found`.
  - **`experiment-plan-reviewer`** (`skills/experiment-design/experiment-plan-reviewer-prompt.md`) — dispatched from `experiment-design`. Verifies the plan is buildable: no placeholder commands, all experiments have exact inputs/outputs/configs/seeds/commit steps, path consistency holds, every hypothesis has at least one experiment, and input version hashes match the registration. Runs between the inline Self-Review Checklist and reporting the plan complete to the user.

### Changed

- **`research-brainstorming`** — Checklist adds a new step 13 "Dispatch design-document-reviewer subagent" between inline self-review (step 12) and user approval (now step 14). Process flow diagram updated. New "Dispatching the Design Document Reviewer" section documents the fill-and-dispatch protocol and how to act on `Issues Found`.
- **`hypothesis-first`** — REGISTER phase now has an explicit pre-commit gate. New "Dispatching the Registration Reviewer (PRE-COMMIT GATE — NON-NEGOTIABLE)" section is inserted between the 9-item draft and the `git add` / `git commit` step. The flowchart now shows the three-node sequence `register → inline verify → subagent review → commit`, with `Issues Found` looping back to the drafting step. The verification checklist adds a new item: `registration-reviewer subagent dispatched and returned Status: Approved`.
- **`experiment-design`** — New "Dispatching the Experiment Plan Reviewer" section inserted between the Self-Review Checklist and the Save Location step. Plan is not reported complete to the user until the reviewer approves.

### Rationale

This closes a real architectural gap versus Superpowers. Main agent context was previously doing write + review + execute in the same session, which pollutes context and misses blind spots. Fresh subagent reviews catch things inline reviews cannot.

Research-specific justification: `hypothesis-first`'s registration is immutable once committed. A bad registration that slips through becomes permanent scientific debt — any retroactive correction counts as HARKing or undisclosed protocol deviation. The `registration-reviewer` is the last line of defense before that commit becomes permanent, and is therefore the strictest of the three reviewers. It's the scientific equivalent of `superpowers:verification-before-completion` applied to the registration step: **evidence before commit, always.**

No per-task execution subagents (Superpowers' `implementer`, `spec-compliance-reviewer`, `code-quality-reviewer`) are added in this release. Research experiments are user-executed (data loading, model training, GPU jobs) and an automated experiment runner does not fit the research workflow model. `experiment-design` already produces a plan the user follows manually.

## [1.1.2] - 2026-04-14

### Fixed

- **Windows install error (EPERM, case collision)** — v1.1.1 capitalized the plugin name to `Eureka` so the slash-command namespace would appear as `Eureka:`, but the marketplace name in `marketplace.json` was still `eureka` (lowercase). On Windows (case-insensitive filesystem), this meant Claude Code tried to extract the plugin into `cache\eureka\Eureka\1.1.1\`, where the parent `eureka` and child `Eureka` resolve to the same directory. The rename operation failed with `EPERM: operation not permitted, rename`.

  Reported error from a v1.1.1 Windows install:
  ```
  Error: Failed to install: EPERM: operation not permitted, rename
    'C:\Users\User\.claude\plugins\cache\Eureka' ->
    'C:\Users\User\.claude\plugins\cache\eureka\Eureka\1.1.1'
  ```

  Fix: The marketplace top-level name in `.claude-plugin/marketplace.json` is now `eureka-marketplace` (case-distinct from the plugin name `Eureka`). The cache path becomes `cache/eureka-marketplace/Eureka/1.1.2/`, with no case-only collisions in any parent-child pair.

  This follows the same pattern superpowers uses: marketplace `superpowers-dev`, plugin `superpowers` — two genuinely different strings.

### Migration

If you got the EPERM error on v1.1.1, do the following in Claude Code:

```
/plugin marketplace remove eureka
/plugin marketplace add jeonnoin-alt/Eureka
/plugin install Eureka
```

The first command removes the half-installed v1.1.1 marketplace registration. The second re-adds it (now picking up the v1.1.2 marketplace name `eureka-marketplace`). The third installs the plugin cleanly.

If `/plugin marketplace remove` does not clean up the cache directory, manually delete `C:\Users\User\.claude\plugins\cache\eureka\` (or `~/.claude/plugins/cache/eureka/` on macOS/Linux) before retrying.

## [1.1.1] - 2026-04-14

### Changed

- **Plugin name capitalized to `Eureka`** — The `name` field in `.claude-plugin/plugin.json` and the `plugins[0].name` field in `.claude-plugin/marketplace.json` are now `"Eureka"` (capitalized) instead of `"eureka"`. Per Claude Code's plugin docs, the plugin name controls the slash-command namespace, so plugin skills now appear as `/Eureka:research-brainstorming`, `/Eureka:hypothesis-first`, etc., instead of `/research-brainstorming` (which had no visible namespace prefix). The `package.json` `name` field stays lowercase (`eureka`) per npm convention.

### Migration

Existing installs need to reinstall to pick up the new namespace:

```
/plugin uninstall eureka
/plugin marketplace update eureka
/plugin install Eureka
```

The install command argument is now case-sensitive: `Eureka`, not `eureka`.

## [1.1.0] - 2026-04-13

### Added

- **whats-next** skill — Triage / dispatcher skill for researchers who are stuck or unsure of the next step. Scans project state (designs, registrations, plans, results, manuscripts), asks diagnostic questions, maps the user to a research lifecycle phase, and recommends 2–3 next actions linked to specific Eureka skills. Always hands off — does not do the work itself. Triggered by phrases like "what should I do next?", "I'm stuck", "where am I?", or any equivalent. Fills the gap that other Eureka skills leave: every other skill has a specific trigger condition, but "I don't know which phase I'm in" is a meta-state with no specialist owner. `whats-next` is that meta-router.
- **research-journal** skill — Writer counterpart to `whats-next`'s reader role. Appends structured narrative entries to `docs/eureka/journal/YYYY-MM-DD.md` capturing decisions, failed attempts, surprises, insights, blockers, and a "Next session starts with" handoff field. Triggered by explicit user request, session wind-down signals, post-decision moments, post-failure moments, or pre-phase transitions. Complements `experiment-log.md` (metric-focused) with WHY-focused narrative. Identifies cross-project insights and suggests promoting them to Claude Code auto-memory without writing to it directly. Fills the narrative continuity gap: Eureka had rich file persistence (registrations, audits, experiment-log) but no writer for mid-project decision rationale and blocker state.
- **docs/templates/research-journal-entry.md** — Template consumed by `research-journal`. Required sections: `Worked on`, `Next session starts with`. Optional sections: `Decisions`, `Failed attempts`, `Surprises`, `Insights`, `Blockers`, `References`. Includes a concrete worked example and length/specificity rules.
- **Multi-platform support** — Eureka now installs on five platforms. Added `.cursor-plugin/plugin.json` and `hooks/hooks-cursor.json` (Cursor); `gemini-extension.json`, `GEMINI.md`, and `skills/using-eureka/references/gemini-tools.md` (Gemini CLI); `.codex/INSTALL.md` and `skills/using-eureka/references/codex-tools.md` (Codex — symlink-based install, requires `multi_agent = true` in `config.toml` for subagent dispatch); `.opencode/INSTALL.md` and `.opencode/plugins/eureka.js` (OpenCode JavaScript plugin that injects the bootstrap via system prompt transform and auto-registers the skills directory). `package.json` now specifies `main` pointing at the OpenCode plugin entry point. The Claude Code install path is unchanged.
- **`skills/using-eureka/references/` directory** — Tool-name mapping tables for Gemini CLI and Codex. Translates Claude Code tool names (`Skill`, `TodoWrite`, `Task`, `Read`, `Write`, `Edit`, `Bash`) into their platform equivalents and documents subagent dispatch workarounds for platforms without a `Task` tool.
- **README Quick Start section** — Concrete first-session walkthrough for new users: start with `whats-next`, end with `research-journal`, let everything else trigger automatically. Clarifies that Eureka is strictly additive and does not require restructuring existing projects.
- **README FAQ section** — Five common concerns answered: existing project migration, pre-registration of past experiments, `CLAUDE.md` precedence, exploratory work feeling heavy, and disabling a specific skill.
- **README installation section** — Expanded to document all five supported platforms with platform-specific install commands and links to the per-platform `INSTALL.md` files.

### Changed

- **using-eureka** — Lifecycle diagram now includes `whats-next` as an alternative entry point and `research-journal` as a cross-phase continuous overlay. Skill Priority section adds triage as step 0 and continuity (research-journal) as step 5. Both new skills listed under FLEXIBLE types.
- **whats-next** — Step 1 project state scan now explicitly includes `docs/eureka/journal/*.md` (most recent entry) as a strong continuity signal. Step 2 reads the `Next session starts with` field from the latest journal entry and quotes it back to the user. Step 6 hand-off ends with a soft reminder that `research-journal` can capture the current session at the end.

### Build

- **CI**: Bumped `actions/checkout@v4` → `@v6` (v6.0.2) and `actions/setup-python@v5` → `@v6` (v6.2.0) to use Node 24-compatible action versions, resolving the Node 20 deprecation warning ahead of GitHub's 2026-06-02 force-migration deadline.
- **CI**: JSON validation job extended to cover `.cursor-plugin/plugin.json`, `gemini-extension.json`, and `hooks/hooks-cursor.json`.
- **CI**: New step runs `node --check` on `.opencode/plugins/eureka.js` to catch JavaScript syntax errors before they ship.
- **Branch protection**: Force-push and deletion blocked on `main` via classic branch protection. Force-push attempts are rejected by GitHub.
- **Tag protection**: Repository ruleset blocks deletion, non-fast-forward, and update on tags matching `v*`. Release tags are now immutable.

## [1.0.0] - 2026-04-12

### Added

- **Plugin scaffold**: `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `hooks/hooks.json`, `hooks/session-start`, `hooks/run-hook.cmd` — mirroring the Superpowers plugin architecture for cross-platform compatibility (Claude Code on Linux/macOS/Windows).
- **SessionStart hook**: Automatically injects `using-eureka` bootstrap skill content into the system context at every new session, teaching the agent to auto-invoke Eureka skills when research tasks are detected.

#### Bootstrap
- **using-eureka**: Meta-skill that establishes how to find and invoke Eureka skills. Includes rationalization table for researcher-specific excuses, skill priority order (process → review → gate), coexistence rules with Superpowers, and the research lifecycle flowchart.

#### Design & Registration
- **research-brainstorming**: Nine-question Socratic design refinement before any experiment. Mandatory questions cover null hypothesis, primary outcome, falsifiability, confounds (including data leakage), statistical power, alternative explanation, prior publications, contradictory evidence, and data provenance. HARD-GATE blocks analysis execution until a design document is approved.
- **hypothesis-first**: Scientific equivalent of test-driven development. Enforces REGISTER → EXECUTE → INTERPRET cycle. Nine-item registration checklist includes H1, H0, primary outcome, exact statistical test, significance threshold, sample/inclusion criteria with missing value handling, data version lock (file hashes), preprocessing pipeline version, and commit hash. Iron Law: NO DATA ANALYSIS WITHOUT A REGISTERED HYPOTHESIS FIRST.
- **experiment-design**: Break approved designs into executable experiment tasks with exact data paths, version hashes, configs, seeds, commands, and verification steps. Every task produces committable output. Mirrors Superpowers writing-plans for research execution.

#### Troubleshooting
- **systematic-troubleshooting**: Four-phase root cause investigation (Investigate → Pattern Analysis → Hypothesis → Resolution) for unexpected experimental results. Phase 1 includes research-specific diagnostic table (data quality, preprocessing consistency, data leakage, numerical issues, seed fixation, config propagation, metric calculation). Escalates to hypothesis re-examination after three failed fixes.

#### Review
- **requesting-research-review**: Dispatch `research-reviewer` subagent with structured context (research question, design doc path, result files, domain, target venue, pass threshold). Provides threshold guide for mid-project vs pre-submission reviews.
- **receiving-research-review**: Handle review feedback with scientific rigor. READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT protocol. Forbids performative agreement ("You're absolutely right!"). Defines when and how to push back on incorrect reviewer feedback.

#### Publication Gates
- **claims-audit**: Three-component audit of a manuscript. (A) Number traceability — every reported number traced to a source file. (B) Figure integrity — every figure verified as script-generated. (C) Completeness — every experiment in the log accounted for in the manuscript, including null results. Iron Law: EVERY NUMBER IN THE MANUSCRIPT MUST TRACE TO A SPECIFIC FILE.
- **verification-before-publication**: Fresh evidence gate before any submission claim. Mirrors Superpowers verification-before-completion. Publication checklist covers claims, figures, reproducibility (including raw → processed data regeneration from a single command), review status, reporting completeness, and manuscript metadata.
- **submission-readiness**: Four-option decision gate after verification passes (submit to journal / preprint first / continue refining / pivot). Forces explicit documentation of the choice and reasoning.

#### Agent
- **research-reviewer**: Seven-dimension publication readiness assessor dispatched as a subagent. Dimensions: (1) Scientific Foundation, (2) Methodological Rigor, (3) Experimental Execution, (4) Results Quality & Integrity, (5) Novelty & Contribution, (6) Reproducibility & Transparency, (7) Domain-Specific Standards. Evidence-only scoring, configurable pass threshold (85 for mid-project, 95 for pre-submission), produces Gap-to-Threshold analysis for failing dimensions.

#### Reference Documents
- **docs/references/statistical-guide.md**: Test selection decision guide, effect size interpretation, multiple comparison correction methods, assumption checks, common statistical errors. Referenced by `hypothesis-first`, `systematic-troubleshooting`, and `verification-before-publication`.
- **docs/references/data-checklist.md**: Data provenance template, preprocessing pipeline requirements, data leakage taxonomy (temporal, group, feature, preprocessing, label, duplication, target encoding, hyperparameter), missing value decision tree, data split best practices, descriptive statistics (Table 1) template, data version locking requirements. Referenced by `research-brainstorming`, `hypothesis-first`, `experiment-design`, `systematic-troubleshooting`, and `verification-before-publication`.

#### Templates
- **docs/templates/research-design-doc.md**: Output template for `research-brainstorming` — research question, hypotheses (H1/H0/falsifiability), study design, pre-specified analysis plan, operationalization, limitations, approval.
- **docs/templates/research-review-report.md**: Output template for `research-reviewer` — evidence base, dimension scores summary, detailed scoring tables, gap-to-threshold analysis, critical/major/minor issues, verdict with next steps.

### Infrastructure

- **Coexistence with Superpowers**: Eureka and Superpowers share the same plugin architecture and can be installed side by side. `using-eureka` explicitly documents the namespace split (software → `superpowers:*`, science → `eureka:*`).
- **Topics (15)**: `ai-agents`, `claude-code`, `claude-plugin`, `claude-skills`, `hypothesis-testing`, `open-science`, `pre-registration`, `reproducibility`, `reproducible-research`, `research`, `research-methods`, `scientific-rigor`, `statistics`, `subagents`, `workflow`.

### Credit

Eureka's plugin architecture, SessionStart hook mechanism, rigid-vs-flexible skill distinction, rationalization tables, red-flag checklists, iron laws, and subagent review pattern are directly modeled on [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent.

[Unreleased]: https://github.com/jeonnoin-alt/Eureka/compare/v1.10.1...HEAD
[1.10.1]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.10.1
[1.10.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.10.0
[1.9.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.9.0
[1.8.1]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.8.1
[1.8.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.8.0
[1.7.1]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.7.1
[1.7.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.7.0
[1.6.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.6.0
[1.5.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.5.0
[1.4.1]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.4.1
[1.4.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.4.0
[1.3.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.3.0
[1.2.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.2.0
[1.1.2]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.1.2
[1.1.1]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.1.1
[1.1.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.1.0
[1.0.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.0.0
