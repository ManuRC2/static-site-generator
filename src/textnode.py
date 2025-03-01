from enum import Enum

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

HTML_TAGS = {
    TextType.TEXT: "p",
    TextType.BOLD: "b",
    TextType.ITALIC: "i",
    TextType.CODE: "code",
    TextType.LINK: "a",
    TextType.IMAGE: "img",
}

DELIMITERS = {
    TextType.TEXT: ("", ""),
    TextType.BOLD: ("**", "**"),
    TextType.ITALIC: ("_", "_"),
    TextType.CODE: ("`", "`"),
    TextType.LINK: ("[", "]"),
    TextType.IMAGE: ("![", "]"),
}

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return value.text == self.text \
            and value.text_type == self.text_type \
            and value.url == self.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def is_splittable(self):
        for text_type in TextType.__members__.values():
            if self.text.count(DELIMITERS[text_type][0]) > 1 and self.text.count(DELIMITERS[text_type][1]) > 1:
                return True
        return False