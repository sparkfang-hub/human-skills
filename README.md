# Human Skills

**Skills for the parts of life that do not come with documentation.**

Most Agent Skills teach AI how to write code, deploy software, or operate tools. Human Skills teaches compatible AI agents what to do when the task is human:

- you cannot sleep, and a twelve-point sleep-hygiene lecture will only wake you up;
- you want to send a message you may regret tomorrow;
- your brain has turned one unanswered question into a complete disaster story.

The goal is not to turn an AI into a therapist. The goal is to make it a calmer, safer, more useful companion for a difficult moment.

> Human Skills should help you return to your life, not keep you talking to an AI.

[繁體中文說明](README.zh-TW.md)

## The difference

Without a skill:

> I am sorry you are experiencing difficulty sleeping. Here are ten strategies that may improve sleep quality...

With `sleep-with-me`:

> Okay. No life decisions tonight. Is your body still awake, or is one thought refusing to leave?

Without a skill:

> Based on the delayed response, there may be several possible explanations...

With `stop-the-spiral`:

> Let us separate what happened from what your brain is predicting. What do we know for sure?

The intelligence stays. The unnecessary attitude, certainty, and lecture disappear.

## Available skills

| Skill | Use it when |
| --- | --- |
| [`sleep-with-me`](skills/sleep-with-me/) | You cannot fall asleep, woke during the night, or need low-stimulation company while your mind slows down. |
| [`dont-text-them`](skills/dont-text-them/) | You are activated and about to send a message that may be accusatory, pleading, repetitive, or regrettable. |
| [`stop-the-spiral`](skills/stop-the-spiral/) | Rumination, catastrophizing, or uncertainty has started turning into unsupported conclusions. |

Each skill is a small, inspectable `SKILL.md` package following the open Agent Skills format. There are no model calls, accounts, trackers, remote scripts, or runtime dependencies in the skills.

## Install

### Cross-agent installer

List the skills:

```bash
npx skills add sparkfang-hub/human-skills --list
```

Install one skill globally:

```bash
npx skills add sparkfang-hub/human-skills \
  --skill sleep-with-me \
  --global
```

Install all three and choose the supported agents interactively:

```bash
npx skills add sparkfang-hub/human-skills
```

The open `skills` CLI supports Claude Code, Codex, Cursor, OpenCode, and many other Agent Skills hosts.

### Claude Code marketplace

```text
/plugin marketplace add sparkfang-hub/human-skills
/plugin install human-skills@human-skills
```

### Claude.ai or another upload-based host

Download a packaged `.skill` file and upload it through the host's custom-skill interface:

- [`sleep-with-me.skill`](dist/sleep-with-me.skill)
- [`dont-text-them.skill`](dist/dont-text-them.skill)
- [`stop-the-spiral.skill`](dist/stop-the-spiral.skill)

A `.skill` file is a ZIP archive containing the same readable files found under `skills/`.

### Manual installation

Copy one skill directory into the skills directory used by your agent. Common project locations include:

```text
.agents/skills/        Codex and several cross-agent hosts
.claude/skills/        Claude Code
.cursor/skills/        Cursor
```

## Example requests

```text
I cannot sleep. Keep this quiet and simple.
```

```text
I am angry and about to send this message. Help me decide whether it should be sent.
```

```text
My manager barely spoke to me in the meeting and my brain has decided they think I am incompetent. Separate facts from guesses.
```

```text
I had one expensive month and now I keep imagining financial disaster. Help me separate what I know from what I am predicting.
```

```text
My ankle feels strange after training and I keep jumping straight to permanent damage. Help me separate the symptom from the story without dismissing a real injury.
```

Skills can activate automatically from their descriptions, or you can ask the agent to use one by name.

## Design promises

Human Skills aims to be:

- warm without fake intimacy;
- brief when the user is overloaded;
- honest about uncertainty;
- useful without pretending to diagnose or treat;
- protective of consent, boundaries, and the recipient of a message;
- willing to stop analysis when more analysis would feed rumination;
- ready to hand off to human or emergency support when safety is at risk.

Human Skills will not:

- claim to be a person, therapist, doctor, crisis line, or substitute for care;
- interpret silence, response times, or social-media activity as proof of another person's motives;
- help bypass blocks, pressure someone, harass them, or use self-harm threats to obtain a reply;
- give medication instructions, prescribe sleep schedules, or promise that a technique will make someone sleep;
- encourage secrecy, exclusivity, dependency, or replacing human relationships with an AI.

Read the [design principles](docs/design-principles.md), [safety model](docs/safety-model.md), and [seed evaluation cases](docs/evaluation-cases.md) for the current standard and regression coverage.

## Evidence and scope

The sleep skill uses conservative ideas consistent with public guidance from sleep-medicine and health organizations: do not force sleep, reduce stimulation, and leave the bed for a quiet activity if wakefulness has become frustrating. It deliberately does not implement a personalized sleep-restriction program or medical treatment. See the skill's [evidence and boundaries](skills/sleep-with-me/references/evidence-and-boundaries.md).

The communication and rumination skills are non-clinical interaction protocols. They introduce time, separate observation from inference, and reduce coercive or impulsive communication. They do not diagnose attachment styles, anxiety disorders, OCD, trauma, or any other condition.

## Development

The repository has no runtime dependencies. Validate everything with:

```bash
python scripts/check_skills.py
python scripts/check_markdown_links.py
python -m unittest discover -s tests -v
python scripts/package_skills.py --check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a skill.

## Status

This project is new and intentionally conservative. Real-world feedback is welcome, especially reports of language that feels cold, patronizing, overly clinical, manipulative, dependency-forming, or unsafe.

## License

MIT. See [LICENSE](LICENSE).
