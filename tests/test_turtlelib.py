import turtle
import unittest

from lib import printTextInTurtleWindow, PrintMode


class UnitTest(unittest.TestCase):
    def test_turtle_window_vertical(self):
        self.assertEqual(4, printTextInTurtleWindow("芒果帆帆"))

    def test_turtle_window_horizontal(self):
        self.assertEqual(4, printTextInTurtleWindow("芒果帆帆", PrintMode.horizontal))

    def tearDown(self):
        turtle.reset()


if __name__ == '__main__':
    unittest.main()