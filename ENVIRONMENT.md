# CareerOS — Local Environment

## Verified
- Python 3.13
- Node.js 24
- Git
- PostgreSQL 17
- Docker 28.5.1
- Docker Compose 2.40.2
- Ollama 0.32.6
- Qwen3.5 9B
- SQLAlchemy
- Alembic
- psycopg

## PostgreSQL
Database: `careeros`
User: `careeros_user`

Connection has previously been manually verified.

Never store the real password here.

Use `DATABASE_URL` through environment configuration.

## AI
Runtime: Ollama
Model: `qwen3.5:9b`

## Additional Local Requirements
Required before document/automation milestones:
- Tesseract OCR
- LibreOffice
- Playwright Chromium

Check actual installation before using them.

## Future, Not Immediate
- Redis
- Cloud object storage
- Managed PostgreSQL
- CI/CD services
- Production GPU infrastructure

Do not install future dependencies merely for speculation.
