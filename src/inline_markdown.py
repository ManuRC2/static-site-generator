import re

from htmlnode import LeafNode
from textnode import DELIMITERS, HTML_TAGS, TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag="", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextType")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall('\!\[(.*?)\]\((.*?)\)', text)
    
    
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall('\[(.*?)\]\((.*?)\)', text)


def split_nodes(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
    """
    Splits text nodes based on the specified text type.

    Args:
        old_nodes (list[TextNode]): The list of text nodes to be split.
        text_type (TextType): The type of text to split (e.g., BOLD, ITALIC, CODE, IMAGE, LINK).

    Returns:
        list[TextNode]: A new list of text nodes with the specified text type split.
    """
    # TODO add support for nested nodes
    new_nodes = []
    if text_type in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                len_start = len(DELIMITERS[text_type][0])
                len_end = len(DELIMITERS[text_type][1])
                del0 = node.text.count(DELIMITERS[text_type][0])
                del1 = node.text.count(DELIMITERS[text_type][1])
                ammount = min(del0, del1)
                if "Geographical" in node.text:
                    print(node.text)
                if ammount > 0:
                    for x in range(ammount):
                        start = node.text.find(DELIMITERS[text_type][0])
                        end = node.text[(start+len_start):].find(DELIMITERS[text_type][1]) + start + len_start
                        if start != -1 and end != -1:
                            new_nodes.extend([TextNode(text_type=node.text_type, text=node.text[:start]),
                                            TextNode(text_type=text_type, text=node.text[(start + len_start):end]),
                                            ])
                            node.text = node.text[end + len_end:]
                    if end != -1:
                        new_nodes.append(TextNode(text_type=node.text_type, text=node.text[end:]))
                    else:
                        new_nodes.append(node)
                else:
                    new_nodes.append(node)
            else:
                new_nodes.append(node)
    elif text_type in [TextType.IMAGE, TextType.LINK]:
        delimiter_start = DELIMITERS[text_type][0]
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                if text_type == TextType.LINK:
                    values = extract_markdown_links(node.text)
                elif text_type == TextType.IMAGE:
                    values = extract_markdown_images(node.text)
                if values:
                    val_start = 0
                    val_end = 0
                    
                    for value in values:
                        prev_end = val_end
                        val_string = f"{delimiter_start}{value[0]}]({value[1]})"
                        val_start = node.text.find(val_string)
                        val_end = val_start + len(val_string)
                        if prev_end < len(node.text) and prev_end != val_start:
                            new_nodes.append(TextNode(text=node.text[prev_end:val_start], text_type=node.text_type))
                        new_nodes.append(TextNode(text=value[0], text_type=text_type, url=value[1]))
                        
                    if val_end < len(node.text):
                        new_nodes.append(TextNode(text=node.text[val_end:], text_type=node.text_type))
                else:
                    new_nodes.append(node)
            else:
                new_nodes.append(node)
    return new_nodes


def text_to_text_nodes(text: str) -> list[TextNode]:
    """
    Converts a text string into a list of TextNode objects, splitting by various text types.

    Args:
        text (str): The input text string to be converted.

    Returns:
        list[TextNode]: A list of TextNode objects representing the parsed text.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes(nodes, TextType.BOLD)
    nodes = split_nodes(nodes, TextType.CODE)
    nodes = split_nodes(nodes, TextType.ITALIC)
    nodes = split_nodes(nodes, TextType.IMAGE)
    nodes = split_nodes(nodes, TextType.LINK)
    return nodes

