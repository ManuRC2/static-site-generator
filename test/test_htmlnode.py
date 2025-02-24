import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag='div', value='Hello', children=[], props={'class': 'container'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'container'})

    def test_props_to_html(self):
        node = HTMLNode(props={'class': 'container', 'id': 'main'})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

        node_no_props = HTMLNode()
        self.assertEqual(node_no_props.props_to_html(), '')

    def test_repr(self):
        node = HTMLNode(tag='p', value='Hello', children=None, props={'style': 'color:red;'})
        self.assertEqual(repr(node), "HTMLNode(p, Hello, None, {'style': 'color:red;'})")

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode(tag='img', value="Hello", props={'src': 'image.png', 'alt': 'An image'})
        self.assertEqual(node.tag, 'img')
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'src': 'image.png', 'alt': 'An image'})

    def test_props_to_html(self):
        node = LeafNode(tag="", value="", props={'src': 'image.png', 'alt': 'An image'})
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="An image"')

        node_no_props = LeafNode(tag="", value="")
        self.assertEqual(node_no_props.props_to_html(), '')

    def test_repr(self):
        node = LeafNode(tag='img', value=None, props={'src': 'image.png', 'alt': 'An image'})
        self.assertEqual(repr(node), "HTMLNode(img, None, None, {'src': 'image.png', 'alt': 'An image'})")

    def test_to_html(self):
        node = LeafNode(tag='img', value="hello", props={'src': 'image.png', 'alt': 'An image'})
        self.assertEqual(node.to_html().replace('\n', ''), '<img src="image.png" alt="An image">hello</img>')

        node_different = LeafNode(tag='input', value="text", props={'type': 'text'})
        self.assertEqual(node_different.to_html().replace('\n', ''), '<input type="text">text</input>')


class TestParentNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode(tag='div', children=[], props={'class': 'container'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {'class': 'container'})

    def test_props_to_html(self):
        node = ParentNode(tag="", children="", props={'class': 'container', 'id': 'main'})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

        node_no_props = ParentNode(tag="", children="")
        self.assertEqual(node_no_props.props_to_html(), '')

    def test_repr(self):
        node = ParentNode(tag='div', children=[], props={'style': 'color:red;'})
        self.assertEqual(repr(node), "HTMLNode(div, None, [], {'style': 'color:red;'})")

    def test_to_html(self):
        # Test when no children
        node_no_children = ParentNode(tag='div', children=[], props={'class': 'container'})
        with self.assertRaises(ValueError):
            node_no_children.to_html()

        # Test when no tag
        node_no_tag = ParentNode(tag=None, children=[LeafNode(tag='p', value='Hello')], props={'class': 'container'})
        with self.assertRaises(ValueError):
            node_no_tag.to_html()
        
        # Test when one children
        node = ParentNode(tag='div', children=[LeafNode(tag='p', value='Hello')], props={'class': 'container'})
        self.assertEqual(node.to_html().replace('\n', ''), '<div class="container"><p>Hello</p></div>')
        
        # Test when multiple children
        node = ParentNode(tag='div', children=[LeafNode(tag='p', value='Hello'), LeafNode(tag='p', value='World')], props={'class': 'container'})
        self.assertEqual(node.to_html().replace('\n', ''), '<div class="container"><p>Hello</p><p>World</p></div>')


if __name__ == '__main__':
    unittest.main()