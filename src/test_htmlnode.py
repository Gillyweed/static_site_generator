import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Text inside paragraph", children=None, props={"href": "www.google.com"})
        node2 = HTMLNode("p", "Text inside paragraph", children=None, props={"href": "www.google.com"})
        self.assertEqual(node, node2) 

    def test_props_to_html(self):
        node = HTMLNode("p", "Text inside paragraph", children=None, props={"href": "www.google.com"})
        res = node.props_to_html()
        self.assertEqual(res, ' href="www.google.com"')

    def test_not_eq(self):
        node = HTMLNode("p", "Text inside paragraph", children=None, props={"href": "www.google.com"})
        node2 = HTMLNode("p", "Different Text inside paragraph", children=None, props={"href": "www.google.com"})
        self.assertNotEqual(node, node2)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", props={"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<p href="www.google.com">Hello, world!</p>')

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
