from textnode import *

def main():
    dm1 = TextNode("My penus weenus", TextType.BOLD)
    dm2 = TextNode("actual link this time tho", TextType.LINK, "https://www.boot.dev")
    print(dm1)
    print(dm2)

main()
