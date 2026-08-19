from dataclasses import dataclass
from enum import StrEnum


class DocumentType(StrEnum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    TXT = "txt"
    PNG = "png"
    JPG = "jpg"
    WEBP = "webp"


@dataclass(frozen=True)
class DetectedFile:
    document_type: DocumentType
    extension: str
    mime_type: str


@dataclass(frozen=True)
class ExtractedDocument:
    text: str
    document_type: DocumentType
