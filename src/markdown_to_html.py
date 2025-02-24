from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_node_to_html_node, text_to_text_nodes
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Converts a text block into a list of HTML nodes.

    Args:
        text (str): The input text block to be converted.

    Returns:
        list[HTMLNode]: A list of HTML nodes.
    """
    text_nodes = text_to_text_nodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
        


def markdown_block_to_html_node(markdown_node: str) -> ParentNode:
    """
    Converts a markdown block into an HTML node.

    Args:
        markdown_node (str): The input markdown block to be converted.
        
    Returns:
        HTMLNode: The HTML node representing the markdown block.
    """
    block_type = block_to_block_type(markdown_node)
    match block_type:
        case BlockType.PARAGRAPH:
            node = ParentNode('p', markdown_node)
            node.children = text_to_children(markdown_node)
        case BlockType.HEADING:
            x = len(markdown_node.split()[0])
            node = ParentNode(f'h{x}', children=[])
            text = markdown_node[x:].strip()
            node.children = text_to_children(text)
        case BlockType.CODE:
            node = ParentNode('code')
            text = markdown_node[3:-3].strip()
            node.children = text_to_children(text)
        case BlockType.QUOTE:
            node = ParentNode('blockquote')
            text = markdown_node[1:].strip()
            node.children = text_to_children(text)
        case BlockType.UNORDERED_LIST:
            node = ParentNode('ul')
            for line in markdown_node.split('\n'):
                li = ParentNode('li')
                li.children = text_to_children(line[1:])
                node.children.append(li)
        case BlockType.ORDERED_LIST:
            node = ParentNode('ol')
            for line in markdown_node.split('\n'):
                li = ParentNode('li')
                li.children = text_to_children(line[1:])
                node.children.append(li)
                
    return node
            
    

def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a markdown string into a list of HTML nodes.

    Args:
        markdown (str): The input markdown string to be converted.

    Returns:
        HTMLNode: The root node of the HTML tree.
    """
    parent_node = ParentNode('div', children=[])
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        parent_node.children.append(markdown_block_to_html_node(block))
    return parent_node
    