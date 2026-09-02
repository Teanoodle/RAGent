"""Structure-aware Markdown document loading."""

from __future__ import annotations

from pathlib import Path
import re

from ragent.documents.errors import DocumentLoadError
from ragent.documents.models import ContentBlock, Modality, SourceDocument

ATX_HEADING_PATTERN = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*)|[ \t]*)$")
SETEXT_UNDERLINE_PATTERN = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
LIST_ITEM_PATTERN = re.compile(r"^ {0,3}(?:[-+*]|\d+[.)])[ \t]+")
FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class MarkdownLoadError(DocumentLoadError):
    """Raised when a Markdown file cannot be validated or read."""


def _section_label(section_path: list[str]) -> str | None:
    """Return a readable label for the active Markdown heading path."""
    return " > ".join(section_path) or None


def _atx_heading_text(raw_text: str | None) -> str:
    """Normalize optional ATX closing markers without damaging text such as C#."""
    heading_text = (raw_text or "").strip()
    return re.sub(r"[ \t]+#+[ \t]*$", "", heading_text).strip()


def _build_markdown_blocks(
    document_id: str, text: str
) -> tuple[tuple[ContentBlock, ...], str | None]:
    """Parse Markdown into ordered, line-aware structural blocks."""
    lines = text.splitlines()
    blocks: list[ContentBlock] = []
    section_path: list[str] = []
    document_title: str | None = None
    line_index = 0

    def append_block(
        *,
        block_type: str,
        line_start: int,
        line_end: int,
        block_text: str,
        extra_metadata: dict[str, object] | None = None,
    ) -> None:
        block_number = len(blocks) + 1
        metadata: dict[str, object] = {
            "block_number": block_number,
            "block_type": block_type,
            "section_path": tuple(section_path),
        }
        if extra_metadata:
            metadata.update(extra_metadata)
        blocks.append(
            ContentBlock(
                block_id=(
                    f"{document_id}:block:{block_number}:"
                    f"lines:{line_start}-{line_end}:{block_type}"
                ),
                document_id=document_id,
                modality=Modality.TEXT,
                text=block_text,
                section=_section_label(section_path),
                line_start=line_start,
                line_end=line_end,
                metadata=metadata,
            )
        )

    def update_section(level: int, heading_text: str) -> None:
        nonlocal document_title, section_path
        section_path = section_path[: level - 1]
        section_path.append(heading_text)
        if level == 1 and document_title is None:
            document_title = heading_text

    while line_index < len(lines):
        line = lines[line_index]
        line_number = line_index + 1

        if not line.strip():
            line_index += 1
            continue

        fence_match = FENCE_PATTERN.match(line)
        if fence_match:
            fence = fence_match.group(1)
            fence_character = fence[0]
            code_language = fence_match.group(2).strip() or None
            block_lines = [line]
            line_index += 1
            closed = False
            closing_pattern = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}{{{len(fence)},}}[ \t]*$"
            )
            while line_index < len(lines):
                code_line = lines[line_index]
                block_lines.append(code_line)
                line_index += 1
                if closing_pattern.match(code_line):
                    closed = True
                    break
            append_block(
                block_type="code",
                line_start=line_number,
                line_end=line_index,
                block_text="\n".join(block_lines),
                extra_metadata={
                    "code_language": code_language,
                    "fence_character": fence_character,
                    "fence_closed": closed,
                },
            )
            continue

        heading_match = ATX_HEADING_PATTERN.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = _atx_heading_text(heading_match.group(2))
            update_section(level, heading_text)
            append_block(
                block_type="heading",
                line_start=line_number,
                line_end=line_number,
                block_text=line,
                extra_metadata={
                    "heading_level": level,
                    "heading_text": heading_text,
                },
            )
            line_index += 1
            continue

        if line_index + 1 < len(lines):
            setext_match = SETEXT_UNDERLINE_PATTERN.match(lines[line_index + 1])
            if setext_match:
                level = 1 if setext_match.group(1).startswith("=") else 2
                heading_text = line.strip()
                update_section(level, heading_text)
                append_block(
                    block_type="heading",
                    line_start=line_number,
                    line_end=line_number + 1,
                    block_text="\n".join(lines[line_index : line_index + 2]),
                    extra_metadata={
                        "heading_level": level,
                        "heading_text": heading_text,
                        "heading_style": "setext",
                    },
                )
                line_index += 2
                continue

        if LIST_ITEM_PATTERN.match(line):
            block_lines = [line]
            line_index += 1
            while line_index < len(lines):
                candidate = lines[line_index]
                if not candidate.strip():
                    break
                if ATX_HEADING_PATTERN.match(candidate) or FENCE_PATTERN.match(candidate):
                    break
                block_lines.append(candidate)
                line_index += 1
            append_block(
                block_type="list",
                line_start=line_number,
                line_end=line_number + len(block_lines) - 1,
                block_text="\n".join(block_lines),
            )
            continue

        block_lines = [line]
        line_index += 1
        while line_index < len(lines):
            candidate = lines[line_index]
            if not candidate.strip():
                break
            if (
                ATX_HEADING_PATTERN.match(candidate)
                or FENCE_PATTERN.match(candidate)
                or LIST_ITEM_PATTERN.match(candidate)
            ):
                break
            if (
                line_index + 1 < len(lines)
                and SETEXT_UNDERLINE_PATTERN.match(lines[line_index + 1])
            ):
                break
            block_lines.append(candidate)
            line_index += 1
        append_block(
            block_type="paragraph",
            line_start=line_number,
            line_end=line_number + len(block_lines) - 1,
            block_text="\n".join(block_lines),
        )

    return tuple(blocks), document_title


def load_markdown(path: str | Path) -> SourceDocument:
    """Normalize a UTF-8 Markdown file into structure-aware text blocks."""
    markdown_path = Path(path)
    if not markdown_path.exists():
        raise MarkdownLoadError(f"Markdown file does not exist: {markdown_path}")
    if not markdown_path.is_file():
        raise MarkdownLoadError(f"Markdown path is not a file: {markdown_path}")
    if markdown_path.suffix.lower() not in {".md", ".markdown"}:
        raise MarkdownLoadError(f"Expected a .md or .markdown file: {markdown_path}")

    try:
        text = markdown_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise MarkdownLoadError(
            f"Markdown file is not valid UTF-8: {markdown_path}"
        ) from error
    except OSError as error:
        raise MarkdownLoadError(f"Unable to read Markdown file: {markdown_path}") from error

    document_id = markdown_path.stem
    blocks, title = _build_markdown_blocks(document_id, text)
    return SourceDocument(
        document_id=document_id,
        filename=markdown_path.name,
        source_type="text/markdown",
        source_uri=str(markdown_path.resolve()),
        title=title,
        blocks=blocks,
        metadata={"format": "MARKDOWN", "encoding": "utf-8"},
    )
