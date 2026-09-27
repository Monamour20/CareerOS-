# Mathematical Detail Checklist — Generic

## Purpose

Use this checklist whenever a project contains numbers, scores, percentages, dates, limits, rates, probabilities, rankings, analytics, algorithms, AI outputs, or business metrics.

The goal is simple:

> **Every number must have a clear meaning, correct calculation, correct unit, correct boundary, and correct use.**

---

# 1. Define Every Quantity

- [ ] Every important variable has a clear definition.
- [ ] The meaning of every number is documented.
- [ ] Similar quantities have different names when their meanings differ.
- [ ] No variable has two different meanings in different parts of the system.
- [ ] Inputs, intermediate values, and outputs are clearly separated.
- [ ] Optional values such as `null` are handled explicitly.

### Example

If the system contains:

```text
score = 82
document whether 82 means:

82 out of 100
82%
82 points
0.82 normalized score

These are not automatically the same thing.

# 2.Units and Dimensions
 Every physical quantity has a unit.
 Time values clearly state seconds, minutes, hours, days, or timestamps.
 Money values clearly state the currency.
 Percentages and ratios are not mixed accidentally.
 Bytes, KB, MB, and GB are clearly distinguished.
 Counts are not treated as percentages.
 Unit conversions are tested.
 The same unit is used consistently across the system.
Example
0.75

and

75%

may represent the same idea, but the system must define which representation it uses internally.

# 3.Boundaries and Off-by-One Errors
 Minimum values are defined.
 Maximum values are defined.
 It is documented whether boundaries are inclusive or exclusive.
 Empty input is tested.
 Single-item input is tested.
 Maximum-size input is tested.
 Values just below important thresholds are tested.
 Values exactly at important thresholds are tested.
 Values just above important thresholds are tested.

For a rule such as:

score >= 70

test:

69
70
71

# 4.Percentages, Ratios, and Scores
 The numerator is clearly defined.
 The denominator is clearly defined.
 Division by zero is handled.
 Percentage conversion is explicit.
 Weighted scores sum to the intended total.
 Scores stay within their documented range.
 Normalization is documented.
 Rounding happens at the correct stage.
 Ratios are not accidentally displayed as percentages.
 Percentages are not accidentally treated as raw numbers.
Basic percentage
percentage = (part / total) * 100

Always define what part and total mean.

# 5.Rounding and Precision
 Required precision is documented.
 Internal calculations keep enough precision.
 Rounding normally happens at the presentation boundary.
 Floating-point comparisons use safe tolerances where appropriate.
 Currency calculations use suitable precision.
 Repeated rounding does not create avoidable errors.
 Backend and frontend use compatible rounding rules.
 Database precision is sufficient for the calculation.

# 6. Date and Time Mathematics
 The time zone is known.
 Date-only values are separated from timestamps.
 Start and end boundaries are defined.
 Duration calculations are correct.
 Expiration rules are explicit.
 Future and past dates are validated.
 Sorting uses actual timestamps where required.
 Date arithmetic is tested around boundaries.
 Invalid date ranges are rejected.
 Time units are consistent.

# 7. Counts and Aggregates
For every count:
 What exactly is being counted?
 Are duplicates possible?
 Are deleted or inactive records included?
 Are null values included?
 Is the count per user, project, day, or global?
 Is pagination affecting the result?
 Are filtered records included or excluded intentionally?
Average
average = sum(values) / number_of_values

Check the denominator carefully.

Also verify:

 Empty collections are handled.
 Zero values are handled correctly.
 Duplicate values are handled intentionally.

# 8. Rates and Probabilities
 Numerator and denominator represent the same population.
 The observation period is clear.
 Zero observations are handled.
 Probability values stay between 0 and 1.
 Percentage values stay between 0% and 100%.
 Estimated values are separated from measured values.
 Sample size is considered before interpreting a rate.
 The time period used for the rate is documented.
Example
success_rate =
successful_events / total_events

Verify that both values refer to the same group and time period.

# 9.Limits and Capacity
 Maximum input size is defined.
 Maximum database result size is defined.
 Pagination limits are documented.
 API rate limits are documented.
 Retry limits are documented.
 Timeout values are documented.
 Memory limits are considered.
 Storage limits are considered.
 Behavior at the exact limit is tested.
 Behavior above the limit is tested.

# 10. Data Types and Serialization
 Integer vs floating-point values are intentional.
 Decimal values preserve the required precision.
 JSON serialization preserves the intended meaning.
 Database numeric types match application types.
 Dates serialize consistently.
 Booleans are represented consistently.
 Large integers cannot overflow the selected type.
 null and zero are not confused.
 Empty strings and missing values are handled intentionally.

# 11. Algorithms and Invariants

For every important algorithm:

 Input assumptions are documented.
 Output guarantees are documented.
 Important invariants are identified.
 Best-case behavior is considered.
 Average-case behavior is considered where useful.
 Worst-case behavior is considered.
 Time complexity is understood.
 Space complexity is understood.
 Ordering assumptions are documented.
 Duplicate handling is defined.
 Edge cases are tested.
Example invariant

The calculated score must always remain between 0 and 100.

# 12. State and Concurrency
 Counters cannot be incorrectly updated by concurrent requests.
 Duplicate requests are handled safely.
 Retry operations do not double-count results.
 Database transactions protect related calculations.
 Race conditions are considered.
 State transitions have valid conditions.
 Repeated execution produces the intended result.
 Idempotent operations remain idempotent.

# 13. Database Mathematics
 Aggregations use the correct rows.
 Joins do not accidentally multiply records.
 One-to-one relationships are actually one-to-one.
 Unique constraints match business rules.
 Counts are checked after joins.
 Null handling is correct.
 Pagination does not change aggregate meaning.
 Historical values are not accidentally replaced when history matters.
 Database constraints agree with application calculations.
 Duplicate records cannot silently distort metrics.

# 14. API and UI Consistency
 Backend and frontend use the same units.
 Backend and frontend use the same score range.
 Labels match calculations.
 A value displayed as a percentage is actually a percentage.
 Empty values have clear behavior.
 Loading states do not show false values.
 Cached values do not conflict with current values.
 Formatting does not change the underlying value.
 The API schema matches the UI expectation.
 No frontend-only calculation contradicts backend business logic.

# 15. AI/ML Quantitative Checks
 AI-generated numbers are never treated as automatically correct.
 Deterministic calculations are performed by application code when possible.
 AI output is schema-validated.
 AI output is business-validated.
 Scores have documented ranges.
 Confidence values have defined meanings.
 AI is not allowed to invent numeric facts.
 Source data is preserved for traceability.
 Model-generated estimates are separated from verified values.
 AI cannot override deterministic business rules without explicit design.
 Numeric claims generated by AI can be traced back to source evidence.

# 16. Testing Matrix

For every important formula or threshold, test:

Case	Required
Empty input	[ ]
One item	[ ]
Normal input	[ ]
Minimum boundary	[ ]
Maximum boundary	[ ]
Just below threshold	[ ]
Exact threshold	[ ]
Just above threshold	[ ]
Invalid input	[ ]
Duplicate input	[ ]
Null/missing input	[ ]
Very large input	[ ]

# 17. Final Number Audit

Before declaring a feature complete:

 Search the code for hard-coded thresholds.
 Search for percentage calculations.
 Search for score calculations.
 Search for divisions.
 Search for averages.
 Search for date arithmetic.
 Search for retry counts.
 Search for timeout values.
 Search for pagination limits.
 Search for minimum constraints.
 Search for maximum constraints.
 Compare backend calculations with frontend displays.
 Check tests for boundary coverage.
 Check documentation against actual implementation.
 Check whether the same formula is implemented in multiple places.
 Remove conflicting duplicate calculations where appropriate.
 18. Feature-Level Mathematical Review

Before a feature is considered mathematically complete:

Definition
 Every important quantity has a definition.
 Every formula has documented inputs.
 Every output has a documented meaning.
Range
 Minimum value is known.
 Maximum value is known.
 Invalid values are rejected.
Formula
 Formula is documented.
 Numerator is defined.
 Denominator is defined.
 Units are defined.
 Rounding behavior is defined.
Boundaries
 Minimum boundary tested.
 Maximum boundary tested.
 Just below threshold tested.
 Exact threshold tested.
 Just above threshold tested.
Integration
 Database agrees with backend.
 Backend agrees with API.
 API agrees with frontend.
 Documentation agrees with implementation.
 Tests agree with business rules.

# 19. Final Project Audit

Before a project is considered complete:

 All important formulas are documented.
 All important thresholds are documented.
 All score ranges are documented.
 All percentages have defined denominators.
 All rates have defined time periods.
 All date calculations have defined boundaries.
 All limits have defined behavior.
 All AI-generated quantitative values are validated.
 All deterministic calculations have automated tests.
 Boundary cases are tested.
 Backend and frontend calculations agree.
 Database constraints agree with business rules.
 Documentation agrees with implementation.
 No unexplained magic numbers remain.
 No conflicting formulas exist.
 No hidden assumptions remain in important calculations.

# 20. Golden Rule
Never allow a number to exist without knowing what it means, how it was calculated, what its valid range is, what its units are, and what happens at its boundaries.

For every important number, ask:
What does it mean?
Where did it come from?
How was it calculated?
What is its valid range?
What are its units?
What happens at the boundaries?
Can the result be independently verified?

If these questions cannot be answered, the number is not ready to be trusted.