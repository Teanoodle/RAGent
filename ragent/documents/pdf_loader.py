"""Page-aware PDF text extraction."""

from __future__ import annotations

from pathlib import Path

import pymupdf

from ragent.documents.errors import DocumentLoadError
from ragent.documents.models import ContentBlock, Modality, SourceDocument


class PdfLoadError(DocumentLoadError):
    """Raised when a PDF cannot be validated or read."""


def load_pdf(path: str | Path) -> SourceDocument:
    """Normalize a PDF into page-aware text blocks."""
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise PdfLoadError(f"PDF file does not exist: {pdf_path}")
    if not pdf_path.is_file():
        raise PdfLoadError(f"PDF path is not a file: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise PdfLoadError(f"Expected a .pdf file: {pdf_path}")

    try:
        with pymupdf.open(pdf_path) as document:
            if not document.is_pdf:
                raise PdfLoadError(f"File is not a valid PDF: {pdf_path}")

            document_id = pdf_path.stem
            blocks = tuple(
                ContentBlock(
                    block_id=f"{document_id}:page:{page_index + 1}:text",
                    document_id=document_id,
                    modality=Modality.TEXT,
                    page_number=page_index + 1,
                    text=page.get_text("text", sort=True).strip(),
                )
                for page_index, page in enumerate(document)
            )
            pdf_metadata = dict(document.metadata or {})
            return SourceDocument(
                document_id=document_id,
                filename=pdf_path.name,
                source_type="application/pdf",
                source_uri=str(pdf_path.resolve()),
                title=pdf_metadata.get("title") or None,
                author=pdf_metadata.get("author") or None,
                blocks=blocks,
                metadata={"format": "PDF"},
            )
    except (pymupdf.EmptyFileError, pymupdf.FileDataError) as error:
        raise PdfLoadError(f"Unable to read PDF: {pdf_path}") from error
