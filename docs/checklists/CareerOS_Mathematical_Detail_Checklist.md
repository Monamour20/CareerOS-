# CareerOS Mathematical Detail Checklist

## Purpose

This checklist is specific to CareerOS.

Use it whenever CareerOS calculates a score, percentage, gap, count, rate, duration, recommendation category, analytics value, retry count, timeout, limit, or other numeric result.

The main rule is:

> **CareerOS must calculate numbers deterministically when the rules are known, validate AI-generated numbers, and keep the meaning of every number consistent across the backend, database, API, and UI.**

---

# 1. Job Match Score

CareerOS currently uses a deterministic Job Match Score with a range of 0–100.

## Current Weighting

| Component | Weight |
|---|---:|
| Role | 25 |
| Skills | 45 |
| Seniority | 10 |
| Industry | 10 |
| Experience | 10 |
| **Total** | **100** |

## Checklist

- [ ] Every component produces a value compatible with the final 0–100 score.
- [ ] The weights total exactly 100.
- [ ] Role contributes at most 25 points.
- [ ] Skills contributes at most 45 points.
- [ ] Seniority contributes at most 10 points.
- [ ] Industry contributes at most 10 points.
- [ ] Experience contributes at most 10 points.
- [ ] Final score is clamped to 0–100.
- [ ] No negative final score is possible.
- [ ] No final score above 100 is possible.
- [ ] Existing JobMatchingService remains the owner of deterministic match scoring.
- [ ] JD Intelligence does not create a second overall match score.

---

# 2. Skill Matching

CareerOS compares candidate skills against job skills.

## Required-Skill Coverage

