class HTMLNode():
	def __init__(
		self, tag: str | None = None, value: str | None = None,
		children: list[HTMLNode] | None = None, props: dict | None = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self) -> str:
		if self.props is None:
			return ""
		props_html = ""
		for prop in self.props:
			props_html += f' {prop}="{self.props[prop]}"'
		return props_html

	def __repr__(self):
			return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

	def __eq__(self, other) -> bool:
		if not isinstance(other,HTMLNode):
			return False
		return (
			self.tag == other.tag
	 		and self.value == other.value
			and self.children == other.children
			and self.props == other.props
		)

class LeafNode(HTMLNode):
	def __init__(self, tag: str | None, value: str, props: dict | None = None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			raise ValueError()
		if self.tag is None:
			return self.value

		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self, tag: str | None, children: list[HTMLNode] | None, props: dict | None = None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError()
		if self.children is None:
			raise ValueError()

		html_str = f"<{self.tag}>"
		for node in self.children:
			html_str += node.to_html()
		html_str += f"</{self.tag}>"
		return html_str
