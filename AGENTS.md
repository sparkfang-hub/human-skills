# Repository instructions for agents

This repository contains wellbeing-oriented Agent Skills. Treat wording changes as behavior changes.

Before editing a skill, read:

- `docs/design-principles.md`
- `docs/safety-model.md`
- the target skill's complete `SKILL.md`
- any references inside that skill directory

Non-negotiable rules:

1. Do not turn a skill into diagnosis, treatment, or medical advice.
2. Do not add medication guidance, personalized sleep restriction, or promises of symptom relief.
3. Do not infer another person's motives from silence, response time, social activity, or partial evidence.
4. Do not help users bypass blocks, pressure contact, harass, monitor, manipulate, blackmail, or threaten self-harm for a response.
5. Do not add dependency-forming language, exclusivity, secrecy, or claims that the AI is a human relationship.
6. When immediate safety may be at risk, the skill must prioritize local human or emergency support over its normal workflow.
7. Keep each skill self-contained. An installer may copy only that skill directory.
8. Keep the active instructions concise. Supporting explanation belongs in `references/`.
9. Do not add scripts that access the network, credentials, unrelated files, or external commands.
10. Update validation, tests, packaged `.skill` files, and the changelog with every behavior change.

Run all repository checks before opening a pull request:

```bash
python scripts/check_skills.py
python scripts/check_markdown_links.py
python -m unittest discover -s tests -v
python scripts/package_skills.py --check
```
