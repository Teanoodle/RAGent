"""Format-neutral data models shared by document loaders."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Modality(str, Enum):
    """Content types that can be preserved during document ingestion."""

    TEXT = "text"
    TABLE = "table"
    IMAGE = "image"
    CHART = "chart"
    FORMULA = "formula"


@dataclass(frozen=True, slots=True)
class ContentBlock:
    """One traceable unit of text or multimodal document content."""

    block_id: str
    document_id: str
    modality: Modality
    text: str = ""
    page_number: int | None = None
    section: str | None = None
    paragraph_index: int | None = None
    line_start: int | None = None
    line_end: int | None = None
    bounding_box: tuple[float, float, float, float] | None = None
    asset_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_text(self) -> bool:
        """Return whether the block contains extractable text."""
        return bool(self.text.strip())


@dataclass(frozen=True, slots=True)
class SourceDocument:
    """A source file normalized into traceable content blocks."""

    document_id: str
    filename: str
    source_type: str
    blocks: tuple[ContentBlock, ...]
    source_uri: str | None = None
    title: str | None = None
    author: str | None = None
    published_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def page_count(self) -> int:
        """Return the number of distinct page locations in the document."""
        return len(
            {block.page_number for block in self.blocks if block.page_number is not None}
        )

    @property
    def modalities(self) -> tuple[Modality, ...]:
        """Return the distinct modalities in their first-seen order."""
        return tuple(dict.fromkeys(block.modality for block in self.blocks))
