"""Smoke tests for the RAGent package."""

import unittest

from ragent import __version__
from ragent.cli import READY_MESSAGE


class ProjectSmokeTest(unittest.TestCase):
    """Verify that the package and default command remain available."""

    def test_package_has_a_version(self) -> None:
        self.assertEqual(__version__, "0.1.0")

    def test_ready_message_describes_document_ingestion(self) -> None:
        self.assertIn("document ingestion", READY_MESSAGE)


if __name__ == "__main__":
    unittest.main()
