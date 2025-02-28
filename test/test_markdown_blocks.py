import unittest
from markdown_blocks import markdown_to_blocks
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


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


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_code_block(self):
        block = "```\nThis is a code block\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a paragraph."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()