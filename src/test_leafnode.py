import unittest

from leafnode import LeafNode

class LeafNodeTest(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click to win a free iPhone!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click to win a free iPhone!</a>")
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "totalshreddage.jpg", "alt": "Nice flip brah"})
        self.assertEqual(node.to_html(), "<img src=\"totalshreddage.jpg\" alt=\"Nice flip brah\" />")

if __name__ == "__main__":
    unittest.main()
    
