import numpy as np


class OcrResult:
    def __init__(self, oem_count, psm_count):
        self.oem_count = oem_count
        self.psm_count = psm_count
        self.matrix = np.empty((oem_count, psm_count), dtype=np.dtype('U50'))

    def set_value(self, oem_index, psm_index, val: str):
        # 使用空字符串替换所有空白字符（空格、制表符、换行等）
        cleaned_text = val.replace(" ", "").replace("\t", "").replace("\n", "")
        self.matrix[oem_index, psm_index] = cleaned_text

    def print_format(self):
        # 打印包含表头的二维数组
        print('oem\\psm', end='\t')
        psm_names=['方向及语言检测','自动图片分割','自动图片分割(No OSD)','完全的自动图片分割','假设有一列不同大小的文本','假设有一个垂直对齐的文本块','假设有一个对齐的文本块',
                   '图片为单行文本','图片为单词','图片为圆形的单词','图片为单个字符','稀疏文本','OSD稀疏文本','将图像视为单个文本行']
        for j in range(self.psm_count):
            print(psm_names[j], end='\t')
        print()

        oem_names=['Legacy','LSTM']
        for i in range(2):
            print(oem_names[i], end='\t')
            for j in range(self.psm_count):
                print(self.matrix[i, j], end="\t")
            print()  # 在行结束后换行
