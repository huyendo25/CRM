import re
import cv2
from PIL import Image
import pytesseract
from pytesseract import Output
import os
import numpy as np
import time
import base64

# Đổi thành chữ không dấu
def no_accent_vietnamese(s):
    # input: ký tự có dấu
    # output: ký tự không dấu
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

# Xóa các dấu câu
def no_end(s):
    s = re.sub(r'[.,;!?:`~—#-]', '', s)
    return s

def imageToBase64(image):
##    imencode mã hóa định dạng img thành data truyền trực tuyến và gán nó vào bộ nhớ đệm
##    nén định dạng dữ liệu hình ảnh để tạo điều kiện cho việc truyền mạng
##    b64encode mã hóa hình ảnh thành nhị phân hiển thị bằng ASCII
##    decode chuyển dạng mã hóa về string
    
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    image_data = jpg_as_text.decode("utf-8")
    image_data = str(image_data)
    #print(image_data)    # print(image_data)
    image_data = 'data:image/png;base64,' + image_data
    return image_data

# Sử dụng tesseract để predict
def tesseract_predict(image):
    # sử dụng thư viện pytesseract để trích xuất text từ ảnh
    # đọc ảnh => chuyển xám => áp dụng pytesseract
    # input: ảnh
    # output: result: dạng dict gồm
    #level,page_num,block_num,par_num,line_num,word_num,
    #left,top,weight,height,conf,text
    
    # Đọc ảnh đầu vào
    image = cv2.imread(image)
    img_org = image.copy()
    img_org_base64 = imageToBase64(img_org)

    # Chuyển về ảnh xám đặt ngưỡng threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #image = cv2.GaussianBlur(image, (1, 1), 0)
    #gray = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #text = pytesseract.image_to_string(Image.open(filename),config='--psm 4 + --oem 2', lang='vie')

    # Trả về đặc tính các từ
    results = pytesseract.image_to_data(gray,config='--psm 4 + --oem 2', output_type=Output.DICT, lang='vie')
    
    return results,img_org_base64

# Tìm chuỗi khớp
def findText (text_change_org, results):
##    input: chuỗi muốn tìm kiếm, biến results kiểu dict 
##    output: trả về kiểu [index từ 1, index từ 2, ...],
##    trả về index của các chữ cái có trong chuỗi tìm kiếm
##    (index này là của toàn bộ các chữ nhận diện được trong ảnh)

    text_change = no_end(no_accent_vietnamese(text_change_org))
    # text_change = text_change.lower()
    text_change = text_change.split(' ')
    text_change = [text_remove for text_remove in text_change if text_remove != '']
    # tìm chuỗi khớp cả câu
    bien_check = 0
    j = 0
    paint_list = []
    paint_cong = []
    i = 0
    if len(text_change) != 1:
        while i < len(results["text"]):
            if no_end(results["text"][i]).replace(' ', '') != '':
                if bien_check % 2 == 0 and no_end(text_change[0]) == no_end(
                        no_accent_vietnamese(results["text"][i])):
                    bien_check += 1
                    paint_cong.append(i)
                    j = j + 1
                    i = i + 1
                    continue
                if bien_check % 2 == 1:
                    if no_end(text_change[j]) == no_end(no_accent_vietnamese(results["text"][i])):
                        if (j + 1) == len(text_change):
                            paint_cong.append(i)
                            j = 0
                            i = i + 1
                            bien_check += 1
                            paint_list += paint_cong
                            paint_cong = []
                            continue

                        j = j + 1
                        paint_cong.append(i)
                        i = i + 1
                        continue
                    else:
                        j = 0
                        paint_cong = []
                        bien_check = 0
                        i = i - 1
            i = i + 1
    else:
        while i < len(results["text"]):
            if float(results["conf"][i]) > 50:
                if no_end(text_change[0]) == no_end(no_accent_vietnamese(results["text"][i])):
                    paint_list.append(i)
                    i = i + 1
                    continue
            i += 1
    # print(paint_list)
    return paint_list
