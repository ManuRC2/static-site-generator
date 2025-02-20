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