class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res = ""
        for k in self.props:
            res += f' {k}="{self.props[k]}"'
        return res

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props or {})

    def to_html(self):
        if not self.value:
            raise ValueError
        elif not self.tag:
            return self.value
        else:
            props_str = self.props_to_html()
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props or {})

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag found")
        elif not self.children:
            raise ValueError("ParentNode should have children")

        inner_html = "".join(child.to_html() for child in self.children)
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{inner_html}</{self.tag}>"

