import os

import cv2
import pytesseract
from PIL import Image
from numpy import ndarray
from tkinter import filedialog
import tkinter as tk
from ocr.data.ocr_result import OcrResult
import ocr.pytesseract_wrap



class MouseCutOut:
    def __init__(self, image):
        self.img_cut = None
        self.whitelist = None
        self.psm = range(0, 14)
        self.oem = range(0, 2)
        self.ix = None
        self.iy = None
        self.image = image
        self.drawing = False

    def setmode(self, oem: list, psm: list, whitelist: str):
        self.oem = oem
        self.psm = psm
        self.whitelist = whitelist
        print(self.whitelist)

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                img_copy = self.image.copy()
                cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 255), 1)
                cv2.imshow("Image", img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.img_cut = self.image[self.iy:y, self.ix:x]

    def recognize_ocr(self):
        # 将OpenCV图像转换为PIL图像
        if self.img_cut is None:
            return
        cvt_img = cv2.cvtColor(self.img_cut, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cvt_img)
        # r'--psm 8 --oem 2 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.'
        os.system('cls')
        ocr_result = OcrResult(4, 14)
        for oem_item in self.oem:
            print('*' * 30)
            for psm_item in self.psm:
                temp = ''
                try:
                    cmd = r'--psm {0} --oem {1} --user-words eng.user-words -c tessedit_char_whitelist={2} ' \
                          r'-c load_system_dawg=true -c load_freq_dawg=true' \
                          r'-c '.format(psm_item, oem_item,self.whitelist)
                    temp = pytesseract.image_to_string(pil_image, config=cmd, lang='eng')
                except Exception as err:
                    temp = 'err'
                ocr_result.set_value(oem_index=oem_item, psm_index=psm_item, val=temp)
        ocr_result.print_format()

    def show(self):
        cv2.imshow('Image', self.image)
        cv2.setMouseCallback("Image", self.draw_rectangle)
        cv2.waitKey()

        # for i in range(0, 14):
        #     try:
        #         # oem 0 Leagcy
        #         # oem 1 lstm
        #         cmd = r'--psm {0} --oem 2 -c tessedit_char_whitelist=0123456789.'.format(i)
        #         print(i, pytesseract.image_to_string(pil_image, config=cmd, lang='eng'))
        #     except Exception as err:
        #         print(i, '--')

        # custom_config = r'--psm 1 --oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.'
        # # 获取识别的字符边界框
        # detection_boxes = pytesseract.image_to_boxes(pil_image, output_type=pytesseract.Output.STRING, lang='eng',config=custom_config)
        # print(pytesseract.image_to_data(pil_image, config=custom_config, lang='eng'))
        # img_h, img_w, _ = img.shape
        # # 遍历每个字符的边界框并绘制方框
        # for box in detection_boxes.splitlines():
        #     box = box.split()
        #     # 矩形的两个对角点
        #     x1, y1, x2, y2 = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        #     cv2.rectangle(img, (x1, img_h - y1), (x2, img_h - y2), (0, 255, 0), 1)
        #     # cv2.putText(image_cv, x,(x, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #     cv2.putText(img, box[0], (x1, img_h - y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)

        # cv2.imshow("cut", img)


class MouseUI:

    def __init__(self, root_ui):
        self.open_button = tk.Button(root_ui, text="Open Image", command=self.open_file)
        self.open_button.pack()
        self.setmid(root_ui)

    # 创建一个回调函数来加载图像
    def open_file(self):
        file_path = filedialog.askopenfilename()  # 打开文件对话框
        if file_path:
            # 使用OpenCV读取图像
            img = cv2.imread(file_path)
            resize_img = img
            cv2.imshow("Image", resize_img)
            cutout = MouseCutOut(resize_img)
            cv2.waitKey()

    def setmid(self, root):
        window_width = 580
        window_height = 280
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")


# 读取图像
# img = cv2.imread('image/ThinCharacter/Image_20231024161234704.bmp')
# resize_img = cv2.resize(img, (1920, 1080))
# cv2.imshow("Image", resize_img)
# cutout = MouseCutOut(resize_img)
# cv2.waitKey()

if __name__ == '__main__':
    ui_root = tk.Tk()
    ui_root.title("OpenCV File Open")
    ui = MouseUI(ui_root)
    # Set the protocol to call the on_closing function when the window is closed
    # ui_root.protocol("WM_DELETE_WINDOW", lambda : cv2.destroyAllWindows())
    ui_root.mainloop()
