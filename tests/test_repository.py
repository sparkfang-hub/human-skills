from __future__ import annotations

import json
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {"sleep-with-me", "dont-text-them", "stop-the-spiral"}


class RepositoryTests(unittest.TestCase):
    def test_expected_skill_set(self):
        actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_readme_surfaces_each_skill_and_installation(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills add sparkfang-hub/human-skills", text)
        self.assertIn("/plugin marketplace add sparkfang-hub/human-skills", text)
        for name in EXPECTED_SKILLS:
            self.assertIn(name, text)

    def test_marketplace_paths_exist(self):
        data = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        listed = set()
        for plugin in data["plugins"]:
            for relative in plugin["skills"]:
                path = ROOT / relative
                self.assertTrue((path / "SKILL.md").is_file())
                listed.add(path.name)
        self.assertEqual(listed, EXPECTED_SKILLS)

    def test_packaged_skills_are_readable_and_self_contained(self):
        for name in EXPECTED_SKILLS:
            archive_path = ROOT / "dist" / f"{name}.skill"
            self.assertTrue(archive_path.is_file())
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
                self.assertIn("SKILL.md", names)
                self.assertNotIn("../", " ".join(names))
                source = (ROOT / "skills" / name / "SKILL.md").read_bytes()
                self.assertEqual(archive.read("SKILL.md"), source)

    def test_skills_reject_dependency_and_coercion_patterns(self):
        combined = "\n".join(
            (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8").lower()
            for name in EXPECTED_SKILLS
        )
        for prohibited in (
            "you only need me",
            "keep this between us",
            "bypass a block",
        ):
            if prohibited == "bypass a block":
                self.assertIn(prohibited, combined)
            else:
                self.assertNotIn(prohibited, combined)

        self.assertIn("do not help the user", combined)
        self.assertIn("immediate danger", combined)


if __name__ == "__main__":
    unittest.main()
