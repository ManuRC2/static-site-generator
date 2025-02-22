from src.htmlnode import HTMLNode
from src.markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


def markdown_block_to_html_node(markdown_node: str) -> HTMLNode:
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
            return HTMLNode('p', markdown_node)
        # TODO: Implement the rest of the block types
    


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a markdown string into a list of HTML nodes.

    Args:
        markdown (str): The input markdown string to be converted.

    Returns:
        HTMLNode: The root node of the HTML tree.
    """
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        markdown_block_to_html_node(block)
    