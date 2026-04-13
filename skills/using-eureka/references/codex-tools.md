# Codex Tool Mapping

Eureka skills use Claude Code tool names. When you encounter these references in a skill, use your Codex equivalent:

| Skill references | Codex equivalent |
|---|---|
| `Task` tool (dispatch subagent) | `spawn_agent` (see Named agent dispatch below) |
| Multiple `Task` calls (parallel) | Multiple `spawn_agent` calls |
| Task returns result | `wait` |
| Task completes automatically | `close_agent` to free slot |
| `TodoWrite` (task tracking) | `update_plan` |
| `Skill` tool (invoke a skill) | Skills load natively — just follow the instructions |
| `Read`, `Write`, `Edit` (files) | Use your native file tools |
| `Bash` (run commands) | Use your native shell tools |
| `Grep` (search file content) | Use your native search tool |
| `Glob` (search files by name) | Use your native file listing |

## Subagent dispatch requires multi-agent support

Add to your Codex config (`~/.codex/config.toml`):

```toml
[features]
multi_agent = true
```

This enables `spawn_agent`, `wait`, and `close_agent` — required for `eureka:requesting-research-review`, which dispatches the seven-dimension `research-reviewer` subagent.

## Named agent dispatch (eureka:research-reviewer)

Claude Code skills reference named agent types like `eureka:research-reviewer`. Codex does not have a named agent registry — `spawn_agent` creates generic agents from built-in roles (`default`, `explorer`, `worker`).

When `eureka:requesting-research-review` says to dispatch the `research-reviewer` agent:

1. Read the agent prompt at `agents/research-reviewer.md` (in the Eureka repo)
2. Fill any template placeholders:
   - `{RESEARCH_QUESTION}`
   - `{PHASE_DESCRIPTION}`
   - `{DESIGN_DOC_PATH}`
   - `{RESULTS_PATHS}`
   - `{DOMAIN_CONTEXT}`
   - `{TARGET_VENUE}`
   - `{PASS_THRESHOLD}`
3. Spawn a `worker` agent with the filled content as the `message`

### Message framing

The `message` parameter is user-level input, not a system prompt. Structure it for maximum instruction adherence:

```
Your task is to perform the following research review. Follow the instructions below exactly.

<agent-instructions>
[filled content from agents/research-reviewer.md]
</agent-instructions>

Execute this now. Output ONLY the structured review report following the format specified in the instructions above.
```

- Use task-delegation framing ("Your task is...") rather than persona framing ("You are...")
- Wrap instructions in XML tags — the model treats tagged blocks as authoritative
- End with an explicit execution directive to prevent summarization of the instructions

### When this workaround can be removed

This approach compensates for Codex's plugin system not yet supporting an `agents` field in `plugin.json`. When Codex gains native named-agent support, Eureka can symlink `agents/` alongside `skills/` and `requesting-research-review` can dispatch by name directly.

## File paths that skills expect

Several Eureka skills read or write files in predictable locations:

| Skill | Writes to |
|---|---|
| `research-brainstorming` | `docs/eureka/designs/YYYY-MM-DD-<topic>-design.md` |
| `hypothesis-first` | `docs/eureka/registrations/YYYY-MM-DD-<study-id>-registration.md` |
| `experiment-design` | `docs/eureka/plans/YYYY-MM-DD-<topic>-experiments.md` |
| `claims-audit` | `docs/eureka/audits/YYYY-MM-DD-claims-audit.md` |
| `research-journal` | `docs/eureka/journal/YYYY-MM-DD.md` |

Use your native file tools to create these directories and files. The skills will guide you through the content.

## Environment detection

Skills that touch git (like `hypothesis-first` committing the registration) should detect their environment with read-only git commands before proceeding:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `BRANCH` empty → detached HEAD (cannot commit registration; inform the user)
- Not in a git repo → skill should warn and offer to initialize one
