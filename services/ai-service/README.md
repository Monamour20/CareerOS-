# CareerOS AI Service

FastAPI service for converting resume files into a normalized `CareerProfile`.

## Supported Formats

- PDF
- DOC
- DOCX
- TXT
- PNG
- JPG / JPEG
- WEBP

The service detects file type from file content instead of trusting the filename alone.

## OCR Technology

OCR uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) through `pytesseract`.

Scanned PDFs are handled by rendering pages with PyMuPDF, then passing page images to Tesseract.

## Windows System Dependencies

Install Tesseract OCR:

1. Download the Windows installer from the UB Mannheim builds: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it, commonly to `C:\Program Files\Tesseract-OCR`.
3. Add that folder to your `PATH`.
4. Verify:

```powershell
tesseract --version
```

Legacy `.doc` extraction requires LibreOffice because `.doc` is a binary Microsoft Word format:

1. Install LibreOffice for Windows: https://www.libreoffice.org/download/download-libreoffice/
2. Ensure `soffice.exe` is available on `PATH`, or set `LIBREOFFICE_PATH` to the full executable path.
3. Verify:

```powershell
soffice --version
```

DOCX does not require LibreOffice.

## Ollama Configuration

Start Ollama and pull a model:

```powershell
ollama serve
ollama pull qwen3.5:9b
```

Configure the service with environment variables:

```powershell
$env:LLM_PROVIDER = "ollama"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "qwen3.5:9b"
$env:OLLAMA_TIMEOUT_SECONDS = "180"
```

The model name is never hardcoded.

## Start the Service

```powershell
cd services/ai-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## API

Health:

```http
GET /health
```

Analyze resume:

```http
POST /api/v1/resume/analyze
Content-Type: multipart/form-data
```

Form field:

```text
file
```

## Test Each File Type

Use `/docs`, or use PowerShell:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/resume/analyze" -F "file=@C:\path\resume.pdf"
curl.exe -X POST "http://127.0.0.1:8000/api/v1/resume/analyze" -F "file=@C:\path\resume.docx"
curl.exe -X POST "http://127.0.0.1:8000/api/v1/resume/analyze" -F "file=@C:\path\resume.txt"
curl.exe -X POST "http://127.0.0.1:8000/api/v1/resume/analyze" -F "file=@C:\path\resume.png"
curl.exe -X POST "http://127.0.0.1:8000/api/v1/resume/analyze" -F "file=@C:\path\resume.jpg"
```

## Run Tests

```powershell
cd services/ai-service
pytest
```

The OCR unit test mocks the OCR engine so the test suite does not require Tesseract to be installed. Real OCR usage does require Tesseract.

## Known Limitations

- Legacy `.doc` extraction depends on LibreOffice.
- OCR quality depends on image quality and Tesseract language data.
- The service does not store uploaded resumes or generated profiles.
- The service does not include authentication yet.
