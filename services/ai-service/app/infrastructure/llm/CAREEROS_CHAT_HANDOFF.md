CareerOS — Chat Handoff

Purpose: Permanent handoff document for continuing CareerOS in a new ChatGPT conversation.
The repository and its actual source code are the source of truth for implementation. This file preserves project history, decisions, current state, and working rules from the previous CareerOS conversation.

1. Project Identity

Project: CareerOS

Goal: Build a serious AI-powered career operating system that maintains a persistent CareerProfile/Career Vault and provides career intelligence, job matching, skill-gap analysis, interview preparation, and eventually controlled agentic workflows.

CareerOS is not merely a resume parser. The resume is an optional input; the CareerProfile/Career Vault is the persistent career memory.

2. Current Core Stack

Frontend: Next.js

Backend: FastAPI

Database: PostgreSQL

ORM: SQLAlchemy

Migrations: Alembic

AI runtime currently used locally: Ollama

Current local model: Qwen3.5 9B

Python: 3.13

Node.js: 24

PostgreSQL: 17

Docker Desktop

Ollama: 0.32.6

Frontend testing: Vitest

Backend testing: pytest

Python linting: Ruff

Frontend animation/UI: Motion for React

3. Repository Structure

Current repository root:

C:\CareerOs

Important directories/files:

apps\web — Next.js frontend

services\ai-service — FastAPI AI/backend service

docs


PRD.md

Architecture.md

Rules.md

Phases.md

Design.md

Memory.md

ENVIRONMENT.md

README.md

AGENTS.md

CLAUDE.md

Local UI backup directories exist from previous UI passes. They should NOT be committed to GitHub.

4. Frozen Architecture Decisions

These decisions should not be casually changed:

PostgreSQL is the primary database.

FastAPI is the backend.

Next.js is the frontend.

Career Vault is the central persistent career memory.

CareerProfile is not equivalent to a resume.

Resume is optional.

User approval is required before consequential external application actions.

LLM output must be validated before persistence.

Do not silently weaken validation to make bad LLM output pass.

Keep secrets out of Git.

Prefer reproducible development environments.

Expensive AI operations should eventually be asynchronous rather than blocking an HTTP request indefinitely.

5. Completed Milestones

Milestone 1 — Document/Resume Intelligence Foundation

COMPLETE.

Verified capabilities:

Universal document input

PDF extraction

DOC/DOCX extraction

TXT extraction

Image input

OCR

Scanned PDF fallback

Ollama integration

Qwen3.5 9B integration

CareerProfile validation

FastAPI resume analysis

Tests

Ruff

Milestone 2 — Persistence / Career Vault

COMPLETE.

Verified:

Database configuration

SQLAlchemy models

Repository layer

Alembic setup

CareerProfile persistence service

Career Vault routes

Database integration tests

PostgreSQL connection against CareerOS database

Alembic migration 20260810_0001

Career Vault tables

CareerProfile persistence/retrieval

Invalid LLM output does not persist

Real resume workflow:
RESUME_REVISED.pdf
→ extraction
→ Qwen3.5 9B
→ CareerProfile
→ PostgreSQL
→ retrieval

Resume analysis endpoint

pytest previously verified: 21 passed, 1 warning

Ruff passed

Milestone 3.1 — Authentication

COMPLETE.

Verified manually through FastAPI Swagger:

POST /api/v1/auth/signup — PASS

PostgreSQL users persistence — PASS

POST /api/v1/auth/login — PASS

PostgreSQL auth_sessions persistence — PASS

GET /api/v1/auth/me with Bearer session — PASS

POST /api/v1/auth/logout — PASS

GET /api/v1/auth/me after logout — 401 PASS

A test account was used during verification. Credentials/tokens must NOT be written into this document.

Milestone 3.2 — CareerOS Motion Foundation

IN PROGRESS / UI foundation completed.

Completed:

Motion for React installed

Reusable GlassCard

Animated GlassGlow

Transparent crystal GlassToggle

Spring-based toggle movement

Glass blur

Reflections

Rim highlights

Shadows

Warm glow

Multiple UI passes were applied and verified with:

npm run typecheck

npm run test

npm run build

Current UI direction is premium physical glass rather than generic flat glassmorphism.

6. Important UI Direction

The CareerOS UI should eventually have a cursor-reactive physical system across the website.

The Profile Completeness card is intended to be the first reference implementation for cursor-reactive 3D movement.

Desired future behavior:

Mouse movement
→ detect cursor position
→ glass surface reacts
→ subtle 3D tilt/depth shift
→ reflection/light follows cursor
→ smooth spring animation

This should eventually extend to:

Glass cards

Sidebar

Top navigation

Metric cards

Buttons

Toggles

Panels

Modals

Page transitions

Important: do NOT implement this just because this handoff mentions it. It is a future UI direction unless the user explicitly asks to implement it.

The effect should feel physical, premium, subtle, and responsive — not exaggerated spinning.

7. Current Major Problem — Resume Analysis

