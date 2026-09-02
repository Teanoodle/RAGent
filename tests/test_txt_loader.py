"""Tests for line-aware plain-text loading."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ragent.documents.models import Modality
from ragent.documents.txt_loader import TxtLoadError, load_txt


class TxtLoaderTests(unittest.TestCase):
    """Verify plain-text validation, content, and line metadata."""

    def test_load_txt_splits_paragraphs_and_preserves_line_ranges(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "notes.txt"
            txt_path.write_text(
                "First line\nSecond line\n\nThird line\n",
                encoding="utf-8",
            )

            loaded_document = load_txt(txt_path)

        self.assertEqual(loaded_document.document_id, "notes")
        self.assertEqual(loaded_document.filename, "notes.txt")
        self.assertEqual(loaded_document.source_type, "text/plain")
        self.assertEqual(loaded_document.modalities, (Modality.TEXT,))
        self.assertEqual(len(loaded_document.blocks), 2)
        self.assertEqual(loaded_document.blocks[0].text, "First line\nSecond line")
        self.assertEqual(loaded_document.blocks[0].line_start, 1)
        self.assertEqual(loaded_document.blocks[0].line_end, 2)
        self.assertEqual(loaded_document.blocks[1].text, "Third line")
        self.assertEqual(loaded_document.blocks[1].line_start, 4)
        self.assertEqual(loaded_document.blocks[1].line_end, 4)

    def test_load_txt_accepts_utf8_bom(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "bom.txt"
            txt_path.write_text("Evidence", encoding="utf-8-sig")

            loaded_document = load_txt(txt_path)

        self.assertEqual(loaded_document.blocks[0].text, "Evidence")
        self.assertEqual(loaded_document.metadata["encoding"], "utf-8")

    def test_load_txt_returns_no_blocks_for_blank_file(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "blank.txt"
            txt_path.write_text("\n  \n", encoding="utf-8")

            loaded_document = load_txt(txt_path)

        self.assertEqual(loaded_document.blocks, ())
        self.assertEqual(loaded_document.modalities, ())

    def test_load_txt_rejects_missing_file(self) -> None:
        with self.assertRaisesRegex(TxtLoadError, "does not exist"):
            load_txt("missing.txt")

    def test_load_txt_rejects_directory(self) -> None:
        with TemporaryDirectory(suffix=".txt") as temporary_directory:
            with self.assertRaisesRegex(TxtLoadError, "is not a file"):
                load_txt(temporary_directory)

    def test_load_txt_rejects_non_txt_extension(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            markdown_path = Path(temporary_directory) / "notes.md"
            markdown_path.touch()

            with self.assertRaisesRegex(TxtLoadError, "Expected a .txt file"):
                load_txt(markdown_path)

    def test_load_txt_rejects_invalid_utf8(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "invalid.txt"
            txt_path.write_bytes(b"\xff\xfe")

            with self.assertRaisesRegex(TxtLoadError, "not valid UTF-8"):
                load_txt(txt_path)


if __name__ == "__main__":
    unittest.main()
