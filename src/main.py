from textnode import TextNode, TextType

def main():
    node = TextNode("Hello, World!", TextType.BOLD, "http://example.com")
    print(node)

main()
