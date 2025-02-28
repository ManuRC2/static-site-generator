import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes, text_node_to_html_node, text_to_text_nodes
from textnode import TextNode, TextType

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
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children[0].tag, "code")
        self.assertEqual(html_node.children[0].value, "print('Hello')")

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

class TestSplitNodes(unittest.TestCase):
    def test_split_bold_text(self):
        text_node = TextNode(text="This is **bold** text", text_type=TextType.TEXT)
        result = split_nodes([text_node], TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_italic_text(self):
        text_node = TextNode(text="This is *italic* text", text_type=TextType.TEXT)
        result = split_nodes([text_node], TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_code_text(self):
        text_node = TextNode(text="This is ```code``` text", text_type=TextType.TEXT)
        result = split_nodes([text_node], TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_image_text(self):
        text_node = TextNode(text="This is an image ![alt text](https://example.com/image.png)", text_type=TextType.TEXT)
        result = split_nodes([text_node], TextType.IMAGE)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is an image ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image.png")

    def test_split_link_text(self):
        text_node = TextNode(text="This is a link [GitHub](https://github.com)", text_type=TextType.TEXT)
        result = split_nodes([text_node], TextType.LINK)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is a link ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "GitHub")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://github.com")


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **bold** and *italic* text with ```code``` and an image ![alt text](https://example.com/image.png) and a link [GitHub](https://github.com)"
        result = text_to_text_nodes(text)
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "italic")
        self.assertEqual(result[3].text_type, TextType.ITALIC)
        self.assertEqual(result[4].text, " text with ")
        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[5].text, "code")
        self.assertEqual(result[5].text_type, TextType.CODE)
        self.assertEqual(result[6].text, " and an image ")
        self.assertEqual(result[6].text_type, TextType.TEXT)
        self.assertEqual(result[7].text, "alt text")
        self.assertEqual(result[7].text_type, TextType.IMAGE)
        self.assertEqual(result[7].url, "https://example.com/image.png")
        self.assertEqual(result[8].text, " and a link ")
        self.assertEqual(result[8].text_type, TextType.TEXT)
        self.assertEqual(result[9].text, "GitHub")
        self.assertEqual(result[9].text_type, TextType.LINK)
        self.assertEqual(result[9].url, "https://github.com")


if __name__ == '__main__':
    unittest.main()
