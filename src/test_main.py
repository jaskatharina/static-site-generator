import unittest
from main import *

class TestMain(unittest.TestCase):
    def test_extract_title_proper_header(self):
        md = """
# This is a basic markdown header

There's also a few more lines


some of which are blank
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is a basic markdown header"
        )

    def test_extract_title_no_header(self):
        exception_found = False
        md = """
There is no header

There's also a few more lines


some of which are blank
"""
        try:
            extract_title(md)
        except Exception:
            exception_found = True

        self.assertEqual(
            exception_found, True
        )
        
if __name__ == "__main__":
    unittest.main()
