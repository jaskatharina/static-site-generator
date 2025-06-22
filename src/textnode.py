from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALICS = "italics"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    HEADING4 = "heading4"
    HEADING5 = "heading5"
    HEADING6 = "heading6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
            #special case to handle node that starts with delimited text
            if(len(split_text) % 2 == 0 and node.text.startswith(delimiter)):
                for i in range(len(split_text)):
                    #if even parity, use delimited text type
                    if(i % 2 == 0):
                        new_nodes.append(TextNode(split_text[i], node.text_type))
                    #if odd parity, use parent node's text type
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))
            #special case to handle node that ends with delimited text
            elif(len(split_text) % 2 == 0 and node.text.endswith(delimiter)):
                for i in range(len(split_text)):
                    #if even parity, use parent node's text type
                    if(i % 2 == 0):
                        new_nodes.append(TextNode(split_text[i], node.text_type))
                    #if odd parity, use delimited text type
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))
            #if length of split text is even, delimiters dont match
            elif(len(split_text) % 2 == 0):
                raise Exception("Matching delimiters not found")
            #if length is 1, append text without alterations
            elif(len(split_text) == 1):
                new_nodes.append(node)
            else:
                i = 0
                for i in range(len(split_text)):
                    #if even parity, use parent node's text type
                    if(i % 2 == 0):
                        new_nodes.append(TextNode(split_text[i], node.text_type))
                    #if odd parity, use delimited text type
                    else:
                         new_nodes.append(TextNode(split_text[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_nodes = []
        plaintext_nodes = []
        #extracts instances of image syntax
        images = extract_markdown_images(node.text)
        #if no images exist in text, append original node unchanged
        if(len(images) == 0):
            new_nodes.append(node)
        #if one or more images in text
        else: 
            #each image is a tuple of form ('text', 'url')
            for image in images:
                #replace image syntax with special delimiter
                node.text = node.text.replace(f"![{image[0]}]({image[1]})", "<<>>")
                #append image node to list
                image_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            #split up text using delimiter
            plaintext_strings = node.text.split("<<>>")
            #convert plaintext strings into textnodes
            for string in plaintext_strings:
                plaintext_nodes.append(TextNode(string, node.text_type))
            #alternate between appending plaintext and image nodes
            for i in range(len(plaintext_nodes)):
                #ignore any empty nodes
                if plaintext_nodes[i].text != "":
                    new_nodes.append(plaintext_nodes[i])
                #check if i is valid index for image_nodes
                if i < len(image_nodes):
                    new_nodes.append(image_nodes[i])
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_nodes = []
        plaintext_nodes = []
        #extracts instances of link syntax
        links = extract_markdown_links(node.text)
        #if no links exist in text, append original node unchanged
        if(len(links) == 0):
            new_nodes.append(node)
        #if one or more links in text
        else:
            #each link is a tuple of form ('text', 'url')
            for link in links:
                #replace link syntax in original line with special delimiter
                node.text = node.text.replace(f"[{link[0]}]({link[1]})", "<<>>")
                #append link node to list
                link_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            #split up text using delimiter
            plaintext_strings = node.text.split("<<>>")
            #convert plaintext strings into textnodes
            for string in plaintext_strings:
                plaintext_nodes.append(TextNode(string, node.text_type))
            #alternate between appending plaintext and link nodes
            for i in range(len(plaintext_nodes)):
                #ignore any empty nodes
                if plaintext_nodes[i].text != "":
                    new_nodes.append(plaintext_nodes[i])
                #check if i is valid index for link_nodes
                if i < len(link_nodes):
                    new_nodes.append(link_nodes[i])
    return new_nodes
        
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALICS)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return  new_nodes
            
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_blocks.append(block.strip())
    for block in stripped_blocks:
        if block == "":
            stripped_blocks.remove(block)
    return stripped_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    cnt = 0
    valid = False
    #number of hashtags corresponds to heading type
    if re.findall("^######", block) != []:
        return BlockType.HEADING6
    elif re.findall("^#####", block) != []:
        return BlockType.HEADING5
    elif re.findall("^####", block) != []:
        return BlockType.HEADING4
    elif re.findall("^###", block) != []:
        return BlockType.HEADING3
    elif re.findall("^##", block) != []:
        return BlockType.HEADING2
    elif re.findall("^#", block) != []:
        return BlockType.HEADING1
    elif block.startswith("```") and block.strip().endswith("```"):
        return BlockType.CODE
    #first checks if quote pattern appears at all
    elif re.search("^>", block) != None:
        valid = True
        #then checks for the pattern on each line, invalidating if not found
        for line in lines:
            if re.search("^>", line) == None:
                valid = False
        if valid == True:
            return BlockType.QUOTE
    #first checks if unordered list pattern appears at all
    elif re.search("^- ", block) != None:
        valid = True
        #then checks for the pattern on each line, invalidating if not found
        for line in lines:
            if re.search("^- ", line) == None:
                valid = False
        if valid == True:
            return BlockType.UNORDERED_LIST
    elif re.search("^1.", block) != None:
        valid = True
        for line in lines:
            cnt += 1
            #checks if the pattern is not found in the line
            if re.search(f"^{cnt}.", line) == None:
                valid = False
        if valid == True:
            return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
        
def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        parent_node = block_type_to_parent_node(block_type)

        child_nodes = []
        if((block_type == BlockType.UNORDERED_LIST) | (block_type == BlockType.ORDERED_LIST)):
            child_nodes = handle_list_items(block, block_type)
            
        elif(block_type != BlockType.CODE):
            child_nodes = text_to_children(block, block_type)
        #refrain from inline markdown parsing on code blocks
        else:
            parent_node.tag = "pre"
            #strip backticks and leading newlines
            child_nodes.append(text_node_to_html_node(TextNode(block.strip("`").lstrip("\n"), TextType.CODE)))
        
        parent_node.children = child_nodes
        block_nodes.append(parent_node)
    return ParentNode(tag="div", children=block_nodes)

def handle_list_items(block, block_type):
    list_item_nodes = []
    list_items = block.split("\n")
    for list_item in list_items:
        child_nodes = text_to_children(list_item, block_type)
        list_item_nodes.append(ParentNode(tag="li", children=child_nodes))
    return list_item_nodes

def block_type_to_parent_node(block_type):
    if block_type == BlockType.PARAGRAPH:
        return ParentNode(tag="p", children=None)
    elif block_type == BlockType.HEADING1:
        return ParentNode(tag="h1", children=None)
    elif block_type == BlockType.HEADING2:
        return ParentNode(tag="h2", children=None)
    elif block_type == BlockType.HEADING3:
        return ParentNode(tag="h3", children=None)
    elif block_type == BlockType.HEADING4:
        return ParentNode(tag="h4", children=None)
    elif block_type == BlockType.HEADING5:
        return ParentNode(tag="h5", children=None)
    elif block_type == BlockType.HEADING6:
        return ParentNode(tag="h6", children=None)
    elif block_type == BlockType.QUOTE:
        return ParentNode(tag="blockquote", children=None)
    elif block_type == BlockType.CODE:
        return ParentNode(tag="code", children=None)
    elif block_type == BlockType.UNORDERED_LIST:
        return ParentNode(tag="ul", children=None)
    elif block_type == BlockType.ORDERED_LIST:
        return ParentNode(tag="ol", children=None)

#strips markdown indicators from noncode blocks
def block_type_strip(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return block
        case BlockType.HEADING1 | BlockType.HEADING2 | BlockType.HEADING3 | BlockType.HEADING4 | BlockType.HEADING5 | BlockType.HEADING6:
            return block.lstrip(" #")
        case BlockType.QUOTE:
            return block.lstrip(" >")
        case BlockType.UNORDERED_LIST:
            return block.lstrip(" -")
        case BlockType.ORDERED_LIST:
            return block.lstrip("1234567890. ")

#converts raw text into partitioned html nodes    
def text_to_children(block, block_type):
    block = block_type_strip(block, block_type)
    text_nodes = text_to_textnodes(" ".join(block.split()))
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes
 
