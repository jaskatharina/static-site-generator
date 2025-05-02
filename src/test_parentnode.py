import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_two_children_one_grandchild(self):
        uncle = LeafNode("h1", "uncle")
        grandchild = LeafNode("i", "grandchild")
        mom = ParentNode("p", [grandchild])
        gramma = ParentNode("div", [uncle, mom])
        self.assertEqual(
            gramma.to_html(),
            "<div><h1>uncle</h1><p><i>grandchild</i></p></div>"
        )

if __name__ == "__main__":
    unittest.main()
