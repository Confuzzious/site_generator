import unittest

from inline_markdown import split_nodes_delimiter

from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_nonexistent_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode(
            "This is text with an unmatched _italic delimiter", TextType.TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_non_text_node_unchanged(self):
        node = TextNode("bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertEqual(result, expected)

    def test_multiple_bold_sections(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
