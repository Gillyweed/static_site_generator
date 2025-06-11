from textnode import TextType, TextNode
from htmlnode import LeafNode
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def block_to_block_type(md):
    #md is a single block of markdown text
    # it is assumed to have no leading/trailing whitespace
    lines = md.split('\n')

    # Code block: starts and ends with ```
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Heading block: single line, starts with 1-6 # followed by a space
    if len(lines) == 1 and lines[0].startswith("#"):
        if 1 <= len(lines[0].split(" ")[0]) <=6 and lines[0].split(" ")[0].count("#") == len(lines[0].split(" ")[0]):
            return BlockType.HEADING

    # Quote block: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every linke starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines start with 1. 2. 3. etc.
    if all(line.split(". ", 1)[0].isdigit() and line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text) 
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextType not recognized")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) < 2:
                new_nodes.append(node)
                continue

            is_delimited = False

            for part in parts:
                if is_delimited:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                is_delimited = not is_delimited
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        text = node.text
        matches = extract_markdown_images(text)

        current_index = 0
        if not matches:
            new_nodes.append(node)
            continue

        for alt, url in matches:
            image_pos = text.find(f"![{alt}]({url})", current_index)

            if image_pos > current_index:
                before_text = text[current_index:image_pos]
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_index = image_pos + len(f"![{alt}]({url})")

        if current_index < len(text):
            remaining_text = text[current_index:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)

        current_index = 0
        if not matches:
            new_nodes.append(node)
            continue

        for alt, url in matches:
            image_pos = text.find(f"[{alt}]({url})", current_index)

            if image_pos > current_index:
                before_text = text[current_index:image_pos]
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            current_index = image_pos + len(f"[{alt}]({url})")

        if current_index < len(text):
            remaining_text = text[current_index:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    return new_nodes

def markdown_to_blocks(markdown):
    # split the markdown by line
    blocks = markdown.split('\n\n')
    # strip off any whitespace
    blocks = [block.strip() for block in blocks]
    # remove any blocks that are empty
    blocks = list(filter(lambda block: block != '', blocks))
    return blocks
