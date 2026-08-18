from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "evals" / "cases.json"
EXPECTED_SKILLS = {"sleep-with-me", "dont-text-them", "stop-the-spiral"}
EXPECTED_MODES = {"single_turn", "trajectory"}


class EvalCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
        cls.cases = cls.data["cases"]

    def test_schema_version_and_nonempty_cases(self):
        self.assertEqual(self.data["schema_version"], 1)
        self.assertGreater(len(self.cases), 0)

    def test_case_ids_are_unique(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_case_shape(self):
        for case in self.cases:
            self.assertTrue(case["id"].strip())
            self.assertIn(case["mode"], EXPECTED_MODES)
            self.assertTrue(case["domain"].strip())
            self.assertGreater(len(case["expected"]), 0)
            self.assertGreater(len(case["forbidden"]), 0)

            if case["skill"] != "cross-skill":
                self.assertIn(case["skill"], EXPECTED_SKILLS)

            if case["mode"] == "single_turn":
                self.assertTrue(case["input"].strip())
                self.assertNotIn("turns", case)
            else:
                self.assertGreaterEqual(len(case["turns"]), 2)
                self.assertNotIn("input", case)

    def test_each_skill_has_multiple_cases(self):
        for skill in EXPECTED_SKILLS:
            count = sum(case["skill"] == skill for case in self.cases)
            self.assertGreaterEqual(count, 3, skill)

    def test_trajectory_coverage_exists(self):
        trajectory_domains = {
            case["domain"] for case in self.cases if case["mode"] == "trajectory"
        }
        self.assertIn("dependency", trajectory_domains)
        self.assertIn("safety", trajectory_domains)

    def test_cross_domain_coverage_exists(self):
        domains = {case["domain"] for case in self.cases}
        for domain in ("work", "money", "health", "parenting", "customer"):
            self.assertIn(domain, domains)


if __name__ == "__main__":
    unittest.main()
