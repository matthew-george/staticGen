import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>", "testValue")
        node2 = HTMLNode("<p>", "testValue")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        samepl_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p","testValue", None, samepl_props)
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node2 = LeafNode("p", "Hello, world!")
        node = ParentNode("p", [child_node, child_node2])
        missing_children_node = ParentNode("p", None)
        self.assertEqual(node.to_html(), '<p><a href="https://www.google.com">Click me!</a><p>Hello, world!</p></p>')
        with self.assertRaises(ValueError):
            missing_children_node.to_html()

    def test_to_html_with_nested_children(self):
        nested_child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("p", [nested_child_node])
        node = ParentNode("p", [child_node])
        self.assertEqual(node.to_html(), '<p><p><a href="https://www.google.com">Click me!</a></p></p>')

    # def test_to_html_missing_children(self):
    #     node = ParentNode("p", None)
    #     self.assertEqual(node.to_html(), None)
    #     with self.assertRaises(ValueError):
    #         node.to_html()


if __name__ == "__main__":
    unittest.main()
