# studyeasy-ci-demo

A small slice of SupportDesk, a Python support agent, used to show CI on GitHub Actions.

- `supportdesk/` the system prompt, a stand-in model (no API key) and the refund code
- `evals/` the golden set, its baseline from main, and the CI eval gate
- `tests/` unit tests and fixtures
- `.github/workflows/eval-gate.yml` unit tests + the eval gate on every pull request
- `.github/workflows/claude-review.yml` Claude Code (`claude -p`) reviews the diff and posts inline comments
- `.github/CODEOWNERS` and `.github/pull_request_template.md` review and sign-off

Run locally: `pip install anthropic pytest`, then `pytest -q` and `python evals/ci_gate.py`.
