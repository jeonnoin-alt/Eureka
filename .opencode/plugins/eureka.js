/**
 * Eureka plugin for OpenCode.ai
 *
 * Injects the Eureka bootstrap context via system prompt transform.
 * Auto-registers the skills directory via config hook (no symlinks needed).
 *
 * Modeled directly on Jesse Vincent's superpowers plugin for OpenCode.
 */

import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Simple frontmatter extraction (avoid external dependencies for bootstrap)
const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };

  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};

  for (const line of frontmatterStr.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }

  return { frontmatter, content: body };
};

// Normalize a path: trim whitespace, expand ~, resolve to absolute
const normalizePath = (p, homeDir) => {
  if (!p || typeof p !== 'string') return null;
  let normalized = p.trim();
  if (!normalized) return null;
  if (normalized.startsWith('~/')) {
    normalized = path.join(homeDir, normalized.slice(2));
  } else if (normalized === '~') {
    normalized = homeDir;
  }
  return path.resolve(normalized);
};

export const EurekaPlugin = async ({ client, directory }) => {
  const homeDir = os.homedir();
  const eurekaSkillsDir = path.resolve(__dirname, '../../skills');
  const envConfigDir = normalizePath(process.env.OPENCODE_CONFIG_DIR, homeDir);
  const configDir = envConfigDir || path.join(homeDir, '.config/opencode');

  // Helper to generate bootstrap content from the using-eureka skill
  const getBootstrapContent = () => {
    const skillPath = path.join(eurekaSkillsDir, 'using-eureka', 'SKILL.md');
    if (!fs.existsSync(skillPath)) return null;

    const fullContent = fs.readFileSync(skillPath, 'utf8');
    const { content } = extractAndStripFrontmatter(fullContent);

    const toolMapping = `**Tool Mapping for OpenCode:**
When Eureka skills reference Claude Code tool names you don't have, substitute OpenCode equivalents:
- \`TodoWrite\` → \`todowrite\`
- \`Task\` tool with subagents → Use OpenCode's subagent system (@mention)
- \`Skill\` tool → OpenCode's native \`skill\` tool
- \`Read\`, \`Write\`, \`Edit\`, \`Bash\` → Your native tools

**Skills location:**
Eureka skills are in \`${eurekaSkillsDir}\`.
Use OpenCode's native \`skill\` tool to list and load skills — skill names are prefixed with \`eureka/\` (e.g. \`eureka/research-brainstorming\`, \`eureka/hypothesis-first\`, \`eureka/whats-next\`).

**research-reviewer agent:**
Eureka's \`research-reviewer\` is normally dispatched as a subagent via \`eureka:requesting-research-review\`. In OpenCode, use the \`@mention\` subagent syntax to dispatch it inline, or run the review logic in the current session by reading \`agents/research-reviewer.md\` directly.`;

    return `<EXTREMELY_IMPORTANT>
You have Eureka — a research rigor plugin.

**IMPORTANT: The using-eureka skill content is included below. It is ALREADY LOADED — you are currently following it. Do NOT use the skill tool to load "using-eureka" again; that would be redundant.**

${content}

${toolMapping}
</EXTREMELY_IMPORTANT>`;
  };

  return {
    // Inject the Eureka skills path into OpenCode's live config so that
    // OpenCode discovers the skills without requiring symlinks or config edits.
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(eurekaSkillsDir)) {
        config.skills.paths.push(eurekaSkillsDir);
      }
    },

    // Use system prompt transform to inject the bootstrap content at session start.
    'experimental.chat.system.transform': async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (bootstrap) {
        (output.system ||= []).push(bootstrap);
      }
    }
  };
};
