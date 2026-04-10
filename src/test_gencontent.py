import unittest

from gencontent import extract_title


class TestGeneratingContent(unittest.TestCase):
    def test_extract_title(self):
        md = "# This should work as a Title."
        self.assertEqual("This should work as a Title.", extract_title(md))

    def test_extract_title_no_title_case(self):
        md = "This should not work as a title"
        self.assertRaises(Exception, extract_title, md)

    def test_extract_title_not_first_line(self):
        md = """
This is an example with an intro line.

# This should work as a title.
"""
        self.assertEqual("This should work as a title.", extract_title(md))
