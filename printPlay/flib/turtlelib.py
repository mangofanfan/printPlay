import turtle as t

from enum import Enum
from typing import Literal

from rich.console import Console
from rich.progress import track

from .printlib import getRect

SIZE = 15

POS_TUPLE = tuple[int | float, int | float]

DESC = "🐢 海龟正在努力中..."


class PrintMode(Enum):
    vertical = 1
    horizontal = 2


def drawPoint(pos: POS_TUPLE, draw: bool, x_index: int, y_index: int, size: int = SIZE):
    pos = (pos[0] + x_index * size, pos[1] - y_index * size)
    t.up()
    t.goto(*pos)
    if draw:
        t.down()
        t.forward(0.01 * size)
        t.up()


def printTextInTurtleWindow(text: str,
                            printMode: PrintMode = PrintMode.vertical,
                            stay: bool = False,
                            size: int = SIZE,
                            shape: Literal['arrow', 'blank', 'circle', 'classic', 'square', 'triangle', 'turtle'] = "circle",
                            speed: Literal['fastest', 'fast', 'normal', 'slow', 'slowest'] | int = "slow") -> int:
    """
    使用 turtle 打印汉字，对传入参数 `text` 有限制如下。
    :param speed: 海龟作画的速度，与 turtle 中的参数一致。
    :param shape: 海龟画笔的形状，与 turtle 中的参数一致。
    :param size: 每个点的直径或宽度。
    :param printMode: 打印模式，默认为 vertical。
    :param stay: 保持窗口显示（阻塞线程直至窗口关闭）。
    :param text: 需要为数个汉字，传入其他内容将导致显示错误。
    :return: 测试，返回长度。
    """
    t.shape(shape)
    t.width(size)
    t.shapesize(1, 1, 1)
    t.speed(speed)
    fontSize = 16 * size

    rect_list = getRect(text)

    start_pos: POS_TUPLE = (-len(text)/2 * fontSize, 0.5 * fontSize)

    if printMode == PrintMode.vertical:
        y_index = 0
        for row in rect_list:
            x_index = 0
            for i in row:
                drawPoint(start_pos, draw=i, x_index=x_index, y_index=y_index, size=size)
                x_index += 1
            y_index += 1
    elif printMode == PrintMode.horizontal:
        # 交换行列顺序打印
        for x_index in range(len(rect_list[0])):
            y_index = 0
            for row in rect_list:
                drawPoint(start_pos, draw=row[x_index], x_index=x_index, y_index=y_index, size=size)
                y_index += 1
    else:
        raise ValueError("printMode Error")

    if stay: t.done()

    return len(text)


def printTextInTurtleWindowWithProgressBar(console: Console,
                                           text: str,
                                           printMode: PrintMode = PrintMode.vertical,
                                           size: int = SIZE,
                                           shape: Literal['arrow', 'blank', 'circle', 'classic', 'square', 'triangle', 'turtle'] = "circle",
                                           speed: Literal['fastest', 'fast', 'normal', 'slow', 'slowest'] | int = "slow",) -> int:
    """
    使用 turtle 打印汉字，同时在控制台中显示进度条。
    :param speed: 海龟作画的速度，与 turtle 中的参数一致。
    :param shape: 海龟画笔的形状，与 turtle 中的参数一致。
    :param size: 每个点的直径或宽度。
    :param printMode: 打印模式，默认为 vertical。
    :param text: 需要为数个汉字，传入其他内容将导致显示错误。
    :param console: Rich中的控制台对象。
    :return: 测试，返回长度。
    """
    t.shape(shape)
    t.width(size)
    t.shapesize(1, 1, 1)
    t.speed(speed)
    fontSize = 16 * size

    rect_list = getRect(text)

    start_pos: POS_TUPLE = (-len(text)/2 * fontSize, 0.5 * fontSize)

    if printMode == PrintMode.vertical:
        y_index = 0
        for row in track(rect_list, description=DESC):
            x_index = 0
            for i in row:
                drawPoint(start_pos, draw=i, x_index=x_index, y_index=y_index, size=size)
                x_index += 1
            y_index += 1
    elif printMode == PrintMode.horizontal:
        # 交换行列顺序打印
        for x_index in track(range(len(rect_list[0])), description=DESC):
            y_index = 0
            for row in rect_list:
                drawPoint(start_pos, draw=row[x_index], x_index=x_index, y_index=y_index, size=size)
                y_index += 1
    else:
        raise ValueError("printMode Error")

    console.print()

    return len(text)