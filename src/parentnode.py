from htmlnode import *
from leafnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if(self.tag == None):
            raise ValueError("Parent missing tag")
        else:
          html_string = ""
          for child in self.children:
            if(child.value == None and child.children  == None):
                raise ValueError("Child missing value")
            else:
                html_string += child.to_html()
          return f"<{self.tag}>{html_string}</{self.tag}>"    
