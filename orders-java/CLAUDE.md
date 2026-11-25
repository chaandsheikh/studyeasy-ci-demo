# Orders service - project context for Claude Code (also read in CI)

## Review criteria
- Money: use `BigDecimal`, never `double` or `float`. A refund must never be more than what the customer paid for the order.
- Privacy: never log or print a customer's email, phone or address. Log the customer id.
- Every new business rule gets a test in `src/test/java`.
- Report real problems only: bugs, security, privacy. No style comments.

## Testing standards
- JUnit 5, one test class per class under test, run with `mvn test`.
- A valuable test checks a rule from this file or an edge case. Skip tests that repeat an existing one.

## Fixtures
- `orderTotal` in `RefundServiceTest`: the standard test order, 40.00.
