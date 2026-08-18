# Machine-readable eval corpus

`cases.json` mirrors the repository's seed evaluation cases in a deterministic format that can be validated in CI and consumed by future model-evaluation runners.

This corpus does not claim that a model has passed an evaluation. The current CI validates schema, coverage, and repository consistency only. Model execution and scoring require a separate runner and should report the model, prompt or skill version, sampling settings, and scoring method.

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