This is the most important unresolved issue.

Frontend login works.

Backend starts correctly.

Resume extraction works quickly.

The backend logs show:

resume_analysis_started
resume_extraction_completed
resume_llm_started
~180 seconds
504 Gateway Timeout

Example:

2026-08-17 20:11:32 resume_analysis_started
2026-08-17 20:11:32 resume_extraction_completed
2026-08-17 20:11:32 resume_llm_started
2026-08-17 20:14:34 request_failed
POST /api/v1/resume/analyze 504 Gateway Timeout

Therefore:

Upload is working.

PDF extraction is working.

FastAPI is working.

Authentication is working.

The failure is during LLM generation.

The httpx import itself is NOT considered the root cause.

8. Current LLM Configuration

Current config file:

services\ai-service\app\core\config.py

Important defaults:

LLM_PROVIDER = ollama

OLLAMA_BASE_URL = http://localhost:11434

OLLAMA_MODEL = qwen3.5:9b

OLLAMA_TIMEOUT_SECONDS = 180.0

DATABASE_URL comes from environment

Root .env exists locally and must remain secret. It is not supposed to be committed.

9. Current Ollama Provider

File:

services\ai-service\app\infrastructure\llm\ollama.py

The provider uses:

httpx.AsyncClient

POST /api/generate

stream=false

format=json

think=false

A compact configuration was proposed because a direct Ollama test previously completed in about 51 seconds using:

temperature = 0.1

top_k = 20

top_p = 0.9

num_ctx = 4096

num_predict = 1800

The larger 8192 context / 2500 output configuration was associated with the timeout problem and should not be assumed to be better.

10. Current Resume Prompt

File:

services\ai-service\app\infrastructure\llm\prompts\resume_analysis.md

The prompt requests exactly the CareerProfile shape:

personal_information
education
experience
skills
projects
certifications
achievements
career_interests

Rules include:

no markdown

no extra keys

null for unknown strings

[] for unknown lists

concise strings

maximum item counts

infer career interests only from resume evidence

A shorter prompt was proposed to reduce generation complexity, but it should be treated as a controlled experiment, not a reason to bypass validation.

11. Critical AI Lesson

Do NOT solve slow AI generation merely by increasing the HTTP timeout.

The better long-term architecture is:

POST /resume/analyze
→ create analysis job
→ status = processing
→ background AI processing
→ LLM
→ CareerProfile validation
→ PostgreSQL
→ status = completed
→ frontend polls/subscribes
→ display result

The UI should eventually support states such as:

queued

processing

completed

failed

This is especially important for local/cloud AI models where generation may take tens of seconds or minutes.

12. Possible AI Model Strategy

The project is NOT required to remain permanently on Qwen3.5 9B.

Potential modern models discussed for evaluation:

Gemma 3 12B

Qwen3 8B

Qwen3-VL 8B

Mistral Small 3.1 24B

GPT-OSS 20B

Selection should be based on actual CareerOS benchmarks:

generation speed

structured JSON reliability

resume extraction accuracy

context handling

resource requirements

ability to run locally or through cloud infrastructure

Do not blindly download or switch multiple models. Benchmark first.

Long-term direction may use different models for different jobs, e.g.:

Document/vision model
→ CareerProfile extraction

Reasoning model
→ career analysis / job matching / skill-gap reasoning

The LLM layer should remain abstract enough to allow model/provider replacement.

13. Local + Cloud Development Strategy

The project is now moving toward a hybrid development workflow.

Desired setup:

LOCAL WINDOWS MACHINE
→ frontend/UI development
→ Next.js
→ browser testing
→ Motion / physical glass UI
→ optional local Ollama

GITHUB CODESPACES
→ backend development
→ FastAPI
→ Python
→ tests
→ Docker/dev environment
→ reproducible development

GITHUB
→ source of truth
→ synchronization between local and cloud development

VERCEL
→ Next.js frontend deployment

CLOUD BACKEND
→ FastAPI production service

MANAGED POSTGRESQL
→ production database

CLOUD AI
→ heavy AI inference

The laptop should eventually not be responsible for production AI inference.

14. GitHub / Codespaces Migration — CURRENT POSITION

This is the immediate active task.

The latest complete project ZIP was inspected.

Current local repository:

C:\CareerOs

Git state at the start of migration:

branch: master

no commits yet

no GitHub remote configured

all project files currently untracked

The repository contains a .gitignore.

Important local UI backup directories exist:

careeros-ui-backup-20260817-135522

careeros-ui-backup-20260817-140015

careeros-ui-final-backup-20260817-151121

careeros-ui-last-pass-backup-20260817-152808

These should NOT be committed.

.env and secrets should NOT be committed.

15. Immediate Next Action — Git Safety

Before the chat ended, the user was instructed to:

Ensure .gitignore ignores:

.env

.env.*

node_modules/

.venv/

Python caches

Next.js build output

local UI backup directories

Verify:
git check-ignore -v .env
git check-ignore -v apps\web\node_modules
git check-ignore -v careeros-ui-backup-20260817-135522

