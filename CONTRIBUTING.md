# Contributing

Human Skills welcomes careful contributions. This repository is small on purpose: every sentence can change how an agent behaves when a person is tired, distressed, angry, lonely, or uncertain.

## Before proposing a new skill

A good Human Skill should meet all of these conditions:

- The situation is common enough that a reusable protocol is useful.
- The skill changes agent behavior, not merely tone.
- The workflow can be explained without pretending to diagnose or treat.
- The skill has a clear stopping point.
- It helps the user return to an offline decision, person, activity, or source of care.
- The likely benefit is greater than the risk of false certainty, dependency, escalation, or manipulation.

A narrow skill is better than a broad "life coach."

## Skill structure

```text
skills/
  your-skill-name/
    SKILL.md
    references/
      optional-reference.md
```

The folder name and frontmatter `name` must match. Use lowercase letters, digits, and hyphens.

Required frontmatter:

```yaml
---
name: your-skill-name
description: Explain what it does, when it should activate, and important exclusions.
---
```

Keep the primary workflow in `SKILL.md`. Put evidence notes, long examples, and source links under `references/`.

## Writing standard

Prefer:

- one low-effort question at a time;
- concrete observations over labels;
- choices over commands;
- short responses when the user is activated;
- explicit uncertainty;
- a clear exit from the conversation.

Avoid:

- generic praise or scripted empathy;
- long checklists at the beginning;
- diagnostic labels;
- reading motives into missing information;
- repeated reassurance that feeds rumination;
- "I am always here," "you only need me," or similar dependency cues;
- content designed to maximize engagement.

## Safety review

Every new skill must state:

- what it is for;
- what it is not for;
- how it handles immediate danger or self-harm language;
- which actions it will not assist;
- when it should stop and hand back control.

Read `docs/safety-model.md` before drafting.

## Validation

Run:

```bash
python scripts/check_skills.py
python scripts/check_markdown_links.py
python -m unittest discover -s tests -v
python scripts/package_skills.py
python scripts/package_skills.py --check
```

Commit source and regenerated `dist/*.skill` files together.

## Pull requests

Explain:

- the human situation being addressed;
- the exact behavior change;
- misuse or safety risks considered;
- examples before and after;
- validation performed.

Do not include private conversations, identifying personal information, copyrighted therapy manuals, proprietary prompts, or clinical claims without appropriate primary sources.
