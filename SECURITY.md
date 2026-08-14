# Security policy

Human Skills contains instructions rather than executable application code, but Agent Skills still create a security boundary. A malicious or careless instruction can direct an agent to access credentials, execute unrelated commands, reveal private information, or manipulate a vulnerable user.

## Reportable issues

Please report:

- instructions that request secrets, tokens, cookies, private messages, or unrelated files;
- hidden or misleading behavior that is not described in the skill;
- prompt-injection paths that override safety boundaries;
- commands that download or execute remote code;
- dependency-forming, coercive, harassment-enabling, or crisis-mishandling behavior;
- packaged `.skill` files that do not match their readable source;
- unsafe installation instructions.

For non-sensitive issues, open a GitHub issue with the smallest reproducible example.

For sensitive issues, use GitHub private vulnerability reporting if it is available in the repository's Security tab. If it is unavailable, do not post secrets or exploit details publicly; open a minimal issue requesting a private contact channel.

## Scope

The project does not collect user data, run a service, make network requests, or require credentials. The canonical source is the readable content under `skills/`. Packaged files under `dist/` are deterministically generated and checked in CI.
