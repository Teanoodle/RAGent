"""Command-line interface for RAGent."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ragent.documents.errors import DocumentLoadError
from ragent.documents.loader import load_document
from ragent.documents.models import ContentBlock

READY_MESSAGE = "RAGent document ingestion is ready."


def _positive_integer(value: str) -> int:
    """Parse a command-line value that must be greater than zero."""
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed_value


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="ragent",
        description="Inspect and process technical documents with RAGent.",
    )
    subparsers = parser.add_subparsers(dest="command")

    for command, help_text in (
        ("inspect-document", "Extract and preview normalized document content."),
        ("inspect-pdf", "Preview a PDF using the document ingestion pipeline."),
    ):
        inspect_parser = subparsers.add_parser(command, help=help_text)
        inspect_parser.add_argument("path", type=Path, help="Path to the source file.")
        inspect_parser.add_argument(
            "--max-chars",
            type=_positive_integer,
            default=300,
            help="Maximum number of characters to preview per block (default: 300).",
        )
    return parser


def _format_block_location(block_number: int, block: ContentBlock) -> str:
    """Build a readable location label for a normalized content block."""
    location_parts = [f"Block {block_number}"]
    if block.page_number is not None:
        location_parts.append(f"Page {block.page_number}")
    if block.section:
        location_parts.append(f"Section: {block.section}")
    if block.line_start is not None:
        line_label = f"Lines {block.line_start}-{block.line_end or block.line_start}"
        location_parts.append(line_label)
    return " | ".join(location_parts)


def inspect_document(path: Path, max_chars: int) -> int:
    """Print a short block-by-block preview of a source document."""
    try:
        document = load_document(path)
    except DocumentLoadError as error:
        print(f"Error: {error}")
        return 1

    print(f"Document: {document.filename}")
    print(f"Type: {document.source_type}")
    print(f"Blocks: {len(document.blocks)}")
    if document.page_count:
        print(f"Pages: {document.page_count}")
    modality_names = ", ".join(modality.value for modality in document.modalities)
    print(f"Modalities: {modality_names or '[None]'}")

    for block_number, block in enumerate(document.blocks, start=1):
        preview = block.text[:max_chars] if block.has_text else "[No extractable text]"
        location = _format_block_location(block_number, block)
        print(f"\n--- {location} | {block.modality.value} ---")
        print(preview)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the RAGent command-line interface."""
    parser = build_parser()
    arguments = parser.parse_args(argv)

    if arguments.command in {"inspect-document", "inspect-pdf"}:
        return inspect_document(arguments.path, arguments.max_chars)

    print(READY_MESSAGE)
    return 0
