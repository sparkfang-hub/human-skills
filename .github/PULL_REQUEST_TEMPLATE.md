## What changed

Describe the human situation and the exact agent behavior change.

## Why

Explain why a reusable skill is better than a one-off prompt for this case.

## Safety review

- [ ] No diagnosis, treatment, medication, or false medical claim was added.
- [ ] No motive-reading, harassment, coercion, surveillance, or boundary bypass was added.
- [ ] Immediate-danger handling remains clear.
- [ ] The skill has a stopping point and does not encourage dependency.
- [ ] Packaged `.skill` files were regenerated.

## Validation

- [ ] `python scripts/check_skills.py`
- [ ] `python scripts/check_markdown_links.py`
- [ ] `python -m unittest discover -s tests -v`
- [ ] `python scripts/package_skills.py --check`
