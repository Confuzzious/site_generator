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
                raise Exception(f"Invalid Markdown Syntax: {old_node.text}")

            for i, part in enumerate(parts):
                if part == "":
                    continue

                if i % 2 == 0:
                    converted_nodes.append(TextNode(part, TextType.TEXT))

                if i % 2 != 0:
                    converted_nodes.append(TextNode(part, text_type))

    return converted_nodes
