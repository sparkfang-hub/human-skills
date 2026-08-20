from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

Generator = Callable[[dict[str, Any]], str]
Scorer = Callable[[dict[str, Any], str], "Score"]


@dataclass(frozen=True)
class Score:
    passed: bool
    rationale: str
    expected_met: tuple[str, ...] = ()
    forbidden_found: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunMetadata:
    model: str
    skill_revision: str
    scorer: str
    sampling: dict[str, Any]


class EvalRunnerError(ValueError):
    pass


def load_corpus(path: str | Path) -> tuple[list[dict[str, Any]], str]:
    corpus_path = Path(path)
    raw = corpus_path.read_bytes()
    data = json.loads(raw.decode("utf-8"))

    if data.get("schema_version") != 1:
        raise EvalRunnerError("unsupported eval corpus schema_version")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise EvalRunnerError("eval corpus must contain a non-empty cases list")

    case_ids: list[str] = []
    for case in cases:
        if not isinstance(case, dict):
            raise EvalRunnerError("every eval case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise EvalRunnerError("every eval case must have a non-empty id")
        case_ids.append(case_id)

    if len(case_ids) != len(set(case_ids)):
        raise EvalRunnerError("eval case ids must be unique")

    return cases, hashlib.sha256(raw).hexdigest()


def run_cases(
    cases: Iterable[dict[str, Any]],
    *,
    generate: Generator,
    score: Scorer,
    metadata: RunMetadata,
    corpus_sha256: str,
) -> dict[str, Any]:
    case_list = list(cases)
    if not case_list:
        raise EvalRunnerError("at least one eval case is required")
    if not metadata.model.strip():
        raise EvalRunnerError("metadata.model must be non-empty")
    if not metadata.skill_revision.strip():
        raise EvalRunnerError("metadata.skill_revision must be non-empty")
    if not metadata.scorer.strip():
        raise EvalRunnerError("metadata.scorer must be non-empty")
    if len(corpus_sha256) != 64:
        raise EvalRunnerError("corpus_sha256 must be a SHA-256 hex digest")
    try:
        int(corpus_sha256, 16)
    except ValueError as exc:
        raise EvalRunnerError("corpus_sha256 must be a SHA-256 hex digest") from exc

    results: list[dict[str, Any]] = []
    for case in case_list:
        response = generate(case)
        if not isinstance(response, str) or not response.strip():
            raise EvalRunnerError(f"generator returned an empty response for {case['id']}")

        judgement = score(case, response)
        if not isinstance(judgement, Score):
            raise EvalRunnerError("scorer must return Score")
        if not judgement.rationale.strip():
            raise EvalRunnerError(f"scorer returned an empty rationale for {case['id']}")

        results.append(
            {
                "case_id": case["id"],
                "skill": case["skill"],
                "mode": case["mode"],
                "domain": case["domain"],
                "response": response,
                "score": asdict(judgement),
            }
        )

    passed = sum(result["score"]["passed"] for result in results)
    total = len(results)

    return {
        "schema_version": 1,
        "metadata": asdict(metadata),
        "corpus_sha256": corpus_sha256,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total,
        },
        "results": results,
    }


def write_report(report: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
