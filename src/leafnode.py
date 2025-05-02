from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__( tag, value, None, props)
    def to_html(self):
        if(self.value == None):
            raise ValueError
        elif(self.tag == None):
            return self.value
        else:
            match self.tag:
                case "p" | "b" | "i" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "code" | "blockquote" | "li" | "ol" | "ul" | "span" | "div":
                    return f"<{self.tag}>{self.value}</{self.tag}>"
                case "a":
                    link = f"<{self.tag}"
                    keys = self.props.keys()
                    for key in keys:
                        link += f" {key}=\"{self.props[key]}\""
                    link += f">{self.value}</{self.tag}>"
                    return link
                case "img":
                    img = f"<{self.tag}"
                    keys = self.props.keys()
                    for key in keys:
                        img += f" {key}=\"{self.props[key]}\""
                    img += " />"
                    return img
                    
             
