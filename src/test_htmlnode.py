import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("tag1", "Some value")
		node2 = HTMLNode("tag1", "Some value")
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = HTMLNode("tag1", "Some value")
		node2 = HTMLNode("tag1", "Diff value")
		self.assertNotEqual(node, node2)

	def test_props_to_html_eq(self):
		props = {}
		props["href"] = "https://wwww.google.com"
		props["target"] = "_blank"
		node = HTMLNode(props=props)

		str_to_compare = " ".join(f"\"{key}\"=\"{value}\"" for key, value in props.items())
		self.assertEqual(str_to_compare, node.props_to_html())

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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

if __name__ == "__main__":
	unittest.main()
