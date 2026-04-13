# Gemini CLI Tool Mapping

Eureka skills use Claude Code tool names. When you encounter these references in a skill, use your Gemini CLI equivalent:

| Skill references | Gemini CLI equivalent |
|---|---|
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search file content) | `grep_search` |
| `Glob` (search files by name) | `glob` |
| `TodoWrite` (task tracking) | `write_todos` |
| `Skill` tool (invoke a skill) | `activate_skill` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `Task` tool (dispatch subagent) | No equivalent — Gemini CLI does not support subagents |

## No subagent support

Gemini CLI has no equivalent to Claude Code's `Task` tool. The `eureka:research-reviewer` agent — which is normally dispatched as a subagent via `eureka:requesting-research-review` — must be run inline in a Gemini CLI session instead.

When `requesting-research-review` would dispatch a subagent in Claude Code:

1. Read the agent prompt at `agents/research-reviewer.md`
2. Fill the template placeholders (`{RESEARCH_QUESTION}`, `{DESIGN_DOC_PATH}`, `{RESULTS_PATHS}`, `{PHASE_DESCRIPTION}`, `{DOMAIN_CONTEXT}`, `{TARGET_VENUE}`, `{PASS_THRESHOLD}`)
3. Execute the review logic in the current session, following the 7-dimension scoring framework from the agent file
4. Produce the structured review report as the session's output

The discipline of the review (evidence-only scoring, Gap-to-Threshold analysis, severity stratification) is preserved — only the dispatch mechanism differs.

## Additional Gemini CLI tools Eureka can leverage

These Gemini tools have no Claude Code equivalent but are useful for research workflows:

| Tool | How Eureka uses it |
|---|---|
| `save_memory` | Persists facts to `GEMINI.md` across sessions — useful for cross-project insights surfaced by `eureka:research-journal` |
| `ask_user` | Structured input for `eureka:research-brainstorming`'s nine mandatory questions |
| `tracker_create_task` | Richer alternative to the TodoWrite-style checklists used by rigid skills |
| `enter_plan_mode` / `exit_plan_mode` | Read-only research mode — good for `eureka:whats-next`'s project state scan before making recommendations |

## Required behavior

Gemini CLI loads Eureka via the `gemini-extension.json` manifest and the `GEMINI.md` context file. The `@./skills/using-eureka/SKILL.md` import ensures the bootstrap skill is injected at session start, just like the Claude Code SessionStart hook. From there, Eureka skills activate via Gemini's native `activate_skill` tool when their trigger descriptions match the user's request.
