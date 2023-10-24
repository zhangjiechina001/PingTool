import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd="C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
# 读取图像
image = Image.open('fullimg.bmp')

# 使用Pytesseract进行字符识别
text = pytesseract.image_to_string(image)

# 将图像转换为OpenCV格式
image_cv = cv2.cvtColor(cv2.imread('fullimg.bmp'), cv2.COLOR_BGR2RGB)

# 获取识别的字符边界框
detection_boxes = pytesseract.image_to_boxes(image)

img_h,img_w,_=image_cv.shape
# 遍历每个字符的边界框并绘制方框
for box in detection_boxes.splitlines():
    box = box.split()
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    cv2.rectangle(image_cv, (x, y), (w, h), (0, 255, 0), 2)
    # cv2.putText(image_cv, x,(x, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.putText(image_cv, box[0], (x, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

# 显示带有方框标注的图像
cv2.imshow('Image with Boxes', image_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()
