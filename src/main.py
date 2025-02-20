from pprint import pprint
from utils import text_to_text_nodes


nodes = text_to_text_nodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
pprint(nodes)