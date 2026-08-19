from pathlib import Path
from zipfile import BadZipFile, ZipFile

from app.core.errors import InvalidFileError, UnsupportedFileError
from app.infrastructure.document.models import DetectedFile, DocumentType

OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")


class FileTypeDetector:
    def detect(self, filename: str, content: bytes, content_type: str | None = None) -> DetectedFile:
        if not content:
            raise InvalidFileError("Uploaded file is empty.")

        if content.startswith(b"%PDF"):
            return DetectedFile(DocumentType.PDF, "pdf", "application/pdf")

        if content.startswith(OLE_SIGNATURE):
            return DetectedFile(DocumentType.DOC, "doc", "application/msword")

        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return DetectedFile(DocumentType.PNG, "png", "image/png")

        if content.startswith(b"\xff\xd8\xff"):
            return DetectedFile(DocumentType.JPG, "jpg", "image/jpeg")

        if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
            return DetectedFile(DocumentType.WEBP, "webp", "image/webp")

        if self._is_docx(content):
            return DetectedFile(
                DocumentType.DOCX,
                "docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        if self._is_probably_text(content):
            return DetectedFile(DocumentType.TXT, "txt", "text/plain")

        suffix = Path(filename).suffix.lower().lstrip(".")
        suffix_hint = f" Extension hint was .{suffix}." if suffix else ""
        raise UnsupportedFileError(f"Unsupported or unrecognized resume file format.{suffix_hint}")

    def _is_docx(self, content: bytes) -> bool:
        if not content.startswith(b"PK"):
            return False
        try:
            from io import BytesIO

            with ZipFile(BytesIO(content)) as archive:
                names = set(archive.namelist())
                return "[Content_Types].xml" in names and "word/document.xml" in names
        except BadZipFile:
            return False

    def _is_probably_text(self, content: bytes) -> bool:
        sample = content[:4096]
        if b"\x00" in sample:
            return False

        for encoding in ("utf-8", "utf-16", "cp1252"):
            try:
                sample.decode(encoding)
                return True
            except UnicodeDecodeError:
                continue
        return False
