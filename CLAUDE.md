# CareerOS — Coding Agent Instructions

Read before implementing:
1. PRD.md
2. Architecture.md
3. Rules.md
4. Phases.md
5. Design.md
6. Memory.md
7. ENVIRONMENT.md

## Operating Mode
Inspect repository, dependencies, tests, and configuration before implementation. Reuse working code. State a concise plan, then implement only the requested milestone.

## Frozen Technology
Do not replace PostgreSQL, FastAPI, SQLAlchemy, Alembic, Ollama, Qwen3.5 9B, Next.js, React, or TypeScript.

## Task 1 Protection
The universal resume pipeline is frozen:
`Document → Extraction/OCR → Qwen3.5 9B → CareerProfile validation → API response`

Career Vault persistence must happen only after successful validation.

## Quality Loop
For each milestone:
`Inspect → Plan → Implement → Test → Repair → Integration Test → Final Report`

Repair ordinary lint/test issues within the same milestone rather than stopping at the first failure.

## Database Safety
Never guess credentials, expose credentials, or run destructive SQL against the existing database. Use Alembic.

## Final Report
Report files changed, architecture/database changes, tests, lint, integration verification, limitations, acceptance status, and the next milestone without implementing it.
