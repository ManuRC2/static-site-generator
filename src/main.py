from markdown_to_html import markdown_to_html_node

html = markdown_to_html_node("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item""")
print(html)