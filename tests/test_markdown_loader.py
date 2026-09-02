"""Tests for structure-aware Markdown loading."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ragent.documents.markdown_loader import MarkdownLoadError, load_markdown
from ragent.documents.models import Modality


class MarkdownLoaderTests(unittest.TestCase):
    """Verify Markdown structure, source locations, and validation."""

    def test_load_markdown_preserves_structure_sections_and_line_ranges(self) -> None:
        markdown = """# Guide

Introductory paragraph.

## Install

- Create an environment
- Install the package

```python
print("ready")
```
"""
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "guide.md"
            markdown_path.write_text(markdown, encoding="utf-8")

            document = load_markdown(markdown_path)

        self.assertEqual(document.document_id, "guide")
        self.assertEqual(document.filename, "guide.md")
        self.assertEqual(document.source_type, "text/markdown")
        self.assertEqual(document.title, "Guide")
        self.assertEqual(document.modalities, (Modality.TEXT,))
        self.assertEqual(len(document.blocks), 5)

        title, paragraph, heading, item_list, code = document.blocks
        self.assertEqual(title.metadata["block_type"], "heading")
        self.assertEqual(title.metadata["heading_level"], 1)
        self.assertEqual(title.section, "Guide")
        self.assertEqual((title.line_start, title.line_end), (1, 1))

        self.assertEqual(paragraph.metadata["block_type"], "paragraph")
        self.assertEqual(paragraph.section, "Guide")
        self.assertEqual((paragraph.line_start, paragraph.line_end), (3, 3))

        self.assertEqual(heading.metadata["section_path"], ("Guide", "Install"))
        self.assertEqual(heading.section, "Guide > Install")
        self.assertEqual((heading.line_start, heading.line_end), (5, 5))

        self.assertEqual(item_list.metadata["block_type"], "list")
        self.assertEqual(item_list.text, "- Create an environment\n- Install the package")
        self.assertEqual((item_list.line_start, item_list.line_end), (7, 8))
        self.assertEqual(item_list.section, "Guide > Install")

        self.assertEqual(code.metadata["block_type"], "code")
        self.assertEqual(code.metadata["code_language"], "python")
        self.assertTrue(code.metadata["fence_closed"])
        self.assertEqual((code.line_start, code.line_end), (10, 12))
        self.assertIn('print("ready")', code.text)
        self.assertEqual(code.section, "Guide > Install")

    def test_load_markdown_supports_setext_headings(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "setext.markdown"
            markdown_path.write_text(
                "Document title\n==============\n\nSection\n-------\n",
                encoding="utf-8",
            )

            document = load_markdown(markdown_path)

        self.assertEqual(document.title, "Document title")
        self.assertEqual(len(document.blocks), 2)
        self.assertEqual(document.blocks[0].metadata["heading_level"], 1)
        self.assertEqual(document.blocks[1].metadata["heading_level"], 2)
        self.assertEqual(document.blocks[1].section, "Document title > Section")

    def test_load_markdown_preserves_hash_in_heading_text(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "language.md"
            markdown_path.write_text("# C#\n\n## Syntax ###", encoding="utf-8")

            document = load_markdown(markdown_path)

        self.assertEqual(document.title, "C#")
        self.assertEqual(document.blocks[0].metadata["heading_text"], "C#")
        self.assertEqual(document.blocks[1].metadata["heading_text"], "Syntax")
        self.assertEqual(document.blocks[1].section, "C# > Syntax")

    def test_load_markdown_preserves_unclosed_code_fence(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "code.md"
            markdown_path.write_text("```text\nunfinished", encoding="utf-8")

            document = load_markdown(markdown_path)

        self.assertEqual(len(document.blocks), 1)
        self.assertEqual(document.blocks[0].text, "```text\nunfinished")
        self.assertFalse(document.blocks[0].metadata["fence_closed"])
        self.assertEqual(
            (document.blocks[0].line_start, document.blocks[0].line_end), (1, 2)
        )

    def test_load_markdown_accepts_utf8_bom(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "bom.md"
            markdown_path.write_text("# Evidence", encoding="utf-8-sig")

            document = load_markdown(markdown_path)

        self.assertEqual(document.title, "Evidence")
        self.assertEqual(document.blocks[0].text, "# Evidence")

    def test_load_markdown_returns_no_blocks_for_blank_file(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "blank.md"
            markdown_path.write_text("\n  \n", encoding="utf-8")

            document = load_markdown(markdown_path)

        self.assertEqual(document.blocks, ())
        self.assertIsNone(document.title)

    def test_load_markdown_rejects_missing_file(self) -> None:
        with self.assertRaisesRegex(MarkdownLoadError, "does not exist"):
            load_markdown("missing.md")

    def test_load_markdown_rejects_directory(self) -> None:
        with TemporaryDirectory(suffix=".md") as temporary_directory:
            with self.assertRaisesRegex(MarkdownLoadError, "is not a file"):
                load_markdown(temporary_directory)

    def test_load_markdown_rejects_unsupported_extension(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            text_path = Path(temporary_directory) / "notes.txt"
            text_path.touch()

            with self.assertRaisesRegex(MarkdownLoadError, "Expected a .md"):
                load_markdown(text_path)

    def test_load_markdown_rejects_invalid_utf8(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "invalid.md"
            markdown_path.write_bytes(b"\xff\xfe")

            with self.assertRaisesRegex(MarkdownLoadError, "not valid UTF-8"):
                load_markdown(markdown_path)


if __name__ == "__main__":
    unittest.main()
