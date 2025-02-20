import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, "Hello")
        node2 = TextNode("This is a text node", TextType.BOLD, "Hello")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "asd")
        node2 = TextNode("This is a different text node", TextType.BOLD, "asd")
        self.assertNotEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, "asd")
        node2 = TextNode("This is a text node", TextType.TEXT, "asd")
        self.assertNotEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, "asd")
        node2 = TextNode("This is a text node", TextType.BOLD, "asdasdasd")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, http://example.com)")

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_text_content(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text, "This is a text node")

    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        self.assertEqual(node.url, "http://example.com")

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()