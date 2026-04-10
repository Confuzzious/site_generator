import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    converted_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            converted_nodes.append(old_node)
            continue

        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f"Invalid Markdown Syntax: {old_node.text}")

            for i, part in enumerate(parts):
                if part == "":
                    continue

                if i % 2 == 0:
                    converted_nodes.append(TextNode(part, TextType.TEXT))

                if i % 2 != 0:
                    converted_nodes.append(TextNode(part, text_type))

    return converted_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    converted_nodes = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if not images:
            converted_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for image in images:
            alt, url = image
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            converted_nodes.append(TextNode(sections[0], TextType.TEXT))
            converted_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]
        if remaining_text != "":
            converted_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return converted_nodes


def split_nodes_link(old_nodes):
    converted_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if not links:
            converted_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        for link in links:
            alt, link = link
            sections = remaining_text.split(f"[{alt}]({link})", 1)
            converted_nodes.append(TextNode(sections[0], TextType.TEXT))
            converted_nodes.append(TextNode(alt, TextType.LINK, link))
            remaining_text = sections[1]

        if remaining_text != "":
            converted_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return converted_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
