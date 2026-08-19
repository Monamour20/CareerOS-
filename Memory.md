# CareerOS — Project Memory

## Milestone 1
COMPLETE.

Verified:
- Universal document input
- PDF extraction
- DOC/DOCX extraction
- TXT
- Image input
- OCR
- Scanned PDF fallback
- Ollama
- Qwen3.5 9B
- CareerProfile validation
- FastAPI resume analysis
- Tests
- Ruff

## Milestone 2
COMPLETE.

Codex has created:
- Database configuration
- SQLAlchemy models
- Repository layer
- Alembic setup
- CareerProfile persistence service
- Career Vault routes
- Database integration tests

Final verified state as of 2026-08-14:
- PostgreSQL connection: verified against `careeros` as `careeros_user`
- Alembic migration: `20260810_0001` applied successfully
- Career Vault tables: verified present
- CareerProfile persistence and retrieval: verified
- Invalid LLM output non-persistence: verified
- Real resume workflow: RESUME_REVISED.pdf → extraction → Qwen3.5 9B → CareerProfile → PostgreSQL → retrieval verified
- Task 1 resume endpoint: verified with RESUME_REVISED.pdf
- pytest: 21 passed, 1 warning
- Ruff: all checks passed
- DATABASE_URL: configured through local `.env`; value must remain secret

## Immediate Next Action
Milestone 2 is frozen. Do not add new product features until Milestone 3 is explicitly requested.

## Environment
Windows, Python 3.13, Node 24, Git, PostgreSQL 17, Docker Desktop, Docker Compose, Ollama 0.32.6, Qwen3.5 9B, SQLAlchemy, Alembic, psycopg.

## Frozen Decisions
- PostgreSQL is primary database.
- Ollama + Qwen3.5 9B is current AI runtime.
- FastAPI is backend.
- Next.js is frontend.
- Career Vault is central persistent career memory.
- CareerProfile is not equivalent to a resume.
- Resume is optional.
- User approval is required before consequential external application actions.

## Milestone 3.1 — Authentication Verification

Status: COMPLETE

Verified manually through FastAPI Swagger:

- POST /api/v1/auth/signup — PASS
- PostgreSQL users persistence — PASS
- POST /api/v1/auth/login — PASS
- PostgreSQL auth_sessions persistence — PASS
- GET /api/v1/auth/me with Bearer session — PASS
- POST /api/v1/auth/logout — PASS
- GET /api/v1/auth/me after logout — 401 PASS

Test account:
- Email: careeros.auth.test@example.com
- User ID: 25
- Account type: standard

Security:
- No production credentials used.
- No destructive SQL commands used.
- Session tokens were not persisted in documentation.

## Milestone 3.2 — CareerOS Motion Foundation

Status: IN PROGRESS

### Completed
- Installed Motion for React.
- Created reusable GlassCard component.
- Created animated GlassGlow component.
- Created transparent crystal GlassToggle component.
- Added spring-based toggle movement.
- Added glass blur, reflections, rim highlights, shadows, and warm glow.

### Verification
Run from `C:\CareerOs\apps\web`:

```powershell
npm run typecheck
npm run test
npm run dev