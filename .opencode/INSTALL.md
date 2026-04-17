# Installing Eureka for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add Eureka to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["eureka@git+https://github.com/jeonnoin-alt/Eureka.git"]
}
```

Restart OpenCode. The plugin auto-installs and registers all Eureka skills via OpenCode's skill discovery.

Verify by asking:

> Tell me about your Eureka research skills.

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to list skills
use skill tool to load eureka/research-brainstorming
use skill tool to load eureka/hypothesis-first
use skill tool to load eureka/whats-next
```

Or just describe a research task — the bootstrap injection teaches the agent to auto-invoke the right Eureka skill.

## Pinning a version

To lock to a specific release (recommended for production research projects where reproducibility matters):

```json
{
  "plugin": ["eureka@git+https://github.com/jeonnoin-alt/Eureka.git#v1.8.1"]
}
```

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i eureka`
2. Verify the plugin line in your `opencode.json`
3. Make sure you're running a recent version of OpenCode

### Skills not found

1. Use the `skill` tool to list what OpenCode discovered
2. Check that the plugin is loading (see above)
3. Confirm your `opencode.json` has the plugin line, not just installed it via CLI

### Tool mapping

When Eureka skills reference Claude Code tool names:

- `TodoWrite` → `todowrite`
- `Skill` tool → OpenCode's native `skill` tool
- `Task` tool with subagents → OpenCode's `@mention` syntax
- `Read`, `Write`, `Edit`, `Bash` → your native tools

The JavaScript plugin (`.opencode/plugins/eureka.js`) injects this mapping into the system prompt automatically at session start, so the agent knows the translations without you having to memorize them.

## Updating

Eureka updates automatically when you restart OpenCode (unless you pinned a specific version tag).

## Uninstalling

Remove the Eureka line from your `opencode.json` `plugin` array and restart OpenCode.

## Getting Help

- Report issues: https://github.com/jeonnoin-alt/Eureka/issues
