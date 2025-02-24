import unittest
from markdown_to_html import text_to_children
from htmlnode import HTMLNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_text(self):
        markdown = "Hello, World!"
        result = text_to_children(markdown)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], HTMLNode)
        self.assertEqual(result[0].tag, 'p')
        self.assertEqual(result[0].value, 'Hello, World!')

    def test_bold(self):
        markdown = "Hello, **World**!"
        result = text_to_children(markdown)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], HTMLNode)
        self.assertEqual(result[0].tag, 'p')
        self.assertEqual(result[0].value, 'Hello, ')
        self.assertEqual(result[1].tag, 'b')
        self.assertEqual(result[1].value, 'World')
        self.assertEqual(result[2].tag, 'p')
        self.assertEqual(result[2].value, '!')
        
    def test_italic(self):
        text = "Hello, *World*!"
        result = text_to_children(text)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], HTMLNode)
        self.assertEqual(result[0].tag, 'p')
        self.assertEqual(result[0].value, 'Hello, ')
        self.assertEqual(result[1].tag, 'i')
        self.assertEqual(result[1].value, 'World')
        self.assertEqual(result[2].tag, 'p')
        self.assertEqual(result[2].value, '!')
    
    def test_code(self):
        text = "Hello, ```World```!"
        result = text_to_children(text)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], HTMLNode)
        self.assertEqual(result[0].tag, 'p')
        self.assertEqual(result[0].value, 'Hello, ')
        self.assertEqual(result[1].tag, 'pre')
        self.assertEqual(result[1].value, None)
        self.assertEqual(result[1].children[0].tag, 'code')
        self.assertEqual(result[1].children[0].value, 'World')
        self.assertEqual(result[2].tag, 'p')
        self.assertEqual(result[2].value, '!')
        

if __name__ == '__main__':
    unittest.main()