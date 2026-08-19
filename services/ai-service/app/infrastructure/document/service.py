from app.core.errors import EmptyExtractedTextError
from app.infrastructure.document.detection import FileTypeDetector
from app.infrastructure.document.extractors import (
    DOCExtractor,
    DOCXExtractor,
    FileExtractor,
    ImageOCRExtractor,
    PDFExtractor,
    TextExtractor,
)
from app.infrastructure.document.models import DocumentType, ExtractedDocument
from app.infrastructure.document.normalization import normalize_text


class DocumentExtractionService:
    def __init__(
        self,
        detector: FileTypeDetector | None = None,
        extractors: dict[DocumentType, FileExtractor] | None = None,
        libreoffice_path: str | None = None,
    ):
        image_extractor = ImageOCRExtractor()
        self.detector = detector or FileTypeDetector()
        self.extractors = extractors or {
            DocumentType.PDF: PDFExtractor(ocr_extractor=image_extractor),
            DocumentType.DOCX: DOCXExtractor(),
            DocumentType.DOC: DOCExtractor(libreoffice_path=libreoffice_path),
            DocumentType.TXT: TextExtractor(),
            DocumentType.PNG: image_extractor,
            DocumentType.JPG: image_extractor,
            DocumentType.WEBP: image_extractor,
        }

    def extract(self, filename: str, content: bytes, content_type: str | None = None) -> ExtractedDocument:
        detected = self.detector.detect(filename=filename, content=content, content_type=content_type)
        text = normalize_text(self.extractors[detected.document_type].extract(content))
        if not text:
            raise EmptyExtractedTextError("No readable resume text could be extracted.")
        return ExtractedDocument(text=text, document_type=detected.document_type)
