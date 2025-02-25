from markdown_to_html import markdown_to_html_node


markdown = "![alt text](https://example.com/image.jpg)"
html_node = markdown_to_html_node(markdown)
print(html_node.to_html())