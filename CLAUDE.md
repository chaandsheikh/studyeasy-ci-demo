# SupportDesk - project context for Claude Code (also read in CI)

## Review criteria
- Money: a refund must never be more than what the customer paid for the order.
- Privacy: never log or print a customer's email, phone or address.
- Every change to `supportdesk/prompts.py` must pass the eval gate (`evals/ci_gate.py`).
- Report real problems only: bugs, security, privacy. No style comments.

## Testing standards
- Tests live in `tests/`, one file per module, run with `pytest`.
- A valuable test checks a rule from this file or an edge case. Skip tests that repeat an existing one.

## Fixtures
- `order_total` (tests/conftest.py): the standard test order, 40.00.
