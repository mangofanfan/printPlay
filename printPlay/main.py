import time
import turtle
from typing import Literal

import rich_click as click

from rich.console import Console
from rich.panel import Panel

from flib import *

cil = Console(color_system="truecolor")
click.rich_click.ERRORS_SUGGESTION = "运行 --help 以获得命令帮助。"
click.rich_click.ERRORS_EPILOGUE = "如果您判定此问题不该出现，请考虑将其作为 issue 提交到 GitHub 仓库 [link=https://github.com]printPlay[/link]。"


@click.command()
@click.option("-t", "--text", help="待绘制的文字。", type=str, show_default=True, prompt="⬅️ 请输入待绘制的文字")
@click.option("-si", "--size", help="海龟绘图的笔画尺寸，与绘制结果的字体大小正相关。", default=10, show_default=True)
@click.option("-sp", "--speed", help="海龟绘图速度，范围在1~10之间。", default=5, show_default=True)
@click.option("-m", "--mode", help="海龟的绘图方向，h（纵向横移）或v（横向纵移）", default="v", show_default=True)
@click.option("-p", "--print", "print_rect", is_flag=True, help="在控制台打印文字的点阵预览。", default=False, show_default=True)
@click.option("-s", "--save", "save", is_flag=True, help="保存绘制完成的结果为图片", default=False, show_default=True)
def main(text: str, size: int, speed: int, mode: Literal["v", "h"], print_rect: bool, save: bool):
    """通过海龟库绘制汉字点阵的简单实现，也支持在控制台输出点阵。"""

    # 命令行署名
    cil.clear()
    cil.print(Panel((f"🥭 [bold green]printPlayDraw[/bold green] | 使用海龟绘制点阵汉字的命令行工具~\n"
                     f"👀 本工具[yellow]只能打印 [bold]GB2312[/bold] 编码包含的6000+常用汉字[/yellow]。如果给出汉字不在此范围内，您将收到错误。\n"
                     f"👌 运行前参数预览 | {text=} | {size=} | {speed=} | {print_rect=}"), title="~ 欢迎使用 printPlayDraw ~"))
    cil.print()

    # 传入数据校验
    stop = False
    if (length := len(text)) <= 0:
        cil.print(f"❌ [bold yellow]text 参数错误：[/bold yellow]请提供可供打印的中文文本。")
        stop = True
    if (size := int(size + 0.5)) < 1:
        cil.print(f"❌ [bold yellow]size 参数错误：[/bold yellow]size 不能为负数。")
        stop = True
    if speed not in range(1, 11):
        cil.print(f"❌ [bold yellow]speed 参数错误：[/bold yellow]speed 需要在 1~10 之间。")
        stop = True
    if mode not in ["v", "h"]:
        cil.print(f"❌ [bold yellow]mode 参数错误：[/bold yellow]mode 需要为 v 或 h。")
        stop = True

    if stop:
        cil.print("❌ [red]参数错误，命令行结束。[/red]")
        click.pause()
        return

    # 编码检验
    try:
        rect_list = getRect(text)
    except CharacterError as e:
        cil.print(Panel(str(e), title="[red]给出的文本无法被打印[/red]", border_style="red"))
        cil.print("❌ [bold yellow]这不是程序或您的问题，请更换文本再次尝试打印吧...[/bold yellow]")
        click.pause()
        return

    if print_rect:
        cil.print(f"😄 将在下方预览打印文本「[bold yellow]{text}[/bold yellow]」的点阵结果...")

        i = 1
        cil.print("[ x ]", end=" ")
        for j in range(1, len(rect_list[0]) + 1):
            cil.print(j % 10, end=" ")
        cil.print("✅")
        for line in rect_list:
            cil.print(f"[ {i % 10} ]", end=" ")
            for char in line:
                cil.print('■' if char else ' ', end=" ")
            cil.print("✅")
            i += 1

    try:
        cil.print(f"😊 正在海龟窗口中绘制文本：「[bold yellow]{text}[/bold yellow]」（{size=} | {speed=}）")
        t1 = time.time()
        printTextInTurtleWindowWithProgressBar(console=cil,
                                               text=text,
                                               size=size,
                                               printMode=PrintMode.vertical if mode == "v" else PrintMode.horizontal,
                                               speed=speed)
        t2 = time.time()
        cil.print(f"✅ [green]绘制已完成。[/green]（绘图耗时：[yellow]{t2-t1}s[/yellow] | 字数 {length}）")

    except turtle.Terminator:
        cil.print("⚠️ 海龟窗口在绘图过程中被关闭，[yellow]绘制未完成而被迫结束。[/yellow]")

    else:
        # 如果需要保存
        if save:
            cil.print()
            cil.print("🎇 保存绘图结果为图片...")
            try:
                import os
                from PIL import Image
                os.makedirs(os.path.dirname(__file__) + "/images", exist_ok=True)
                filePath = os.path.dirname(__file__) + f"/images/{text}_{size}.ps"

                canvas = turtle.getscreen().getcanvas()
                canvas.postscript(file=filePath)  # 生成 output.ps

                with open(filePath, "rb") as f:
                    image = Image.open(f)
                image.save(filePath + ".png")
                cil.print(Panel((f"🎇 PS 格式文件保存于 [yellow]{filePath}[/yellow]\n"
                                 f"🎇 PNG 图片保存于 [yellow]{filePath + '.png'}[/yellow]\n"
                                 f"✅ 图片保存完成~"),
                                border_style="green"))

            except OSError as e:
                cil.print(Panel((f"❌ OSError {str(e)}\n"
                                 f"❌ 这一般是由于您的设备上[yellow]未安装 GhostScript[/yellow]，或其环境变量配置存在问题，导致 printPlayDraw 无法基于其处理图片。"
                                 f"✅ GhostScript 的安装程序会自动添加环境变量，请自行安装，然后重试。"
                                 f"👀 或者使用您自己的截图工具截取绘图结果~"),
                                title="[red]GhostScript 未安装 保存图片失败[/red]",
                                border_style="red"))
            except ImportError as e:
                cil.print(Panel((f"❌ ImportError {str(e)}\n"
                                 f"❌ PIL 是选装包，请检查当前 PIL 是否安装，printPlayDraw 需要 PIL 库来保存图片。"
                                 f"✅ 请在环境中（或全局）运行 pip install pillow 来安装 PIL，并请另外安装 GhostScript 来确保正常处理图片。"
                                 f"👀 或者使用您自己的截图工具截取绘图结果~"),
                                title="[red]PIL 未安装 保存图片失败[/red]",
                                border_style="red"))

        cil.print(f"🚶‍♀️ 在您关闭海龟窗口之后，命令行程序将结束。")
        turtle.mainloop()
    click.pause()
    return


if __name__ == "__main__":
    main()