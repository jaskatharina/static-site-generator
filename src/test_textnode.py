import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is the first node", TextType.BOLD)
        node2 = TextNode("This is the second node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_partialeq(self):
        node = TextNode("This is the first node", TextType.BOLD)
        node2 = TextNode("This is the second node", TextType.BOLD)
        self.assertNotEqual(node.text, node2.text)
        self.assertEqual(node.text_type, node2.text_type)

    def test_noneurl(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_to_html(self):
        node = TextNode("Welcome to zombocom", TextType.LINK, "https://www.zombo.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Welcome to zombocom")
        self.assertEqual(html_node.props, {"href": "https://www.zombo.com"})

    def test_img_to_html(self):
        node = TextNode("The majestic feline", TextType.IMAGE, "https://www.catpix.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.catpix.com", "alt": "The majestic feline"})

    def test_split_bold(self):
        node = TextNode("I said shut the fuck **UP**!!!!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        correct_nodes = [
            TextNode("I said shut the fuck ", TextType.TEXT),
            TextNode("UP", TextType.BOLD),
            TextNode("!!!!", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_invalidtype(self):
        node = TextNode("stealing _all_ ur files...", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALICS)
        self.assertEqual([node], new_nodes)

    def test_split_delimiter_missing(self):
        node = TextNode("stealing _all  ur files...", TextType.TEXT)
        try:
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALICS)
        except Exception as e:
            self.assertEqual(f"{e}", "Matching delimiters not found")
            
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [internet](https://www.google.com)")
        self.assertListEqual([("internet", "https://www.google.com")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_text_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some more text", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_two_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links_text_end(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some more text", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALICS),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and a **bold ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)** and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALICS),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("bold ", TextType.BOLD),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )



    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_paragraph(self):
        paragraph = "This is a paragraph"
        self.assertEqual(
            block_to_block_type(paragraph),
            BlockType.PARAGRAPH
        )

    def test_blocktype_heading6(self):
        heading = "######This is a heading 6!!!"
        self.assertEqual(
            block_to_block_type(heading),
            BlockType.HEADING6
        )

    def test_blocktype_heading3(self):
            heading = "###This is a heading 3!!!"
            self.assertEqual(
                block_to_block_type(heading),
                BlockType.HEADING3
            )
            
    def test_blocktype_heading1(self):
            heading = "#This is a heading 1!!!"
            self.assertEqual(
                block_to_block_type(heading),
                BlockType.HEADING1
            )

    def test_blocktype_code(self):
        code = "```This is a code block :>```"
        self.assertEqual(
            block_to_block_type(code),
            BlockType.CODE
        )

    def test_blocktype_quote(self):
        quote = ">be me\n>have to take off the indent on my shitty quotes bc its markdown"
        self.assertEqual(
            block_to_block_type(quote),
            BlockType.QUOTE
        )

    def test_blocktype_unordered_list(self):
        ulist = "- list item 1\n- list item 2\n- list item 3"
        self.assertEqual(
            block_to_block_type(ulist),
            BlockType.UNORDERED_LIST
        )

    def test_blocktype_ordered_list(self):
        olist = "1. list item 1\n2. list item 2\n3. list item 3"
        self.assertEqual(
            block_to_block_type(olist),
            BlockType.ORDERED_LIST
        )
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p 
tag here 

This is another paragraph with _italic_ text and `code` here

"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_heading(self):
        md = """
### This is a heading
that contains some **bold text**
and _italics_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading that contains some <b>bold text</b> and <i>italics</i></h3></div>"
        )
        
    def test_quote(self):
        md = """
> This is a quote that contains some **bold text** and _italics_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that contains some <b>bold text</b> and <i>italics</i></blockquote></div>"
        )

    def test_unorderedlist(self):
        md = """
- This is an unordered list
- that contains some **bold text**
- and _italics_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>that contains some <b>bold text</b></li><li>and <i>italics</i></li></ul></div>"
        )

    def test_orderedlist(self):
        md = """
1. This is an ordered list
2. that contains some **bold text**
3. and _italics_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>that contains some <b>bold text</b></li><li>and <i>italics</i></li></ol></div>"
        )

        
if __name__ == "__main__":
    unittest.main()
