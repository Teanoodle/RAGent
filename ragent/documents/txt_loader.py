"""Line-aware plain-text document loading."""

from __future__ import annotations

from pathlib import Path

from ragent.documents.errors import DocumentLoadError
from ragent.documents.models import ContentBlock, Modality, SourceDocument


class TxtLoadError(DocumentLoadError):
    """Raised when a plain-text file cannot be validated or read."""


def _build_text_blocks(document_id: str, text: str) -> tuple[ContentBlock, ...]:
    """Split text at blank lines while preserving inclusive source line ranges."""
    lines = text.splitlines()
    blocks: list[ContentBlock] = []
    block_lines: list[str] = []
    block_start = 0

    def append_block(line_end: int) -> None:
        block_number = len(blocks) + 1
        blocks.append(
            ContentBlock(
                block_id=f"{document_id}:lines:{block_start}-{line_end}:text",
                document_id=document_id,
                modality=Modality.TEXT,
                text="\n".join(block_lines),
                line_start=block_start,
                line_end=line_end,
                metadata={"block_number": block_number},
            )
        )

    for line_number, line in enumerate(lines, start=1):
        if line.strip():
            if not block_lines:
                block_start = line_number
            block_lines.append(line)
        elif block_lines:
            append_block(line_number - 1)
            block_lines = []

    if block_lines:
        append_block(len(lines))

    return tuple(blocks)


def load_txt(path: str | Path) -> SourceDocument:
    """Normalize a UTF-8 plain-text file into line-aware text blocks."""
    txt_path = Path(path)
    if not txt_path.exists():
        raise TxtLoadError(f"Text file does not exist: {txt_path}")
    if not txt_path.is_file():
        raise TxtLoadError(f"Text path is not a file: {txt_path}")
    if txt_path.suffix.lower() != ".txt":
        raise TxtLoadError(f"Expected a .txt file: {txt_path}")

    try:
        text = txt_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise TxtLoadError(f"Text file is not valid UTF-8: {txt_path}") from error
    except OSError as error:
        raise TxtLoadError(f"Unable to read text file: {txt_path}") from error

    document_id = txt_path.stem
    return SourceDocument(
        document_id=document_id,
        filename=txt_path.name,
        source_type="text/plain",
        source_uri=str(txt_path.resolve()),
        blocks=_build_text_blocks(document_id, text),
        metadata={"format": "TXT", "encoding": "utf-8"},
    )
