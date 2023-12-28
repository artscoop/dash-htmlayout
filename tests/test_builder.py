import unittest

from lxml.etree import XMLSyntaxError

from src.dash.htmlayout import Builder


class BuilderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_simple_file(self):
        """Check that components are properly built from the HTML file."""
        builder = Builder(file="files/simple.html")
        dropdown = builder.get_component("color-dropdown")
        self.assertIsNotNone(dropdown)
        self.assertIsNone(builder.get_component("invalid-dropdown"))
        self.assertIn("Red", dropdown.options)

    def test_empty_file(self):
        """Check that the empty layout file creates no layout."""
        with self.assertRaises(XMLSyntaxError) as e:
            empty_builder = Builder(file="files/empty.html")
            self.assertIsNone(empty_builder.layout)


if __name__ == '__main__':
    unittest.main()