Run:
git status --short

Then:
git add .

Then inspect:
git status

Do NOT commit or push until the staged file list has been inspected and verified safe.

16. Planned GitHub/Codespaces Migration

After the staged files are confirmed safe:

Create/connect GitHub repository.

Create first clean commit.

Push CareerOS to GitHub.

Verify repository.

Add .devcontainer/devcontainer.json.

Create a GitHub Codespace.

Verify frontend/backend development inside Codespaces.

Establish local ↔ GitHub ↔ Codespaces workflow.

Add environment-specific secrets safely.

Only then begin cloud database migration.

Then cloud backend.

Then cloud AI.

Then Vercel production deployment.

Do NOT move everything to AWS/Azure immediately.

17. Git Workflow Rule

GitHub is the synchronization point.

Preferred workflow:

Local:
git pull
→ work
→ git add
→ git commit
→ git push

Codespace:
git pull
→ work
→ git add
→ git commit
→ git push

Avoid simultaneously editing the same files on different branches/environments without pulling first.

Feature branches are preferred for larger changes, e.g.:

feature/resume-intelligence

feature/glass-ui

feature/career-vault

feature/job-matching

18. User's Terminal Preference

The user wants commands to ALWAYS start by locating the correct directory.

For example:

cd C:\CareerOs\apps\web

or:

cd C:\CareerOs\services\ai-service

Do not give commands assuming the user is already in the correct directory.

For PowerShell, provide commands that work on Windows.

19. User's Working Preference

The user is frustrated by repeated requests for information that already exists.

Working rules:

Inspect uploaded project files before asking the user to locate files.

Do not repeatedly ask which files exist when the complete project has been uploaded.

Give exact commands.

Solve the current issue directly.

Do not introduce unnecessary iterative UI passes when the user asks for the full implementation.

Preserve working functionality.

Do not create avoidable errors.

After changes, verify typecheck/test/build where relevant.

For backend changes, verify actual endpoint behavior.

Explain the reason for important architectural changes simply.

Professional English.

Simple enough to understand quickly.

User prefers direct, practical instructions.

20. Verification Commands

Frontend:

cd C:\CareerOs\apps\web
npm run typecheck
npm run test
npm run build
npm run dev

Backend:

cd C:\CareerOs\services\ai-service
python -m uvicorn app.main --reload --host 127.0.0.1 --port 8000

Backend tests:

cd C:\CareerOs\services\ai-service
python -m pytest -q

Ruff:

cd C:\CareerOs\services\ai-service
python -m ruff check .

Python syntax:

cd C:\CareerOs\services\ai-service
python -m compileall .\app

Ollama:

cd C:\CareerOs
ollama list
ollama ps
ollama stop qwen3.5:9b

21. Current Priority Order

Fix/architect Resume Intelligence reliably.

Establish GitHub repository safely.

Establish GitHub Codespaces.

Make local + cloud development reproducible.

Move production database to managed PostgreSQL.

Choose cloud AI strategy/model.

Deploy FastAPI backend.

Deploy Next.js to Vercel.

Continue CareerOS product features.

Expand physical glass/cursor-reactive UI system.

Do not let UI polish repeatedly block core product/backend progress.

22. Future UI Requirement

The user wants CareerOS to eventually feel like a physical, responsive glass interface.

Reference:

Profile Completeness card
→ cursor-reactive 3D movement

Future interaction system:

pointer-reactive lighting

subtle 3D tilt

depth

reflections

spring motion

physical hover/press behavior

smooth page transitions

responsive behavior

This is a future design system, not an immediate task unless explicitly requested.

23. New Chat Startup Instructions

When this document is uploaded into a new ChatGPT conversation, the assistant should:

Read this document.

Read the latest project ZIP.

Treat the actual codebase as implementation truth.

Treat this document and Memory.md as project history/context.

Do not restart completed milestones.

Do not ask the user to locate files that exist in the uploaded project.

Identify the exact current state.

State what is complete.

State what is broken/in progress.

State the single next action.

Give exact Windows PowerShell commands with directory changes included.

Verify changes before moving to the next stage.

The new conversation is a continuation of the CareerOS project, not a new project.

24. Current Exact Handoff Point

The immediate unfinished task is:

Git safety check before the first CareerOS commit.

The user had already run:

cd C:\CareerOs
git status
git branch
git remote -v

Result:

On branch master

No commits yet

No remote

Project files untracked

The next command sequence should begin with:

cd C:\CareerOs

Then inspect/fix .gitignore, verify secrets/backups are ignored, run git status --short, stage safely, and inspect the staged result.

Do not jump directly into Codespaces until the Git repository is clean and safely committed.

25. Golden Rule

CareerOS should become increasingly reproducible.

The long-term source of truth should be:

GitHub
+
project documentation
+
Memory.md
+
devcontainer configuration
+
environment/secrets configuration

The ChatGPT conversation is a working interface, not the permanent database of project knowledge.