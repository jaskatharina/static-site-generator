import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        child = HTMLNode()
        node = HTMLNode(tag="p", value="smokin smokin swisher mane", children=child, props={"href": "https://www.google.com"})
        node2 = HTMLNode(tag="p", value="smokin smokin swisher mane", children=child, props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)
    def test_noteq(self):
        child = HTMLNode()
        node = HTMLNode("a", "smokin smokin swisher mane", child, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "smokin smokin swisher mane", child, {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)
    def test_propstohtml(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(" href=\"https://www.google.com\" target=\"_blank\"", node.props_to_html())

if __name__ == "__main__":
    unittest.main()
        
