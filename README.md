# printPlay
本仓库初始 fork 自[此处](https://github.com/pengfexue2/printPlay)，在其基础上封装了使用 turtle 模块打印点阵汉字的功能。

## 开始
计划未来配套实现GUI，请参照`tests`下的测试脚本和`run_draw.py`来使用现在的半成品。

## 测试
实验性地配置了 unittest，测试内容会以 png 格式保存在`test/images`下。

运行测试之前，需要安装 ghostscript，否则 pillow 无法将绘图结果保存为 png 格式的图像。

Ghostscript：https://www.ghostscript.com/releases/gsdnld.html