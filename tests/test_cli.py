"""Tests for the RAGent command-line interface."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pymupdf

from ragent.cli import main


class CommandLineTests(unittest.TestCase):
    """Verify document previews and user-facing errors."""

    def test_inspect_document_prints_normalized_pdf_summary(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            pdf_path = Path(temporary_directory) / "sample.pdf"
            with pymupdf.open() as document:
                page = document.new_page()
                page.insert_text((72, 72), "Command line preview")
                document.save(pdf_path)

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    ["inspect-document", str(pdf_path), "--max-chars", "100"]
                )

        self.assertEqual(exit_code, 0)
        self.assertIn("Type: application/pdf", output.getvalue())
        self.assertIn("Pages: 1", output.getvalue())
        self.assertIn("Modalities: text", output.getvalue())
        self.assertIn("Command line preview", output.getvalue())

    def test_inspect_document_reports_unsupported_format(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(["inspect-document", "sample.docx"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Unsupported document type", output.getvalue())

    def test_inspect_document_prints_txt_line_ranges(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "notes.txt"
            txt_path.write_text("First paragraph\n\nSecond paragraph", encoding="utf-8")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["inspect-document", str(txt_path)])

        self.assertEqual(exit_code, 0)
        self.assertIn("Type: text/plain", output.getvalue())
        self.assertIn("Blocks: 2", output.getvalue())
        self.assertIn("Lines 1-1", output.getvalue())
        self.assertIn("Lines 3-3", output.getvalue())
        self.assertIn("Second paragraph", output.getvalue())

    def test_inspect_document_reports_invalid_txt_encoding(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            txt_path = Path(temporary_directory) / "invalid.txt"
            txt_path.write_bytes(b"\xff")

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["inspect-document", str(txt_path)])

        self.assertEqual(exit_code, 1)
        self.assertIn("not valid UTF-8", output.getvalue())

    def test_inspect_document_rejects_non_positive_preview_length(self) -> None:
        error_output = StringIO()
        with redirect_stderr(error_output):
            with self.assertRaises(SystemExit) as raised_error:
                main(["inspect-document", "sample.pdf", "--max-chars", "0"])

        self.assertEqual(raised_error.exception.code, 2)
        self.assertIn("value must be greater than zero", error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
