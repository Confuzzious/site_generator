import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com) and another [link](https://www.example.org)"
        )
        self.assertListEqual(
            [("link", "https://www.example.com"), ("link", "https://www.example.org")],
            matches,
        )

    def test_extract_markdown_images_with_exclude(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://imgur.com/zjjcJKZ.png) and another ![image](https://imgur.com/)"
        )
        self.assertListEqual(
            [
                ("image", "https://imgur.com/zjjcJKZ.png"),
                ("image", "https://imgur.com/"),
            ],
            matches,
        )

    def test_split_images(self):
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

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_invalid(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **unclosed bold")

    def test_text_to_textnodes_bold_only(self):
        node = "This is a **bold** only string"

        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" only string", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        self.assertListEqual([], text_to_textnodes(""))

    def test_text_to_textnodes_adjacent_formats(self):
        node = "This is testing **adjacent**_formats_"

        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is testing ", TextType.TEXT),
                TextNode("adjacent", TextType.BOLD),
                TextNode("formats", TextType.ITALIC),
            ],
            new_nodes,
        )
