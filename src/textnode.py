from enum import Enum
from leafnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALICS = "italics"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, rhs):
        return self.text == rhs.text and self.text_type == rhs.text_type and self.url == rhs.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALICS:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        #only split text nodes
        if(node.text_type == TextType.TEXT):
            split_text = node.text.split(delimiter)
            #if string split by two matching delimiters, should have len of 3
            if(len(split_text) != 3):
                raise Exception("Matching delimiters not found")
            new_nodes.append(TextNode(split_text[0], node.text_type))
            new_nodes.append(TextNode(split_text[1], text_type))
            new_nodes.append(TextNode(split_text[2], node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
