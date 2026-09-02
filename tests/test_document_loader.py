"""Tests for format-based document loader dispatch."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pymupdf

from ragent.documents.errors import DocumentLoadError
from ragent.documents.loader import UnsupportedDocumentTypeError, load_document
from ragent.documents.markdown_loader import MarkdownLoadError
from ragent.documents.pdf_loader import PdfLoadError
from ragent.documents.txt_loader import TxtLoadError


class DocumentLoaderTests(unittest.TestCase):
    """Verify extension-based dispatch and unsupported format errors."""

    def test_loader_errors_share_a_common_base_type(self) -> None:
        self.assertTrue(issubclass(PdfLoadError, DocumentLoadError))
        self.assertTrue(issubclass(MarkdownLoadError, DocumentLoadError))
        self.assertTrue(issubclass(TxtLoadError, DocumentLoadError))
        self.assertTrue(issubclass(UnsupportedDocumentTypeError, DocumentLoadError))

    def test_load_document_dispatches_pdf_case_insensitively(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            pdf_path = Path(temporary_directory) / "sample.PDF"
            with pymupdf.open() as document:
                page = document.new_page()
                page.insert_text((72, 72), "Dispatch test")
                document.save(pdf_path)

            loaded_document = load_document(pdf_path)

        self.assertEqual(loaded_document.filename, "sample.PDF")
        self.assertIn("Dispatch test", loaded_document.blocks[0].text)

    def test_load_document_dispatches_txt_case_insensitively(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "sample.TXT"
            txt_path.write_text("Dispatch test", encoding="utf-8")

            loaded_document = load_document(txt_path)

        self.assertEqual(loaded_document.filename, "sample.TXT")
        self.assertEqual(loaded_document.blocks[0].text, "Dispatch test")

    def test_load_document_dispatches_markdown_extensions_case_insensitively(
        self,
    ) -> None:
        with TemporaryDirectory() as temporary_directory:
            for filename in ("sample.MD", "sample.MARKDOWN"):
                with self.subTest(filename=filename):
                    markdown_path = Path(temporary_directory) / filename
                    markdown_path.write_text("# Dispatch test", encoding="utf-8")

                    loaded_document = load_document(markdown_path)

                    self.assertEqual(loaded_document.filename, filename)
                    self.assertEqual(loaded_document.title, "Dispatch test")

    def test_load_document_reports_unsupported_extension(self) -> None:
        with self.assertRaisesRegex(UnsupportedDocumentTypeError, "'.docx'"):
            load_document("sample.docx")

    def test_load_document_reports_missing_extension(self) -> None:
        with self.assertRaisesRegex(UnsupportedDocumentTypeError, "no extension"):
            load_document("README")


if __name__ == "__main__":
    unittest.main()
