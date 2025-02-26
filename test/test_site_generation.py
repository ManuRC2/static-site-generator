
import unittest

from site_generation import extract_title


class TestSiteGeneration(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# My Awesome Title")
        self.assertEqual(title, "My Awesome Title")
        
    def test_extract_title_2(self):
        title = extract_title("### My Very Awesome Title\n\nSome other text")
        self.assertEqual(title, "My Very Awesome Title")
        
if __name__ == "__main__":
    unittest.main()