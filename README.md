# Eureka

Eureka is a complete research rigor workflow for your coding agents, built on top of a set of composable "skills" and some initial instructions that make sure your agent uses them.

It is the research-workflow counterpart to [Superpowers](https://github.com/obra/superpowers) — same plugin architecture, same skill system, same "rigid discipline through mandatory skills" philosophy. Where Superpowers enforces test-driven development and code review for software, Eureka enforces hypothesis pre-registration, statistical rigor, claims auditing, and reproducibility for scientific work.

## How it works

It starts from the moment you open a research conversation with your agent. As soon as it sees that you're about to run an experiment or make a scientific claim, it *doesn't* just jump into analysis. Instead, it steps back and asks you what you're really trying to test.

Once it's teased a research question out of the conversation, it walks you through nine mandatory questions — null hypothesis, falsifiability criterion, primary outcome, confounds, statistical power, contradictory evidence, data provenance — and refuses to proceed until they all have clear answers. One question at a time. Multiple choice when possible.

After you've approved the design, the agent registers the hypothesis to version control **before** touching any data. Statistical test, significance threshold, data version hash, preprocessing pipeline version — all committed as a pre-registration record. Deviations from the pre-registered plan are allowed, but they must be explicitly labeled as exploratory.

When experiments fail or produce unexpected results, the agent runs a systematic troubleshooting process — reading logs, reproducing the issue, checking for data leakage, tracing the pipeline stage by stage — before proposing any explanation. No post-hoc rationalization.

Before you submit anything, the agent runs a multi-dimensional research review (7 independent dimensions scored out of 100), a full claims audit (every number in the manuscript traced to a source file, every figure verified as script-generated, all experiments — including negative ones — accounted for), and a fresh reproducibility check. If any gate fails, submission is blocked.

There's a bunch more to it, but that's the core of the system. And because the skills trigger automatically, you don't need to do anything special. Your research agent just has Eureka.

## Credit

Eureka is modeled directly on [Superpowers](https://github.com/obra/superpowers) by [Jesse Vincent](https://blog.fsck.com). The plugin architecture, session-start hook mechanism, rigid-vs-flexible skill distinction, rationalization tables, red-flag checklists, iron laws, and subagent review pattern are all borrowed from Superpowers. If you do software engineering as well as research, install both — they share a namespace convention and were designed to coexist.

## Installation

### Claude Code (via Plugin Marketplace)

In Claude Code, register this repository as a marketplace, then install:

```bash
/plugin marketplace add jeonnoin-alt/Eureka
/plugin install eureka
```

### Manual Installation

Clone this repository into your Claude Code plugins cache:

```bash
git clone https://github.com/jeonnoin-alt/Eureka ~/.claude/plugins/cache/eureka/eureka/1.0.0
```

Then restart Claude Code. The `SessionStart` hook will automatically inject the `using-eureka` bootstrap skill at the start of every new session.

### Verify Installation

Start a new Claude Code session and ask for something that should trigger a skill:

- "I want to run an experiment comparing Model A and Model B" → should invoke `research-brainstorming`
- "My baseline results look wrong" → should invoke `systematic-troubleshooting`
- "I finished the analysis, ready to write up" → should invoke `requesting-research-review`

The agent should automatically announce which skill it is using.

## The Research Workflow

1. **research-brainstorming** — Activates when a research question is detected. Explores the idea through nine mandatory questions (H0, falsifiability, primary outcome, confounds + data leakage, power, alternative explanation, prior work, contradictory evidence, data provenance). Presents the design in sections for validation. Saves a research design document.

2. **hypothesis-first** — Activates after design approval. The scientific equivalent of test-driven development. Forces you to commit H1, H0, exact statistical test, significance threshold, data version hash, and preprocessing version to version control **before** any data is analyzed. No analysis without a registered hypothesis.

3. **experiment-design** — Activates with a registered hypothesis. Breaks the design into bite-sized experiment tasks with exact data paths, version hashes, configs, seeds, and commands. Every task produces committable output.

4. **systematic-troubleshooting** — Activates when an experiment fails or produces unexpected results. A four-phase process (Investigate → Pattern Analysis → Hypothesis → Resolution) that blocks you from re-running with a different seed until root cause is identified.

5. **requesting-research-review** — Activates when an experiment phase is complete. Dispatches a `research-reviewer` subagent that scores the work across seven independent dimensions (Scientific Foundation, Methodological Rigor, Experimental Execution, Results Quality, Novelty, Reproducibility, Domain Standards). All seven must meet the threshold to PASS.

6. **claims-audit** — Activates during manuscript writing. Traces every quantitative claim to a source file, verifies every figure is script-generated, and confirms that all experiments (including negative ones) are reported. Unreported null results are flagged as publication bias.

7. **verification-before-publication** — Activates before submission. Fresh verification of every claim, regeneration of every figure from scripts, end-to-end reproducibility check (raw → processed → analysis → results with a single command), and confirmation that the `research-reviewer` score meets the pre-submission threshold.

8. **submission-readiness** — Activates after verification passes. Presents four structured options: submit to target journal, preprint first then submit, continue refining, or pivot. Forces explicit documentation of the decision.

**The agent checks for relevant skills before any task.** Mandatory workflows, not suggestions.

## What's Inside

### Skills Library

**Design & Registration**
- **research-brainstorming** — Nine-question Socratic design refinement
- **hypothesis-first** — Pre-register H1, H0, analysis plan, and data version before analysis
- **experiment-design** — Break approved designs into executable, versioned tasks

**Execution & Debugging**
- **systematic-troubleshooting** — Four-phase root cause investigation for failed experiments

**Review**
- **requesting-research-review** — Dispatch a seven-dimension scientific rigor review
- **receiving-research-review** — Respond to review feedback with technical rigor, not performative agreement

**Publication Gates**
- **claims-audit** — Trace every number, verify every figure, report every experiment
- **verification-before-publication** — Fresh evidence for every claim before submission
- **submission-readiness** — Four-option decision gate for finished work

**Meta**
- **using-eureka** — Bootstrap skill that teaches the agent to auto-invoke Eureka skills

### Agents

- **research-reviewer** — Senior research reviewer that scores work across seven dimensions and produces a Gap-to-Threshold analysis for failing dimensions. Dispatched via `requesting-research-review`.

### Reference Documents

- **docs/references/statistical-guide.md** — Test selection, effect size interpretation, multiple comparison correction
- **docs/references/data-checklist.md** — Data provenance, preprocessing, leakage taxonomy, missing value handling, split strategies

### Templates

- **docs/templates/research-design-doc.md** — Output of `research-brainstorming`
- **docs/templates/research-review-report.md** — Output of `research-reviewer`

## Philosophy

- **Hypothesis before data** — The scientific TDD. Register the prediction before you can possibly know the answer.
- **Evidence before claims** — No publication claim without fresh verification.
- **Null results are results** — Report all experiments, including the ones that failed to support your hypothesis. Selective reporting is p-hacking by omission.
- **Systematic over ad-hoc** — Root cause investigation beats re-running with a different seed.
- **Reproducibility is not retrofittable** — Data version, seeds, configs, and environment must be locked from day one.

## Coexistence with Superpowers

Eureka and Superpowers are designed to work side by side. They share the same plugin architecture and session-start hook mechanism. Both hooks fire; both `using-*` bootstrap skills are injected at session start. Claude uses the appropriate namespace for the task:

| Task | Namespace |
|---|---|
| Writing or refactoring code | `superpowers:*` |
| Running or writing about experiments | `eureka:*` |
| Software design | `superpowers:brainstorming` |
| Research design | `eureka:research-brainstorming` |
| Code review | `superpowers:code-reviewer` |
| Scientific review | `eureka:research-reviewer` |

Use the namespace that matches the artifact: **code → Superpowers**, **science → Eureka**.

## Contributing

Skills live directly in this repository. To contribute a new skill or improve an existing one:

1. Fork the repository
2. Create a branch for your skill
3. Follow the structure of existing `SKILL.md` files (see `skills/hypothesis-first/SKILL.md` as a canonical example)
4. Every new discipline-enforcing skill should include an Iron Law, a rationalization table, and red-flag checklist
5. Submit a PR

## License

MIT License — see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Jesse Vincent](https://blog.fsck.com) for Superpowers, whose architecture and discipline-through-skills philosophy this plugin directly borrows from.
