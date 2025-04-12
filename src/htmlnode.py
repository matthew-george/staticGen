class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, HTMLNodeB):
        return self.tag == HTMLNodeB.tag and self.value == HTMLNodeB.value and self.children == HTMLNodeB.children and self.props == HTMLNodeB.props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag},\nvalue: {self.value},\nchildren: {self.children},\nprops: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: No value")
        if self.tag is None:
            return self.value
        return f"<{(self.tag + " " + self.props_to_html()).strip()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag: {self.tag},\nvalue: {self.value},\nprops: {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: No tag")
        if self.children is None:
            raise ValueError("Invalid HTML: No children")
        return f"<{(self.tag + " " + self.props_to_html()).strip()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag: {self.tag},\nchildren: {self.children},\nprops: {self.props})"