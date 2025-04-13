import os
import turtle
import unittest

from PIL import Image

from printPlay.flib import printTextInTurtleWindow, PrintMode


class TurtleTest(unittest.TestCase):
    def test_turtle_window_speed(self):
        self.assertEqual(4, printTextInTurtleWindow("芒果帆帆", speed='fastest'))

    def test_turtle_window_horizontal(self):
        self.assertEqual(4, printTextInTurtleWindow("荔枝桃桃", PrintMode.horizontal))

    def test_turtle_window_square(self):
        self.assertEqual(4, printTextInTurtleWindow("柠檬酸酸", shape="square"))

    def test_turtle_window_size(self):
        self.assertEqual(4, printTextInTurtleWindow("草莓甜甜", size=4))

    def tearDown(self):
        try:
            os.makedirs(os.path.dirname(__file__) + "/images", exist_ok=True)
            filePath = os.path.dirname(__file__) + f"/images/output_{TurtleTest.index}.ps"

            TurtleTest.index += 1

            canvas = turtle.getscreen().getcanvas()
            canvas.postscript(file=filePath)  # 生成 output.ps

            with open(filePath, "rb") as f:
                image = Image.open(f)
            image.save(filePath + ".png")

        except OSError as e:
            print("保存测试图像时出现错误，请确认正确安装 Ghostscript 并配置环境变量。")
            print("本次测试将抛出错误，但这不是代码层面的原因。")
            raise e

        finally:
            # 保存图像过程中发生异常时，清空画布以继续测试
            turtle.reset()

    @classmethod
    def setUpClass(cls) -> None:
        cls.index = 0

    @classmethod
    def tearDownClass(cls):
        turtle.done()


if __name__ == '__main__':
    unittest.main()