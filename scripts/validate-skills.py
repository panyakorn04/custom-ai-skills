#!/usr/bin/env python3
"""Validate repo-managed SKILL.md files."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "ai" / "skills"
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_CONTENT_CHARS = 100_000
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    """Parse the flat scalar fields this validator needs without external deps."""
    data: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            data[key] = value
    return data


def validate_skill(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")

    if len(content) > MAX_SKILL_CONTENT_CHARS:
        errors.append(f"{path}: file is larger than {MAX_SKILL_CONTENT_CHARS} chars")

    if not content.startswith("---"):
        errors.append(f"{path}: frontmatter must start at byte 0 with ---")
        return errors

    match = re.search(r"\n---\s*\n", content[3:])
    if not match:
        errors.append(f"{path}: missing closing frontmatter delimiter")
        return errors

    frontmatter_text = content[3 : match.start() + 3]
    body = content[match.end() + 3 :].strip()

    frontmatter = parse_simple_frontmatter(frontmatter_text)

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not name:
        errors.append(f"{path}: missing non-empty name")
    elif not NAME_PATTERN.match(name):
        errors.append(f"{path}: invalid name {name!r}; use lowercase letters, numbers, hyphens, or underscores, <=64 chars")

    if not isinstance(description, str) or not description:
        errors.append(f"{path}: missing non-empty description")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f"{path}: description exceeds {MAX_DESCRIPTION_LENGTH} chars")
    elif not description.startswith("Use when "):
        errors.append(f"{path}: description should start with 'Use when '")

    for recommended in ("version", "author", "license"):
        if recommended not in frontmatter:
            errors.append(f"{path}: missing recommended frontmatter field {recommended!r}")

    if not body:
        errors.append(f"{path}: body must not be empty")

    if not re.search(r"^## When to Use\s*$", body, flags=re.MULTILINE):
        errors.append(f"{path}: missing '## When to Use' section")

    if not re.search(r"^## Verification Checklist\s*$", body, flags=re.MULTILINE):
        errors.append(f"{path}: missing '## Verification Checklist' section")

    return errors


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/*/SKILL.md"))
    if not skill_files:
        print(f"No SKILL.md files found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for skill_file in skill_files:
        all_errors.extend(validate_skill(skill_file))

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(skill_files)} skill file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
