"""Tests for format-neutral document models."""

import unittest

from ragent.documents.models import ContentBlock, Modality, SourceDocument


class DocumentModelTests(unittest.TestCase):
    """Verify shared metadata and modality behavior."""

    def test_content_block_detects_text(self) -> None:
        text_block = ContentBlock(
            block_id="document:text:1",
            document_id="document",
            modality=Modality.TEXT,
            text="Useful evidence",
        )
        empty_image_block = ContentBlock(
            block_id="document:image:1",
            document_id="document",
            modality=Modality.IMAGE,
            text="   ",
            asset_path="assets/image-1.png",
        )

        self.assertTrue(text_block.has_text)
        self.assertFalse(empty_image_block.has_text)

    def test_source_document_summarizes_pages_and_modalities(self) -> None:
        blocks = (
            ContentBlock(
                block_id="document:page:1:text",
                document_id="document",
                modality=Modality.TEXT,
                text="Page one text",
                page_number=1,
            ),
            ContentBlock(
                block_id="document:page:1:image",
                document_id="document",
                modality=Modality.IMAGE,
                page_number=1,
                asset_path="assets/image-1.png",
            ),
            ContentBlock(
                block_id="document:page:2:text",
                document_id="document",
                modality=Modality.TEXT,
                text="Page two text",
                page_number=2,
            ),
        )
        document = SourceDocument(
            document_id="document",
            filename="document.pdf",
            source_type="application/pdf",
            blocks=blocks,
        )

        self.assertEqual(document.page_count, 2)
        self.assertEqual(document.modalities, (Modality.TEXT, Modality.IMAGE))


if __name__ == "__main__":
    unittest.main()
