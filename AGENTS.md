# CareerOS — Codex Agent Instructions

## 1. PROJECT IDENTITY

CareerOS is an AI-powered Career Operating System.

Its core purpose is to maintain a user's professional identity in a persistent Career Vault and use that information to provide career intelligence, opportunity discovery, resume intelligence, application assistance, interview preparation, networking assistance, and career analytics.

The complete product journey is:

User Account
→ Adaptive Onboarding
→ Career Vault
→ Career Intelligence
→ Opportunity Discovery
→ JD Intelligence
→ Resume Studio
→ Application Preparation
→ User Approval
→ Supported Application Automation
→ Application Tracking
→ Interview Intelligence
→ Career Analytics

---

# 2. REQUIRED DOCUMENTATION

Before implementing any major milestone, read:

1. `PRD.md`
2. `Architecture.md`
3. `Rules.md`
4. `Phases.md`
5. `Design.md`
6. `Memory.md`
7. `ENVIRONMENT.md`

These files are the project's source of truth for product requirements, architecture, rules, design, implementation phases, current state, and local environment.

Do not repeatedly ask the user to explain information already contained in these files.

---

# 3. CURRENT PROJECT STATE

CareerOS already contains a working AI Resume Intelligence service.

Milestone 1 is COMPLETE.

Current resume pipeline:

```text
Resume/File
    ↓
Document Detection
    ↓
Extraction / OCR
    ↓
Qwen3.5 9B via Ollama
    ↓
CareerProfile Validation
    ↓
FastAPI Response