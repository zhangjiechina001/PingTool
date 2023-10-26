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
        for j in range(self.psm_count):
            print('psm {0}'.format(j), end='\t')
        print()

        for i in range(self.oem_count):
            print('oem {0}'.format(i), end='\t')
            for j in range(self.psm_count):
                print(self.matrix[i, j], end="\t")
            print()  # 在行结束后换行
