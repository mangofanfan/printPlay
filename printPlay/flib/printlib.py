import binascii
import os
KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

def getRect(textStr):
    # 初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示，需要32个字节才能显示一个汉字
    # 之所以32字节：256个点每个点是0或1，那么总共就是2的256次方，一个字节是2的8次方
    rect_list = [] * 16
    for i in range(16):
        rect_list.append([] * 16)

    for text in textStr:
        #获取中文的gb2312编码，一个汉字是由2个字节编码组成
        # 在此处处理错误
        try:
            gb2312 = text.encode('gb2312')
        except UnicodeEncodeError:
            raise CharacterError(textStr, text)
        #将二进制编码数据转化为十六进制数据
        hex_str = binascii.b2a_hex(gb2312)
        #将数据按unicode转化为字符串
        result = str(hex_str, encoding='utf-8')

        #前两位对应汉字的第一个字节：区码，每一区记录94个字符
        area = eval('0x' + result[:2]) - 0xA0
        #后两位对应汉字的第二个字节：位码，是汉字在其区的位置
        index = eval('0x' + result[2:]) - 0xA0
        #汉字在HZK16中的绝对偏移位置，最后乘32是因为字库中的每个汉字字模都需要32字节
        offset = (94 * (area-1) + (index-1)) * 32

        font_rect = None

        #读取HZK16汉字库文件
        with open(os.path.dirname(__file__) + "/HZK16", "rb") as f:
            #找到目标汉字的偏移位置
            f.seek(offset)
            #从该字模数据中读取32字节数据
            font_rect = f.read(32)

        #font_rect的长度是32，此处相当于for k in range(16)
        for k in range(len(font_rect) // 2):
            #每行数据
            row_list = rect_list[k]
            for j in range(2):
                for i in range(8):
                    asc = font_rect[k * 2 + j]
                    #此处&为Python中的按位与运算符
                    flag = asc & KEYS[i]
                    #数据规则获取字模中数据添加到16行每行中16个位置处每个位置
                    row_list.append(flag)

    return rect_list


def printTextInCil(textStr: str, line: str = '■', background: str = '○') -> None:
    """
    在控制台打印给出的汉字
    :param textStr: 给出汉字，长度任意
    :param line: 构成点阵图案的字符
    :param background: 构成点阵背景的字符
    :return: 无返回值，会在控制台打印点阵。
    """
    rect_list = getRect(textStr)
    #根据获取到的16*16点阵信息，打印到控制台
    for row in rect_list:
        for i in row:
            if i:
                #前景字符（即用来表示汉字笔画的输出字符）
                print(line, end=' ')
            else:

                # 背景字符（即用来表示背景的输出字符）
                print(background, end=' ')
        print()


class CharacterError(Exception):
    def __init__(self, textStr: str, text: str) -> None:
        self.textStr = textStr
        self.text = text

    def __str__(self) -> str:
        return (f"😱 Character Error: {self.textStr} {self.text}\n"
                f"❌ 文本「{self.textStr}」中的「{self.text}」无法被转为 GB2312 编码。\n"
                f"❌ 因此，printPlay 无法将其转为点阵，也无法将其打印。这并非是程序或您的问题。\n"
                f"✅ 请尝试将「{self.text}」替换成其他文本，并再次尝试。\n"
                f"👀 注意，「{self.text}」可能并非文本「{self.textStr}」中唯一无法被转为 GB2312 编码的文字。")
