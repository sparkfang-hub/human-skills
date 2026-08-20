# Machine-readable eval corpus

`cases.json` mirrors the repository's seed evaluation cases in a deterministic format that can be validated in CI and consumed by model-evaluation runners.

The repository now includes a provider-neutral runner core in `evals/runner.py`. It executes a corpus through caller-supplied generator and scorer functions, then records reproducibility metadata, the exact corpus SHA-256, per-case responses and judgments, and aggregate pass/fail counts.

The runner deliberately does not access the network, credentials, model-provider SDKs, or external commands. A caller may connect a model outside this repository and inject its generator/scorer functions. This keeps provider credentials and paid execution out of the skill package while making the evaluation contract testable in CI.

A completed run should record:

- `model`: the exact model or local checkpoint identifier
- `skill_revision`: the exact Human Skills commit or immutable revision under test
- `scorer`: the judge or rubric version
- `sampling`: relevant generation settings such as temperature or seed
- `corpus_sha256`: the exact hash of `cases.json`
- each case response, pass/fail decision, rationale, expected behaviors observed, and forbidden behaviors found

This corpus and runner do not claim that any model has passed an evaluation until real model outputs have been generated and scored. The current repository CI validates the corpus structure and tests runner mechanics with deterministic fixtures; it does not call live models.

## Schema

Each case contains:

- `id`: stable unique identifier
- `skill`: one Human Skill or `cross-skill`
- `mode`: `single_turn` or `trajectory`
- `domain`: the scenario domain
- `input` or `turns`: reproducible scenario input
- `expected`: behaviors a passing response should preserve
- `forbidden`: regressions the case is designed to catch

Keep this file and `docs/evaluation-cases.md` aligned when adding or materially changing evaluation coverage.

## Runner API

A model adapter can stay outside the repository and call the runner like this:

```python
from evals.runner import RunMetadata, Score, load_corpus, run_cases

cases, corpus_hash = load_corpus("evals/cases.json")

report = run_cases(
    cases,
    generate=my_model_adapter,
    score=my_eval_judge,
    metadata=RunMetadata(
        model="exact-model-id",
        skill_revision="exact-commit-sha",
        scorer="judge-or-rubric-version",
        sampling={"temperature": 0},
    ),
    corpus_sha256=corpus_hash,
)
```

`my_model_adapter(case)` must return a non-empty response string. `my_eval_judge(case, response)` must return a `Score` with a pass/fail decision and non-empty rationale. The runner fails closed when either side returns incomplete data.
