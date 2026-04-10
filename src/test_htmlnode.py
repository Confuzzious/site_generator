import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_none(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
        )
        self.assertEqual(node.props_to_html(), "")

    def test__repr__(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(a, Click me!, None, {'href': 'https://www.google.com', 'target': '_blank'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_tag_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
        )

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

    def test_to_html_with_no_childrent(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("b", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("i", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child1</b><span>child2</span><i>child3</i></div>",
        )

    def test_to_html_mixed_deep(self):
        great_grandchild = LeafNode("i", "deep")
        grandchild = ParentNode("b", [great_grandchild])
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b><i>deep</i></b></span></div>",
        )

    def test_to_html_mixed_children(self):
        nested = ParentNode("b", [LeafNode(None, "bold")])
        parent = ParentNode(
            "p",
            [
                LeafNode(None, "before "),
                nested,
                LeafNode(None, " after"),
            ],
        )
        self.assertEqual(
            parent.to_html(),
            "<p>before <b>bold</b> after</p>",
        )
