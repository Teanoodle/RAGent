"""Format-based document loader dispatch."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ragent.documents.errors import DocumentLoadError
from ragent.documents.models import SourceDocument
from ragent.documents.pdf_loader import load_pdf
from ragent.documents.txt_loader import load_txt

DocumentLoader = Callable[[str | Path], SourceDocument]

LOADERS: dict[str, DocumentLoader] = {
    ".pdf": load_pdf,
    ".txt": load_txt,
}


class UnsupportedDocumentTypeError(DocumentLoadError):
    """Raised when no loader is registered for a file extension."""


def load_document(path: str | Path) -> SourceDocument:
    """Load a document with the loader registered for its extension."""
    document_path = Path(path)
    extension = document_path.suffix.lower()
    loader = LOADERS.get(extension)
    if loader is None:
        supported_extensions = ", ".join(sorted(LOADERS))
        raise UnsupportedDocumentTypeError(
            f"Unsupported document type '{extension or '[no extension]'}'. "
            f"Currently supported: {supported_extensions}"
        )
    return loader(document_path)
