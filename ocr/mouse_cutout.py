import cv2
import pytesseract
from PIL import Image
from numpy import ndarray
from tkinter import filedialog
import tkinter as tk

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
print(pytesseract.get_languages(config=''))


class MouseCutOut:
    def __init__(self, image):
        self.iy = None
        self.ix = None
        self.image = image
        self.drawing = False
        cv2.setMouseCallback("Image", self.draw_rectangle)

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
            img_cut = self.image[self.iy:y, self.ix:x]
            self.draw_ocr(img_cut.copy())

    def draw_ocr(self, img):
        # 将OpenCV图像转换为PIL图像
        pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # r'--psm 8 --oem 0 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        custom_config = r'--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        # 获取识别的字符边界框
        detection_boxes = pytesseract.image_to_boxes(pil_image, output_type=pytesseract.Output.STRING, lang='eng',
                                                     config=custom_config)
        print(pytesseract.image_to_data(pil_image, config=custom_config, lang='eng'))
        img_h, img_w, _ = img.shape
        # 遍历每个字符的边界框并绘制方框
        for box in detection_boxes.splitlines():
            box = box.split()
            # 矩形的两个对角点
            x1, y1, x2, y2 = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv2.rectangle(img, (x1, img_h - y1), (x2, img_h - y2), (0, 255, 0), 1)
            # cv2.putText(image_cv, x,(x, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(img, box[0], (x1, img_h - y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)

        cv2.imshow("cut", img)


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
# img = cv2.imread('image/FineBody/Image_20231024161234704.bmp')
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
