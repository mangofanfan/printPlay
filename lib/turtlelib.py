import turtle as t

from enum import Enum

from .printlib import getRect

# 更改 SIZE大小即可更改字号大小。
SIZE = 15
# 除此之外不宜更改其他任何变量大小。

FONT_SIZE = 16 * SIZE


POS_TUPLE = tuple[int | float, int | float]


class PrintMode(Enum):
    vertical = 1
    horizontal = 2


def drawPoint(pos: POS_TUPLE, draw: bool, x_index: int, y_index: int):
    pos = (pos[0] + x_index * SIZE, pos[1] - y_index * SIZE)
    t.up()
    t.goto(*pos)
    if draw:
        t.down()
        t.forward(0.01 * SIZE)
        t.up()


def printTextInTurtleWindow(text: str, printMode: PrintMode = PrintMode.vertical, stay: bool = False) -> int:
    """
    使用 turtle 打印汉字，对传入参数 `text` 有限制如下。
    :param printMode: 打印模式，默认为 vertical。
    :param stay: 保持窗口显示（阻塞线程直至窗口关闭）。
    :param text: 需要为长度在2~4之间的汉字，传入其他内容可能导致显示错误。
    :return: 测试，返回长度。
    """
    t.shape("circle")
    t.width(SIZE)

    rect_list = getRect(text)

    start_pos: POS_TUPLE = (-len(text)/2 * FONT_SIZE, 0.5 * FONT_SIZE)

    if printMode == PrintMode.vertical:
        y_index = 0
        for row in rect_list:
            x_index = 0
            for i in row:
                drawPoint(start_pos, draw=i, x_index=x_index, y_index=y_index)
                x_index += 1
            y_index += 1
    elif printMode == PrintMode.horizontal:
        # 交换行列顺序打印
        for x_index in range(len(rect_list[0])):
            y_index = 0
            for row in rect_list:
                drawPoint(start_pos, draw=row[x_index], x_index=x_index, y_index=y_index)
                y_index += 1
    else:
        raise ValueError("printMode Error")

    if stay: t.done()

    return len(text)