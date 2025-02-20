import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        markdown = "This is a single block of text."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is a single block of text."])

    def test_multiple_blocks(self):
        markdown = "This is the first block.\n\nThis is the second block."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["This is the first block.", "This is the second block."])

    def test_blocks_with_extra_newlines(self):
        markdown = "First block.\n\n\n\nSecond block."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First block.", "Second block."])

    def test_blocks_with_leading_and_trailing_spaces(self):
        markdown = "  First block.  \n\n  Second block.  "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["First block.", "Second block."])

    def test_empty_string(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_only_newlines(self):
        markdown = "\n\n\n"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_mixed_content(self):
        markdown = "First block with **bold** text.\n\nSecond block with *italic* text.\n\nThird block with `code`."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [
            "First block with **bold** text.",
            "Second block with *italic* text.",
            "Third block with `code`."
        ])


if __name__ == '__main__':
    unittest.main()