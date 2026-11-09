from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		parts = node.text.split(delimiter)
		if len(parts) % 2 == 0:
			raise ValueError("invalid markdown syntax")

		split_nodes = []
		for i in range(len(parts)):
			if parts[i] == "":
				continue
			if i % 2 == 0:
				split_nodes.append(TextNode(parts[i], TextType.TEXT))
			else:
				split_nodes.append(TextNode(parts[i], text_type))

		new_nodes.extend(split_nodes)
	return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue

		original_text = node.text
		images = extract_markdown_images(original_text)
		if len(images) == 0:
			new_nodes.append(node)
			continue

		for image in images:
			parts = original_text.split(f"![{image[0]}]({image[1]})", 1)
			if len(parts) != 2:
				raise ValueError("invalid markdown, image section not closed")
			if parts[0] != "":
				new_nodes.append(TextNode(parts[0], TextType.TEXT))
			new_nodes.append(
				TextNode(
					image[0],
					TextType.IMAGE,
					image[1]
				)
			)
			original_text = parts[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, TextType.TEXT))
	return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		original_text = node.text
		links = extract_markdown_links(original_text)
		if len(links) == 0:
			new_nodes.append(node)
			continue
		for link in links:
			parts = original_text.split(f"[{link[0]}]({link[1]})", 1)
			if len(parts) != 2:
				raise ValueError("invalid markdown, link section not closed")
			if parts[0] != "":
				new_nodes.append(TextNode(parts[0], TextType.TEXT))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			original_text = parts[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, TextType.TEXT))
	return new_nodes

def extract_markdown_images(text) -> list[tuple[str, str]]:
	pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
	matches = re.findall(pattern, text)
	return matches

def extract_markdown_links(text) -> list[tuple[str, str]]:
	pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
	matches = re.findall(pattern, text)
	return matches

def text_to_textnodes(text) -> list[TextNode]:
	new_node = TextNode(text, TextType.TEXT)
	nodes = split_nodes_delimiter([new_node], "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	return nodes
