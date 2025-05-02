class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        attr_string = ""
        for attr in self.props:
            attr_string += f" {attr}=\"{self.props[attr]}\""
        return attr_string
    def __eq__(self, rhs):
        return (self.tag == rhs.tag and
                self.value == rhs.value and
                self.children == rhs.children and
                self.props == rhs.props)
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
        
