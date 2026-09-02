"""Smoke tests for the initial project scaffold."""

import unittest

from ragent import __version__
from ragent.cli import READY_MESSAGE


class ProjectSmokeTest(unittest.TestCase):
    """Verify that the package can be imported before feature work begins."""

    def test_package_has_a_version(self) -> None:
        self.assertEqual(__version__, "0.1.0")

    def test_ready_message_describes_the_next_milestone(self) -> None:
        self.assertIn("V0", READY_MESSAGE)


if __name__ == "__main__":
    unittest.main()

