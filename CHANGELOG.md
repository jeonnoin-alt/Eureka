# Changelog

All notable changes to Eureka will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/jeonnoin-alt/Eureka/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.1.0
[1.0.0]: https://github.com/jeonnoin-alt/Eureka/releases/tag/v1.0.0
