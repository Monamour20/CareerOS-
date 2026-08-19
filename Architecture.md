# CareerOS — System Architecture

## Frozen Stack

### Frontend
Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Framer Motion, Lucide.

### Backend
Python 3.13, FastAPI, Pydantic, SQLAlchemy 2.x, Alembic, psycopg.

### Database
PostgreSQL 17.

### AI
Ollama + Qwen3.5 9B. Do not switch without explicit approval.

### Documents
PyMuPDF, python-docx, Pillow, pytesseract/Tesseract, LibreOffice for legacy DOC.

### Browser
Playwright + Chromium.

### Infrastructure
Docker + Docker Compose.

## High-Level Architecture

```text
Browser
  ↓
Next.js / React
  ↓
FastAPI
  ↓
Application Services
  ├── Career Vault
  ├── Opportunity Intelligence
  ├── Resume Intelligence
  ├── Application Intelligence
  └── Analytics
  ↓
Infrastructure
  ├── PostgreSQL
  ├── Object/File Storage
  ├── Ollama
  ├── Document Extractors
  └── Playwright
```

## AI Boundary

`API → Application Service → AI Workflow → LLM Interface → Ollama → Qwen3.5 9B`

The LLM has no direct database access.

## Resume Pipeline

`Upload → Validation → Signature Detection → Extraction/OCR → Normalization → Qwen3.5 9B → Pydantic Validation → Business Validation → CareerProfile → Persistence`

Supported current formats: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG, WEBP.

## Career Vault

PostgreSQL is the system of record. Core entities include User, UserProfile, CareerProfile, Education, Experience, Skill, Project, Certification, Achievement, CareerGoal, CareerPreference, Resume, ResumeVersion, Opportunity, Application, Interview, and CareerMetric.

Use normalized relational tables. Do not make the entire career profile one JSON column.

## Persistence Boundary

Never use `LLM → Database`.

Use:
`LLM → Validated Domain Object → Application Service → Repository → SQLAlchemy → PostgreSQL`

## Data Flow

### Onboarding
`User → Signup → Adaptive Questions → Career Profile Data → Career Vault`

### Resume onboarding
`Resume → Document Intelligence → Validated CareerProfile → Merge with onboarding data → Career Vault`

### Opportunity
`External Source → Normalize → Deduplicate → Job Profile → Matching → Ranking → User`

### Application
`Job → JD Analysis → Resume Tailoring → Cover Letter → Answers → Validation → User Approval → Supported Automation → Tracking`

## Storage
PostgreSQL stores structured data and document metadata. Large documents should eventually use object storage.

## Browser Automation
Use adapters:
`Application → Automation Router → ATS/Website Adapter → Playwright → Browser`

Do not assume every site is automatable. Stop for CAPTCHA/MFA/security controls.

## Production Direction
Future architecture may use frontend hosting, API hosting, managed PostgreSQL, object storage, background workers, and GPU AI infrastructure. Redis is not mandatory until background jobs justify it.
