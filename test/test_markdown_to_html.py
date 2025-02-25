import unittest
from src.markdown_to_html import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraph_conversion(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'p')
        self.assertEqual(html_node.children[0].children[0].value, "This is a paragraph.")

    def test_heading_conversion(self):
        markdown = "# Heading 1"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'h1')
        self.assertEqual(html_node.children[0].children[0].value, "Heading 1")

    def test_code_block_conversion(self):
        markdown = "```\ncode block\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'code')
        self.assertEqual(html_node.children[0].children[0].value, "code block")

    def test_quote_conversion(self):
        markdown = "> This is a quote."
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'blockquote')
        self.assertEqual(html_node.children[0].children[0].value, "This is a quote.")

    def test_unordered_list_conversion(self):
        markdown = "* Item 1\n* Item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'ul')
        self.assertEqual(len(html_node.children[0].children), 2)
        self.assertEqual(html_node.children[0].children[0].tag, 'li')
        self.assertEqual(html_node.children[0].children[0].children[0].value, "Item 1")
        self.assertEqual(html_node.children[0].children[1].tag, 'li')
        self.assertEqual(html_node.children[0].children[1].children[0].value, "Item 2")

    def test_ordered_list_conversion(self):
        markdown = "1. Item 1\n2. Item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'ol')
        self.assertEqual(len(html_node.children[0].children), 2)
        self.assertEqual(html_node.children[0].children[0].tag, 'li')
        self.assertEqual(html_node.children[0].children[0].children[0].value, "Item 1")
        self.assertEqual(html_node.children[0].children[1].tag, 'li')
        self.assertEqual(html_node.children[0].children[1].children[0].value, "Item 2")
        
    def test_image_conversion(self):
        markdown = "![alt text](https://example.com/image.jpg)"
        html_node = markdown_to_html_node(markdown)
        print(html_node.to_html())
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, 'img')
        self.assertEqual(html_node.children[0].props['src'], "https://example.com/image.jpg")
        self.assertEqual(html_node.children[0].props['alt'], "alt text")
        

if __name__ == '__main__':
    unittest.main()