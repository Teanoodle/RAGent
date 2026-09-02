"""Tests for page-aware PDF loading."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pymupdf

from ragent.documents.models import Modality
from ragent.documents.pdf_loader import PdfLoadError, load_pdf


class PdfLoaderTests(unittest.TestCase):
    """Verify PDF validation and page metadata."""

    def test_load_pdf_preserves_filename_page_numbers_and_text(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            pdf_path = Path(temporary_directory) / "sample.pdf"
            with pymupdf.open() as document:
                first_page = document.new_page()
                first_page.insert_text((72, 72), "First page text")
                second_page = document.new_page()
                second_page.insert_text((72, 72), "Second page text")
                document.save(pdf_path)

            loaded_document = load_pdf(pdf_path)

        self.assertEqual(loaded_document.document_id, "sample")
        self.assertEqual(loaded_document.filename, "sample.pdf")
        self.assertEqual(loaded_document.source_type, "application/pdf")
        self.assertEqual(loaded_document.page_count, 2)
        self.assertEqual(len(loaded_document.blocks), 2)
        self.assertEqual(loaded_document.blocks[0].modality, Modality.TEXT)
        self.assertEqual(loaded_document.blocks[0].page_number, 1)
        self.assertIn("First page text", loaded_document.blocks[0].text)
        self.assertEqual(loaded_document.blocks[1].page_number, 2)
        self.assertIn("Second page text", loaded_document.blocks[1].text)

    def test_load_pdf_keeps_blank_pages(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            pdf_path = Path(temporary_directory) / "blank.pdf"
            with pymupdf.open() as document:
                document.new_page()
                document.save(pdf_path)

            loaded_document = load_pdf(pdf_path)

        self.assertEqual(loaded_document.page_count, 1)
        self.assertEqual(loaded_document.blocks[0].page_number, 1)
        self.assertFalse(loaded_document.blocks[0].has_text)

    def test_load_pdf_rejects_missing_file(self) -> None:
        with self.assertRaisesRegex(PdfLoadError, "does not exist"):
            load_pdf("missing.pdf")

    def test_load_pdf_rejects_non_pdf_extension(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            text_path = Path(temporary_directory) / "notes.txt"
            text_path.touch()

            with self.assertRaisesRegex(PdfLoadError, "Expected a .pdf file"):
                load_pdf(text_path)

    def test_load_pdf_rejects_invalid_pdf_content(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            pdf_path = Path(temporary_directory) / "invalid.pdf"
            pdf_path.touch()

            with self.assertRaisesRegex(PdfLoadError, "Unable to read PDF"):
                load_pdf(pdf_path)


if __name__ == "__main__":
    unittest.main()
