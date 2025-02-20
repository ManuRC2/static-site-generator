import unittest
from utils import extract_markdown_images, extract_markdown_links, split_nodes_complex, text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType, DELIMITERS
from htmlnode import LeafNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text(self):
        text_node = TextNode(text="Hello", text_type=TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, None)

    def test_bold_text(self):
        text_node = TextNode(text="Hello", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, None)

    def test_italic_text(self):
        text_node = TextNode(text="Hello", text_type=TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, None)

    def test_code_text(self):
        text_node = TextNode(text="print('Hello')", text_type=TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")
        self.assertEqual(html_node.props, None)

    def test_link_text(self):
        text_node = TextNode(text="GitHub", text_type=TextType.LINK, url="https://github.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "GitHub")
        self.assertEqual(html_node.props, {"href": "https://github.com"})

    def test_image_text(self):
        text_node = TextNode(text="Image", text_type=TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Image"})

    def test_invalid_text_type(self):
        text_node = TextNode(text="Invalid", text_type="INVALID")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is an image ![alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.png")])

    def test_multiple_images(self):
        text = "Here is an image ![image1](https://example.com/image1.png) and another ![image2](https://example.com/image2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image1", "https://example.com/image1.png"), ("image2", "https://example.com/image2.png")])

    def test_no_images(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_image_with_special_characters(self):
        text = "Image with special characters ![alt text](https://example.com/image-1_2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image-1_2.png")])

    def test_image_with_spaces(self):
        text = "Image with spaces ![alt text](https://example.com/image%20with%20spaces.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image%20with%20spaces.png")])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This is a link [GitHub](https://github.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("GitHub", "https://github.com")])

    def test_multiple_links(self):
        text = "Here is a link [GitHub](https://github.com) and another [Google](https://google.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("GitHub", "https://github.com"), ("Google", "https://google.com")])

    def test_no_links(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_link_with_special_characters(self):
        text = "Link with special characters [GitHub](https://github.com/special-characters_1-2)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("GitHub", "https://github.com/special-characters_1-2")])

    def test_link_with_spaces(self):
        text = "Link with spaces [GitHub](https://github.com/with%20spaces)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("GitHub", "https://github.com/with%20spaces")])


if __name__ == '__main__':
    unittest.main()
