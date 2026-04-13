# Installing Eureka for Codex

Enable Eureka research rigor skills in Codex via native skill discovery. Clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the Eureka repository:**
   ```bash
   git clone https://github.com/jeonnoin-alt/Eureka.git ~/.codex/eureka
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/eureka/skills ~/.agents/skills/eureka
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\eureka" "$env:USERPROFILE\.codex\eureka\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Enable subagent dispatch

Eureka's `research-reviewer` agent is normally dispatched as a subagent via `eureka:requesting-research-review`. To enable this in Codex, add to your `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

This enables `spawn_agent`, `wait`, and `close_agent` — required for the seven-dimension research review. See `skills/using-eureka/references/codex-tools.md` for the full tool mapping.

## Verify

```bash
ls -la ~/.agents/skills/eureka
```

You should see a symlink (or junction on Windows) pointing to your Eureka skills directory.

In Codex, ask:

> I just installed Eureka. What skills do you have?

The agent should be able to list the Eureka skills and describe what each one does.

## Updating

```bash
cd ~/.codex/eureka && git pull
```

Skills update instantly through the symlink — no reinstall needed.

## Uninstalling

```bash
rm ~/.agents/skills/eureka
```

Optionally delete the clone: `rm -rf ~/.codex/eureka`.
