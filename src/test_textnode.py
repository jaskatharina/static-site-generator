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
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
if __name__ == "__main__":
    unittest.main()
