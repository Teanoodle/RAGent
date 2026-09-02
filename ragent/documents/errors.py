"""Shared errors for document ingestion."""


class DocumentLoadError(ValueError):
    """Base error raised when a document cannot be selected, validated, or read."""
