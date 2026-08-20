from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evals.runner import EvalRunnerError, RunMetadata, Score, load_corpus, run_cases, write_report

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "evals" / "cases.json"


class EvalRunnerTests(unittest.TestCase):
    def test_load_corpus_returns_cases_and_sha256(self):
        cases, digest = load_corpus(CORPUS_PATH)
        self.assertGreater(len(cases), 0)
        self.assertEqual(len(digest), 64)
        int(digest, 16)

    def test_run_cases_records_reproducibility_metadata_and_summary(self):
        cases, digest = load_corpus(CORPUS_PATH)
        selected = cases[:3]

        def generate(case):
            return f"candidate response for {case['id']}"

        def score(case, response):
            passed = case["id"] != selected[-1]["id"]
            return Score(
                passed=passed,
                rationale="fixture scorer decision",
                expected_met=(case["expected"][0],) if passed else (),
                forbidden_found=() if passed else (case["forbidden"][0],),
            )

        metadata = RunMetadata(
            model="fixture-model",
            skill_revision="f3bf53bca26b1c738567d38e724c03e520549fba",
            scorer="fixture-scorer-v1",
            sampling={"temperature": 0},
        )
        report = run_cases(
            selected,
            generate=generate,
            score=score,
            metadata=metadata,
            corpus_sha256=digest,
        )

        self.assertEqual(report["summary"]["total"], 3)
        self.assertEqual(report["summary"]["passed"], 2)
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertAlmostEqual(report["summary"]["pass_rate"], 2 / 3)
        self.assertEqual(report["metadata"]["model"], "fixture-model")
        self.assertEqual(report["corpus_sha256"], digest)
        self.assertEqual([item["case_id"] for item in report["results"]], [case["id"] for case in selected])

    def test_empty_generator_response_fails_closed(self):
        cases, digest = load_corpus(CORPUS_PATH)
        metadata = RunMetadata(
            model="fixture-model",
            skill_revision="test-revision",
            scorer="fixture-scorer-v1",
            sampling={},
        )

        with self.assertRaises(EvalRunnerError):
            run_cases(
                cases[:1],
                generate=lambda case: "",
                score=lambda case, response: Score(True, "unused"),
                metadata=metadata,
                corpus_sha256=digest,
            )

    def test_empty_scorer_rationale_fails_closed(self):
        cases, digest = load_corpus(CORPUS_PATH)
        metadata = RunMetadata(
            model="fixture-model",
            skill_revision="test-revision",
            scorer="fixture-scorer-v1",
            sampling={},
        )

        with self.assertRaises(EvalRunnerError):
            run_cases(
                cases[:1],
                generate=lambda case: "candidate response",
                score=lambda case, response: Score(True, ""),
                metadata=metadata,
                corpus_sha256=digest,
            )

    def test_write_report_round_trips_json(self):
        report = {"schema_version": 1, "summary": {"total": 1, "passed": 1}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            write_report(report, path)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), report)


if __name__ == "__main__":
    unittest.main()
