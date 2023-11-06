import unittest

from src.dash.htmlayout import Builder


class BuilderTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = Builder(file="files/simple.html")

    def test_simple_file(self):
        print(self.builder.layout)

if __name__ == '__main__':
    unittest.main()
