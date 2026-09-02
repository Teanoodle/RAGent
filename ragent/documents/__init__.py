"""Format-neutral document ingestion utilities for RAGent."""

from ragent.documents.errors import DocumentLoadError
from ragent.documents.loader import UnsupportedDocumentTypeError, load_document
from ragent.documents.models import ContentBlock, Modality, SourceDocument
from ragent.documents.pdf_loader import PdfLoadError, load_pdf
from ragent.documents.txt_loader import TxtLoadError, load_txt

__all__ = [
    "ContentBlock",
    "DocumentLoadError",
    "Modality",
    "PdfLoadError",
    "SourceDocument",
    "TxtLoadError",
    "UnsupportedDocumentTypeError",
    "load_document",
    "load_pdf",
    "load_txt",
]