```text
required_skill_coverage =
matched_required_skills / total_required_skills

## Checklist
Numerator = required skills that are actually matched.
Denominator = total required skills.
Zero required skills has explicit behavior.
Coverage stays between 0 and 1.
Percentage display converts the value correctly.
Required and preferred skills are kept separate.
A skill cannot be both matched and missing.
Skill normalization is consistent.
Skill aliases are handled consistently.
Duplicate skills do not inflate the score.
Missing required skills are separate from missing preferred skills.
Current Recommendation Rule

Jobs with less than 50% required-skill match are excluded.

Skill-gap recommendations can still appear when required-skill coverage is at least 50%.
49%
50%
51%

# 3. Job Recommendation Thresholds

Current CareerOS recommendation thresholds:

Category	                   Threshold
Potential	                      40+
Strong	                          70+
Excellent	                      85+
Below recommendation minimum	Below 40

Current minimum recommendation score:
40
# Checklist
 Score below 40 is excluded.
 Score = 40 is tested.
 Score = 69 is tested.
 Score = 70 is tested.
 Score = 84 is tested.
 Score = 85 is tested.
 Score = 100 is tested.
 Category boundaries are identical in backend and frontend.
 UI labels match backend categories.
 Recommendation thresholds are not duplicated with conflicting values.

 # 4. Job Recommendation Candidate Limits
CareerOS currently defines:
MAX_CANDIDATES = 100

# Checklist
 Candidate generation cannot exceed the intended limit.
 Pagination is not confused with candidate generation.
 Filtering does not change the meaning of the score.
 Empty candidate sets are handled correctly.
 Candidate limits are documented.
 Boundary behavior at the candidate limit is tested.

 # 5. JD Intelligence — Requirement Classification

JD Intelligence separates:

Required skills
Preferred skills
Experience requirements
Education requirements
Certification requirements
Responsibilities

# Checklist
 Required and preferred lists are disjoint after normalization.
 Requirements are supported by the job description.
 Required/preferred classification is based on job-description wording.
 AI does not invent requirements.
 Existing deterministic job skills are not blindly treated as semantically required.
 Qwen does not calculate the overall match score.
 CareerOS application logic remains responsible for deterministic calculations.
 Requirement lists are validated before being used by later features.

 6. JD Intelligence — Skill Gap

Required values:

skills_you_have
missing_required_skills
missing_preferred_skills
gap_severity
Checklist
 skills_you_have comes from verified Career Vault information.
 A skill cannot appear in both skills_you_have and a missing list.
 Required missing skills are separate from preferred missing skills.
 Gap severity has documented thresholds.
 Gap severity is calculated consistently.
 Empty required skills have defined behavior.
 The same normalized skill is not counted twice.
 JD Intelligence does not produce a second overall match score.
 Skill-gap calculations use normalized skill names.
Recommended Implementation Rule

Use Qwen for semantic classification and explanation; use CareerOS deterministic logic for final quantitative conclusions.

7. Career Vault Completeness

Career Vault contains structured career information.

Potential completeness areas include:

Personal information
Education
Experience
Skills
Projects
Certifications
Achievements
Career interests
Checklist
 Completeness has a documented formula.
 Every section has a documented contribution if percentages are used.
 Missing sections do not cause division-by-zero errors.
 Empty optional sections are distinguished from invalid data.
 Completeness does not claim information exists when it was not verified.
 UI percentage matches backend calculation.
 Adding or removing an item changes completeness only according to the documented rule.
 The maximum completeness value is defined.
 The minimum completeness value is defined.
8. Career Experience Mathematics

CareerOS stores experience information such as:

Start dates
End dates
Titles
Employers
Technologies
Responsibilities
Checklist
 Duration uses the correct dates.
 Current roles are handled without requiring an end date.
 End date cannot precede start date.
 Date-only and timestamp values are not mixed carelessly.
 Overlapping experiences are handled intentionally.
 Experience is not double-counted when records overlap.
 Years of experience are not invented from incomplete dates.
 Months and years are calculated consistently.
 Boundary dates are tested.
 Time zone behavior is defined where timestamps are involved.
9. Resume Intelligence — Numeric Truth

Resume Intelligence must preserve evidence from the uploaded resume.

Sensitive numeric facts can include:

Years of experience
Percent improvements
Revenue
User counts
Performance improvements
Project metrics
Rankings
Dates
Durations
Certification counts
Checklist
 Numbers are extracted from source evidence.
 AI does not invent metrics.
 Units are preserved.
 Percentages are not converted incorrectly.
 Dates are preserved accurately.
 Similar numbers from different sections are not merged incorrectly.
 Missing numbers remain missing.
 Resume analysis does not turn an estimate into a verified fact.
 Numeric claims can be traced back to resume evidence.
 Rewriting does not silently change numeric facts.
10. Job Ingestion — Duplicate Identity

CareerOS job ingestion uses provider identity information.

Checklist
 External job identity is stable.
 Provider/source is part of identity where required.
 Duplicate jobs do not create duplicate records.
 Upsert operations preserve the intended record.
 Job skills are not duplicated during repeated ingestion.
 Re-ingesting the same job does not change counts incorrectly.
 Created and updated timestamps have clear meanings.
 Duplicate detection is tested with repeated ingestion.
11. Job Timestamps

CareerOS jobs can contain:

posted_at
expires_at
created_at
updated_at
Checklist
 Each timestamp has a defined meaning.
 Time zones are handled consistently.
 Expiration is not confused with database update time.
 A job is not treated as expired solely because its database record is old.
 Invalid timestamp ordering is detected where relevant.
 Frontend formatting does not change the underlying timestamp.
 Date comparisons use actual timestamp values.
 Boundary dates are tested.
12. Application Intelligence

When Application Intelligence is implemented, define every rate mathematically.

Example
application_success_rate =
successful_applications / total_applications
Checklist
 Denominator is explicitly defined.
 Withdrawn or cancelled applications have defined treatment.
 Duplicate applications do not inflate the denominator.
 Zero applications do not cause division by zero.
 Time period is explicit.
 User-specific and global metrics are not mixed.
 Rates are not presented as percentages unless converted correctly.
 The same application cannot be counted twice.
 Status definitions are documented.
13. Career Analytics

For every Career Analytics metric:

 Metric name is defined.
 Numerator is defined.
 Denominator is defined.
 Time period is defined.
 User population is defined.
 Data source is defined.
 Missing-data behavior is defined.
 Zero-data behavior is defined.
 Duplicate records are handled.
 Historical values are preserved where required.
 Frontend and backend use the same formula.
 Metric units are documented.
 Metric ranges are documented.
Future Metrics May Include
Applications submitted
Interviews received
Interview rate
Offer rate
Application-to-interview conversion
Application-to-offer conversion
Skill-gap frequency
Opportunity activity
Career progress over time
14. Resume Studio — Quantitative Truth

Resume Studio must not create unsupported numbers.

Checklist
 Resume bullet metrics come from Career Vault or user-provided evidence.
 AI cannot create fake percentages.
 AI cannot create fake revenue figures.
 AI cannot create fake user counts.
 AI cannot create fake performance improvements.
 Original numeric evidence is preserved when rewriting.
 Unit changes are validated.
 Date changes are prevented unless supported by evidence.
 Numeric claims remain consistent between Career Vault and generated resume content.
 User approval is required before unsupported information could enter the final resume.
15. Interview Intelligence

If CareerOS introduces interview scoring:

 Score range is defined.
 Each criterion has a defined weight.
 Weights total the intended maximum.
 Partial scores have clear meanings.
 Empty answers have defined behavior.
 AI feedback is separated from deterministic scoring.
 AI cannot silently change the scoring formula.
 Score changes are traceable to the input.
 The same answer is scored consistently under the same rules.
 Boundary scores are tested.
Example
final_score =
criterion_1 * weight_1 +
criterion_2 * weight_2 +
criterion_3 * weight_3

Document whether criterion scores are normalized to 0–1 or 0–100 before applying weights.

16. Application Automation

When controlled application automation is implemented:

Retry Mathematics
 Maximum retry count is defined.
 Retry count starts at the documented value.
 Failed attempts are not counted as successful applications.
 A successful retry cannot create a duplicate application.
 Retry behavior is deterministic.
 Retry limits are tested at their boundaries.
Timeout Mathematics
 Page timeout is defined.
 Action timeout is defined.
 Overall workflow timeout is defined.
 Timeout units are consistent.
 Timeout behavior is tested.
Rate Limits
 Maximum requests/actions per time period are defined.
 Rate-limit windows are explicit.
 Waiting time is calculated correctly.
 Automation stops when the configured limit is reached.
 Rate-limit counters do not reset incorrectly.
17. AI vs Deterministic Mathematics

Use deterministic application code when the rule is mathematical and known.

Deterministic
Match score
Recommendation thresholds
Required-skill coverage
Percentages
Counts
Dates
Retry counts
Timeouts
Limits
Database constraints
AI-Assisted
Semantic requirement classification
Natural-language insights
Semantic skill interpretation
Explanation generation
Checklist
 Qwen is not used for calculations CareerOS can perform exactly.
 AI-generated numeric values are validated.
 AI cannot override business rules.
 AI cannot create unsupported career facts.
 Deterministic services remain the source of truth for quantitative rules.
 AI output is validated before affecting downstream calculations.
 AI-generated conclusions are traceable to supplied data.
18. Cross-Feature Consistency

The same career fact must mean the same thing everywhere.

Checklist
 Career Vault skill list matches Job Matching skill input.
 Job Matching and JD Intelligence use the same skill normalization rules.
 Job Recommendation thresholds match the recommendation service.
 Resume Studio uses the same verified Career Vault facts.
 Application Intelligence uses the same application records.
 Career Analytics uses the same source records.
 Interview Intelligence does not invent career facts.
 Frontend values match backend values.
 Database values match API values.
 The same formula is not implemented differently in multiple services.
 Shared mathematical rules have one clear source of truth.
19. CareerOS Number Audit

Before completing any feature:

 Search for hard-coded numeric thresholds.
 Search for percentage calculations.
 Search for score calculations.
 Search for divisions.
 Search for minimum constraints.
 Search for maximum constraints.
 Search for retry counts.
 Search for timeout values.
 Search for pagination limits.
 Search for date arithmetic.
 Search for duration calculations.
 Search for averages.
 Search for recommendation thresholds.
 Search for skill-gap thresholds.
 Search for completeness calculations.
 Search for analytics formulas.
 Compare backend values with frontend labels.
 Compare formulas with tests.
 Compare implementation with project documentation.
 Check for duplicate formulas in different services.
20. CareerOS Boundary Test Matrix

For every important CareerOS threshold:

Case	Test
Empty input	[ ]
Zero	[ ]
One item	[ ]
Normal value	[ ]
Just below threshold	[ ]
Exact threshold	[ ]
Just above threshold	[ ]
Maximum value	[ ]
Invalid value	[ ]
Duplicate value	[ ]
Missing value	[ ]
Very large value	[ ]
Current Job Recommendation Boundaries
39
40
41

69
70
71

84
85
86

100
Required-Skill Coverage
49%
50%
51%
21. CareerOS Final Mathematical Review

Before a CareerOS milestone is considered complete:

 Every formula is documented.
 Every threshold is documented.
 Every score range is documented.
 Every percentage has a defined denominator.
 Every date calculation has defined boundaries.
 Every rate has a defined time period.
 Every AI-generated quantitative value is validated.
 Every deterministic calculation has automated tests.
 Boundary cases are tested.
 Backend and frontend calculations agree.
 Database constraints agree with business rules.
 Documentation agrees with implementation.
 No duplicate calculation logic exists without a clear reason.
 No unexplained magic numbers remain.
 All important numerical behavior is covered by tests.
22. CareerOS Golden Rule

If CareerOS can calculate something exactly, CareerOS code should calculate it. If AI is used to interpret something, CareerOS must validate the result before treating it as truth.

Every important number in CareerOS should answer these five questions:

What does it mean?
Where did it come from?
How was it calculated?
What is its valid range?
What happens at its boundaries?

If these questions cannot be answered, the number is not ready to be trusted.


### So you need these two files

```text
docs/checklists/Mathematical_Detail_Checklist_Generic.md
docs/checklists/CareerOS_Mathematical_Detail_Checklist.md

The second one above now uses proper Markdown headings such as #, ##, and ###, so VS Code/GitHub will render the hierarchy correctly.