import re

from htmlnode import LeafNode
from textnode import DELIMITERS, HTML_TAGS, TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag=HTML_TAGS[text_node.text_type], value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextType")


def split_nodes_delimiter(old_nodes: list[TextNode], text_type: TextType) -> list[LeafNode]:
    new_nodes = []
    for node in old_nodes:
        # TODO add support for nested nodes
        if node.text_type != TextType.NORMAL:
            new_nodes.append(text_node_to_html_node(node))
        else:
            len_start = len(DELIMITERS[text_type][0])
            len_end = len(DELIMITERS[text_type][1])
            start = node.text.find(DELIMITERS[text_type][0])
            end = node.text.rfind(DELIMITERS[text_type][1])
            if start == -1 or end == -1:
                raise ValueError(f"Invalid markdown syntax for {text_type.value}")
            else:
                new_nodes.extend([LeafNode(tag=HTML_TAGS[node.text_type], value=node.text[:start]),
                                  LeafNode(tag=HTML_TAGS[text_type], value=node.text[(start + len_start):end]),
                                  LeafNode(tag=HTML_TAGS[node.text_type], value=node.text[(end + len_end):]),
                                  ])
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall('\!\[(.*?)\]\((.*?)\)', text)
    
    
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall('\[(.*?)\]\((.*?)\)', text)


def split_nodes_complex(old_nodes: list[TextNode], text_type: TextType) -> list[LeafNode]:
    if text_type in [TextType.IMAGE, TextType.LINK]:
        delimiter_start = DELIMITERS[text_type][0]
        new_nodes = []
        for node in old_nodes:
            if text_type == TextType.LINK:
                values = extract_markdown_links(node.text)
            if text_type == TextType.IMAGE:
                values = extract_markdown_images(node.text)
            if values:
                val_start = 0
                val_end = 0
                
                for value in values:
                    prev_end = val_end
                    val_start = node.text.find(f"{delimiter_start}{value[0]}]({value[1]})")
                    val_end = val_start + len(f"{delimiter_start}{value[0]}]({value[1]})")
                    if prev_end < len(node.text):
                        new_nodes.append(LeafNode(tag=HTML_TAGS[node.text_type], value=node.text[prev_end:val_start]))
                        
                    if text_type == TextType.LINK:
                        new_nodes.append(LeafNode(tag=HTML_TAGS[text_type], value=value[0], props={"href": value[1]}))
                    if text_type == TextType.IMAGE:
                        new_nodes.append(LeafNode(tag=HTML_TAGS[text_type], value="", props={"src": value[1], "alt": value[0]}))
                    
                if val_end < len(node.text):
                    new_nodes.append(LeafNode(tag=HTML_TAGS[node.text_type], value=node.text[val_end:]))
            else:
                new_nodes.append(text_node_to_html_node(node))
        return new_nodes

def split_nodes_images(old_nodes: list[TextNode]) -> list[LeafNode]:
    return split_nodes_complex(old_nodes, TextType.IMAGE)

def split_nodes_links(old_nodes: list[TextNode]) -> list[LeafNode]:
    return split_nodes_complex(old_nodes, TextType.LINK)