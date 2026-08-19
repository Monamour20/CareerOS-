# CareerOS — Engineering Rules

## Frozen Technologies
Do not replace PostgreSQL, FastAPI, SQLAlchemy, Alembic, Ollama, Qwen3.5 9B, Next.js, React, or TypeScript without explicit approval.

Do not introduce MongoDB, MySQL, SQLite, or another LLM as a substitute.

## Preserve Working Code
Inspect before changing. Reuse existing code. Make the smallest safe change. Task 1 resume intelligence is frozen unless an integration defect requires a minimal change.

## Layering
`Route → Application Service → Domain → Repository/Infrastructure`

Routes must remain thin. Do not place SQLAlchemy orchestration inside routes.

## AI Safety
Never invent employers, titles, dates, skills, technologies, metrics, certifications, projects, achievements, or experience.

## Validation
`LLM → Parser → Pydantic → Business Validation → Persistence`

Never persist raw LLM output.

## Secrets
Never hardcode, commit, print, or expose passwords. Use environment variables. `.env.example` contains placeholders only.

## Database
PostgreSQL is the system of record. Schema changes go through Alembic. Do not auto-create tables at application startup. Never run destructive SQL against the user's development database during tests.

## Testing
Every milestone must preserve existing tests, add tests for new behavior, run pytest, run Ruff, and verify important integration flows.

## External Automation
Never bypass CAPTCHA, MFA, security controls, authorization, or consent. Never claim an application was submitted without external confirmation.

## Dependencies
Before adding a dependency, check whether it is already installed and whether an existing dependency solves the problem. Do not globally install unnecessary packages.

## Coding-Agent Workflow
Before implementation inspect repository structure, dependencies, tests, and configuration. Do not assume the repository is empty.

## Scope
Complete one milestone at a time. Do not silently start the next milestone.

## Final Report
Report changed files, architecture/database changes, tests, lint, integration verification, limitations, acceptance status, and the next milestone without implementing it.
