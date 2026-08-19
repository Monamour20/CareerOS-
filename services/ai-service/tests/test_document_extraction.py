from io import BytesIO

import fitz
import pytest
from docx import Document
from PIL import Image

from app.core.errors import EmptyExtractedTextError, UnsupportedFileError
from app.infrastructure.document.extractors import ImageOCRExtractor
from app.infrastructure.document.service import DocumentExtractionService


def make_pdf(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def make_docx(text: str) -> bytes:
    document = Document()
    document.add_paragraph(text)
    stream = BytesIO()
    document.save(stream)
    return stream.getvalue()


def make_png() -> bytes:
    image = Image.new("RGB", (320, 120), color="white")
    stream = BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def test_pdf_extraction():
    service = DocumentExtractionService()
    result = service.extract("resume.pdf", make_pdf("Ada Lovelace resume " * 10))

    assert result.document_type == "pdf"
    assert "Ada Lovelace" in result.text


def test_docx_extraction():
    service = DocumentExtractionService()
    result = service.extract("resume.docx", make_docx("Grace Hopper resume"))

    assert result.document_type == "docx"
    assert "Grace Hopper" in result.text


def test_txt_extraction():
    service = DocumentExtractionService()
    result = service.extract("resume.txt", b"Margaret Hamilton\nSoftware Engineer")

    assert result.document_type == "txt"
    assert "Software Engineer" in result.text


def test_image_ocr_extraction(monkeypatch):
    monkeypatch.setattr("pytesseract.image_to_string", lambda image: "Katherine Johnson resume")
    extractor = ImageOCRExtractor()

    assert extractor.extract(make_png()) == "Katherine Johnson resume"


def test_scanned_pdf_falls_back_to_ocr(monkeypatch):
    monkeypatch.setattr("pytesseract.image_to_string", lambda image: "Scanned resume text")
    service = DocumentExtractionService()
    document = fitz.open()
    document.new_page()
    content = document.tobytes()
    document.close()

    result = service.extract("resume.pdf", content)

    assert result.text == "Scanned resume text"


def test_unsupported_file_type():
    service = DocumentExtractionService()

    with pytest.raises(UnsupportedFileError):
        service.extract("resume.bin", bytes.fromhex("000102030405"))


def test_empty_document():
    service = DocumentExtractionService()

    with pytest.raises(EmptyExtractedTextError):
        service.extract("resume.txt", b"   \n\t")
