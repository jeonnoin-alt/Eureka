#!/usr/bin/env python3
"""Validate Eureka SKILL.md files have proper frontmatter.

Checks:
- Every SKILL.md has a YAML frontmatter block delimited by ---
- Required fields present (name, description)
- Only allowed Claude Code skill frontmatter fields used
- name field matches the parent directory name
"""

import re
import sys
from pathlib import Path

ALLOWED_FIELDS = {
    "name",
    "description",
    "argument-hint",
    "compatibility",
    "disable-model-invocation",
    "license",
    "metadata",
    "user-invokable",
}
REQUIRED_FIELDS = {"name", "description"}


def parse_frontmatter(content: str) -> dict | None:
    """Extract top-level keys from YAML frontmatter (simple parser).

    Returns dict of {field_name: raw_value_string} or None if no frontmatter.
    """
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        return None
    block = m.group(1)
    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in block.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line and not line[0].isspace() and ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            current_key = key
            fields[key] = value.strip()
        elif current_key is not None and line.strip():
            fields[current_key] += " " + line.strip()
    return fields


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        print(f"ERROR: {skills_dir} does not exist", file=sys.stderr)
        return 1

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print(f"ERROR: no SKILL.md files found under {skills_dir}", file=sys.stderr)
        return 1

    errors: list[str] = []
    for skill_file in skill_files:
        rel = skill_file.relative_to(repo_root)
        content = skill_file.read_text(encoding="utf-8")
        fields = parse_frontmatter(content)
        if fields is None:
            errors.append(f"{rel}: missing frontmatter block (--- ... ---)")
            continue

        present = set(fields.keys())
        missing = REQUIRED_FIELDS - present
        if missing:
            errors.append(f"{rel}: missing required fields: {sorted(missing)}")

        unsupported = present - ALLOWED_FIELDS
        if unsupported:
            errors.append(f"{rel}: unsupported frontmatter fields: {sorted(unsupported)}")

        # Verify name matches parent directory
        name = fields.get("name", "").strip().strip('"').strip("'")
        expected_name = skill_file.parent.name
        if name and name != expected_name:
            errors.append(f"{rel}: name '{name}' does not match directory '{expected_name}'")

        # Verify description is non-empty
        description = fields.get("description", "").strip()
        if not description:
            errors.append(f"{rel}: description is empty")

    if errors:
        print("Skill validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: validated {len(skill_files)} SKILL.md files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
