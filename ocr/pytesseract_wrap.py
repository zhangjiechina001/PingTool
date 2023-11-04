import pytesseract
import os
import cv2
from PIL import Image
from numpy import ndarray

from ocr.data.ocr_result import OcrResult

if os.path.exists("C:/Program Files/Tesseract-OCR/tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
elif os.path.exists("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"

print(pytesseract.get_languages(config=''))
print(pytesseract.get_tesseract_version())


class PytesseractWrap:
    def __init__(self, cv2_img:ndarray):
        cv2_img=cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB) if len(cv2_img.shape)==3 else cv2_img
        self.pil_img = Image.fromarray(cv2_img)
        self.enable_wordlist = False
        self.whitelist = ''
        self.psm = range(6, 14)
        self.oem = range(0, 2)

    def set_enable_wordlist(self, enable: bool):
        self.enable_wordlist = enable

    def set_whitelist(self, whitelist: str):
        self.whitelist = whitelist

    def link_command(self, psm_item, oem_item, enable_wordlist: bool, whitelist: str):
        ret = r'--psm {0} --oem {1}'.format(psm_item, oem_item)
        if whitelist != '':
            ret += ' -c tessedit_char_whitelist={0}'.format(whitelist)
        if enable_wordlist:
            ret += ' bazaar'
        return ret

    # 指令实例
    # tesseract 1.PNG stdout --psm 11 --oem 0 -c tessedit_char_whitelist=013456789Z bazaar

    def image_to_string(self, psm_item, oem_item, isTrim=False):
        try:
            # cmd = r'--psm {0} --oem {1} --user-words eng.user-words -c tessedit_char_whitelist={2} ' \
            #       r'-c load_system_dawg=true -c load_freq_dawg=true' \
            #       r'-c '.format(psm_item, oem_item, self.whitelist)
            cmd = self.link_command(psm_item, oem_item, self.enable_wordlist, self.whitelist)
            temp = pytesseract.image_to_string(self.pil_img, config=cmd, lang='eng')
        except BaseException as err:
            temp = 'err'
        return temp.replace(" ", "").replace("\t", "").replace("\n", "") if isTrim else temp

    def recognize(self) -> OcrResult:
        ocr_result = OcrResult(2, 14)
        for oem_item in self.oem:
            print('*' * 30)
            for psm_item in self.psm:
                self.image_to_string(psm_item, oem_item)
                temp = ''
                try:
                    cmd = r'--psm {0} --oem {1} --user-words eng.user-words -c tessedit_char_whitelist={2} ' \
                          r'-c load_system_dawg=true -c load_freq_dawg=true' \
                          r'-c '.format(psm_item, oem_item, self.whitelist)
                    cmd = self.link_command(psm_item, oem_item, self.enable_wordlist, self.whitelist)
                    temp = pytesseract.image_to_string(self.pil_img, config=cmd, lang='eng')
                except Exception as err:
                    temp = 'err'
                ocr_result.set_value(oem_index=oem_item, psm_index=psm_item, val=temp)

        return ocr_result


def cv_to_pil(cv_src):
    cvt_img = cv2.cvtColor(cv_src, cv2.COLOR_BGR2RGB)
    return cvt_img
