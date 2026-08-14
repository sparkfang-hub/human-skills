#!/usr/bin/env python3
"""Validate Human Skills source files without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DEPENDENCY_PHRASES = (
    "you only need me",
    "do not tell anyone",
    "don't tell anyone",
    "keep this between us",
    "i am your therapist",
    "i am your doctor",
    "i am your partner",
    "i am all you need",
)


class ValidationError(Exception):
    """Raised when a skill package violates repository rules."""


def parse_skill(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValidationError(f"{path}: missing opening YAML frontmatter")
    try:
        raw_frontmatter, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValidationError(f"{path}: missing closing YAML frontmatter") from exc

    metadata: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValidationError(f"{path}: invalid frontmatter line {line!r}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    return metadata, body


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    try:
        metadata, body = parse_skill(path)
    except ValidationError as exc:
        return [str(exc)]

    name = metadata.get("name", "")
    description = metadata.get("description", "")

    if name != skill_dir.name:
        errors.append(f"{path}: name {name!r} must match folder {skill_dir.name!r}")
    if not NAME_RE.fullmatch(name):
        errors.append(f"{path}: name must use lowercase letters, digits, and hyphens")
    if len(description) < 80:
        errors.append(f"{path}: description is too short to route safely")
    if len(description) > 1024:
        errors.append(f"{path}: description exceeds 1024 characters")
    if not body.lstrip().startswith("# "):
        errors.append(f"{path}: body must start with an H1")
    if len(body.split()) > 1800:
        errors.append(f"{path}: body exceeds the 1800-word context budget")

    lowered = body.lower()
    for phrase in DEPENDENCY_PHRASES:
        if phrase in lowered:
            errors.append(f"{path}: prohibited dependency phrase {phrase!r}")

    if "safety" not in lowered:
        errors.append(f"{path}: must include an explicit safety section")
    if "diagnos" not in lowered:
        errors.append(f"{path}: must state a diagnosis boundary")
    if "immediate" not in lowered and "emergency" not in lowered:
        errors.append(f"{path}: must describe immediate-danger handling")
    if "stop" not in lowered and "end" not in lowered:
        errors.append(f"{path}: must define a stopping or exit condition")

    return errors


def validate_marketplace(skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{MARKETPLACE}: {exc}"]

    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        return [f"{MARKETPLACE}: plugins must be a non-empty list"]

    listed: set[str] = set()
    for plugin in plugins:
        for relative in plugin.get("skills", []):
            path = (ROOT / relative).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{MARKETPLACE}: skill path escapes repository: {relative}")
                continue
            if not (path / "SKILL.md").is_file():
                errors.append(f"{MARKETPLACE}: missing skill path {relative}")
            listed.add(path.name)

    if listed != skill_names:
        errors.append(
            f"{MARKETPLACE}: listed skills {sorted(listed)} "
            f"do not match source skills {sorted(skill_names)}"
        )
    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print("skills directory is missing", file=sys.stderr)
        return 1

    skill_dirs = sorted(
        path for path in SKILLS_DIR.iterdir() if path.is_dir() and not path.name.startswith(".")
    )
    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))
    errors.extend(validate_marketplace({path.name for path in skill_dirs}))

    if errors:
        print("Human Skills validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills: {', '.join(path.name for path in skill_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
