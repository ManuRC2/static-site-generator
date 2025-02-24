from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Converts a markdown string into a list of text blocks.

    Args:
        markdown (str): The input markdown string to be converted.

    Returns:
        list[str]: A list of text blocks.
    """
    blocks = [x.strip().strip('\n') for x in markdown.split('\n\n') if x.strip().strip('\n')]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    """
    Converts a block of text into a BlockType.

    Args:
        block (str): The block of text to be converted.

    Returns:
        BlockType: The type of block.
    """
    if block.startswith('#'):
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    elif block.startswith('>'):
        return BlockType.QUOTE
    elif False not in [x.startswith('* ') for x in block.split('\n')]:
        return BlockType.UNORDERED_LIST
    elif False not in [x[0].isdigit() and x[1] == '.' for x in block.split('\n')]:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    