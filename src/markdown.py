import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from markdownblock import BlockType, markdown_to_blocks, block_to_block_type


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Invalid Markdown: Not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        substrings = node.text.split(delimiter)
        if len(substrings) % 2 == 0:
            raise Exception("Invalid Markdown: Delimiter not in text")
        for index in range(0, len(substrings)):
            if substrings[index] == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(substrings[index], TextType.TEXT))
            else:
                new_nodes.append(TextNode(substrings[index], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]+)\]\(([^\(\)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[([^\[\]]+)\]\(([^\(\)]+)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Invalid Markdown: Not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        images = extract_markdown_images(node_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:
            substrings = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(substrings) != 2:
                raise ValueError("Invalid Markdown: Image syntax not closed")
            if substrings[0] != "":
                new_nodes.append(TextNode(substrings[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = substrings[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

        # substrings = node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
        # if substrings[0] != "":
        #     new_nodes.append(TextNode(substrings[0], TextType.TEXT))
        # new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
        # if substrings[1] != "":
        #     new_nodes.extend(split_nodes_image([TextNode(substrings[1], TextType.TEXT)]))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise Exception("Invalid Markdown: Not a TextNode")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        links = extract_markdown_links(node_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            substrings = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(substrings) != 2:
                raise ValueError("Invalid Markdown: Link syntax not closed")
            if substrings[0] != "":
                new_nodes.append(TextNode(substrings[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = substrings[1]
        if node_text != "":
            new_nodes.append([TextNode(node_text, TextType.TEXT)])
            
        # substrings = node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
        # if substrings[0] != "":
        #     new_nodes.append(TextNode(substrings[0], TextType.TEXT))
        # new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
        # if substrings[1] != "":
        #     new_nodes.extend(split_nodes_link([TextNode(substrings[1], TextType.TEXT)]))

    return new_nodes

def text_to_textnodes(text):
    return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case BlockType.PARAGRAPH:
                nodes.append()