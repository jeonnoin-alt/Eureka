#!/usr/bin/env python3
"""Check that eureka:<skill-name> references point to real skills or agents.

Scans every markdown file in the repository (excluding .git and dependencies)
and finds eureka:<name> tokens. Each must resolve to either:
- skills/<name>/SKILL.md, or
- agents/<name>.md

Fails CI if any reference is broken.
"""

import re
import sys
from pathlib import Path

REFERENCE_PATTERN = re.compile(r"eureka:([a-z][a-z0-9-]*)")
EXCLUDE_DIRS = {".git", "node_modules", ".github"}


def collect_real_names(repo_root: Path) -> set[str]:
    """Collect names of all real skills and agents."""
    names: set[str] = set()
    skills_dir = repo_root / "skills"
    if skills_dir.is_dir():
        for skill_md in skills_dir.glob("*/SKILL.md"):
            names.add(skill_md.parent.name)
    agents_dir = repo_root / "agents"
    if agents_dir.is_dir():
        for agent_md in agents_dir.glob("*.md"):
            names.add(agent_md.stem)
    return names


def find_markdown_files(repo_root: Path) -> list[Path]:
    """Find all markdown files, excluding common irrelevant directories."""
    md_files: list[Path] = []
    for path in repo_root.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        md_files.append(path)
    return sorted(md_files)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    real_names = collect_real_names(repo_root)
    if not real_names:
        print("ERROR: no skills or agents found", file=sys.stderr)
        return 1

    md_files = find_markdown_files(repo_root)
    if not md_files:
        print("ERROR: no markdown files found", file=sys.stderr)
        return 1

    broken_refs: list[tuple[Path, int, str]] = []
    total_refs = 0
    for md_file in md_files:
        try:
            lines = md_file.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(lines, start=1):
            for match in REFERENCE_PATTERN.finditer(line):
                ref_name = match.group(1)
                total_refs += 1
                if ref_name not in real_names:
                    rel = md_file.relative_to(repo_root)
                    broken_refs.append((rel, lineno, ref_name))

    if broken_refs:
        print("Cross-reference check FAILED:", file=sys.stderr)
        for rel, lineno, ref_name in broken_refs:
            print(f"  - {rel}:{lineno}: 'eureka:{ref_name}' does not exist", file=sys.stderr)
        print(
            f"\nReal skills/agents available: {sorted(real_names)}",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {total_refs} eureka:* references across {len(md_files)} files all resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
