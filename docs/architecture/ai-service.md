# AI Service Architecture

The AI Service is a FastAPI service with thin HTTP routes and an application workflow in `application/analyze_resume.py`.

Main boundaries:

- `api/`: HTTP route definitions and dependency wiring.
- `application/`: orchestration of document extraction, LLM analysis, and validation.
- `domain/`: strict career profile models and validation helpers.
- `infrastructure/document/`: file type detection, extraction, OCR, and text normalization.
- `infrastructure/llm/`: LLM interface and provider-specific clients.

Adding a new document format should require a new extractor implementation, not a rewrite of the resume analysis workflow.
