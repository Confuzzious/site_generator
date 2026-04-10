from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.QUOTE:
        split = block.split("\n")
        new_lines = []
        for line in split:
            stripped = line[2:]
            new_lines.append(stripped)
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)

    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        li = []
        for line in lines:
            if line.startswith("-"):
                text = line[2:]
                children = text_to_children(text)
                line = ParentNode("li", children)
                li.append(line)
        return ParentNode("ul", li)

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        li = []
        count = 1
        for line in lines:
            if line.startswith(f"{count}."):
                text = line[3:]
                children = text_to_children(text)
                line = ParentNode("li", children)
                li.append(line)
                count += 1
        return ParentNode("ol", li)

    if block_type == BlockType.CODE:
        text = block[4:-3]
        typed = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(typed)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])

    if block_type == BlockType.HEADING:
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        lines = block[count + 1 :]
        children = text_to_children(lines)
        return ParentNode(f"h{count}", children)

    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        joined = " ".join(lines)
        children = text_to_children(joined)
        return ParentNode("p", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    stripped = []
    for word in split_markdown:
        stripped_word = word.strip()
        if stripped_word == "":
            continue

        stripped.append(stripped_word)
    return stripped


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    split_block = block.split("\n")
    if block.startswith(">"):
        for lines in split_block:
            if not lines.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for lines in split_block:
            if not lines.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    list_number = 1
    if block.startswith(f"{list_number}. "):
        for lines in split_block:
            if not lines.startswith(f"{list_number}. "):
                list_number += 1
                return BlockType.PARAGRAPH
            list_number += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
