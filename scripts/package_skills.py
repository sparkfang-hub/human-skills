#!/usr/bin/env python3
"""Build deterministic .skill ZIP archives from readable skill folders."""

from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DEFAULT_OUTPUT = ROOT / "dist"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def build_archive(skill_dir: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in skill_dir.rglob("*") if item.is_file()):
            relative = path.relative_to(skill_dir).as_posix()
            info = zipfile.ZipInfo(relative, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    args.output.mkdir(parents=True, exist_ok=True)
    stale: list[str] = []

    for skill_dir in skill_dirs:
        destination = args.output / f"{skill_dir.name}.skill"
        expected = build_archive(skill_dir)
        if args.check:
            if not destination.is_file() or destination.read_bytes() != expected:
                stale.append(str(destination.relative_to(ROOT)))
        else:
            destination.write_bytes(expected)
            print(f"Wrote {destination.relative_to(ROOT)}")

    if stale:
        print("Packaged skills are missing or stale:", file=sys.stderr)
        for path in stale:
            print(f"- {path}", file=sys.stderr)
        print("Run: python scripts/package_skills.py", file=sys.stderr)
        return 1

    if args.check:
        print(f"Verified {len(skill_dirs)} deterministic .skill archives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
