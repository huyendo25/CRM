from wand.image import Image as Img
from wand.color import Color
from pdf2image import convert_from_path
from subprocess import check_output
import argparse
from docx import Document
from docx2pdf import convert
from findText import *
from replaceString import *
from pdf2docx import Converter
import base64
from subprocess import Popen
from PyPDF2 import PdfFileReader
import time

# Xây dựng hệ thống tham số đầu vào
# ap = argparse.ArgumentParser()
# # -f : file đầu vào
# ap.add_argument("-f", "--file", required=True)
# args = vars(ap.parse_args())

# Xử lý file đầu vào

def input_file_processing(input_file):
##    input: file cần xử lý
##    output: file pdf/doc/docx, lưu trong folder chứa input_file
    
    # Xử lý file đầu vào
    doc_end = ['.docx', '.doc']
    pdf_end = ['.pdf']

    input_file_name, input_file_end = os.path.splitext(input_file)

    # Tiếm kiếm nếu đầu vào là file doc docx
    if input_file_end in doc_end:
        input_pdf , output_file = convert_file_word(input_file_name,input_file)
        doc = Document(input_file)
        doc.save(output_file) #lưu lại output_file
        return input_pdf, output_file

    # Nếu đầu vào là file pdf
    elif input_file_end in pdf_end:
        input_pdf, output_file = convert_file_pdf(input_file_name,input_file)
        return input_pdf, output_file
    # # Đầu vào khác docx , doc , pdf , jpg , png
    # else:
    #     print("Ko đúng định dạng yêu cầu")

def convert_file_word(input_file_name,input_file):
##    input: tên file word, folder chứa file word, folder đầu ra
##    output: input_pdf file pdf đầu ra, file word_output
    # Convert doc , docx to pdf
    time_1 = time.time()
    # convert trên window
    convert(input_file)
    # convert trên linux
##    LIBRE_OFFICE = r"/usr/bin/lowriter"
##    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
##               out_folder, input_file])
    # print([LIBRE_OFFICE, '--convert-to', 'pdf', input_file])
    #p.communicate()
    time_c = time.time()  # Time khi kết thúc
    fps = time_c - time_1
    print("Thời gian đổi từ word sang pdf : {}".format(fps))

    # Output = file pdf
    input_pdf = input_file_name + '.pdf'
    output_file = input_file_name + '_output.docx'
    return input_pdf,output_file

def convert_file_pdf(input_file_name,input_file):
##    input: tên file word, folder chứa file word, folder đầu ra
##    output: input_pdf file pdf đầu ra, file word_output
    # Output = file pdf
    input_file_docx = input_file_name + '.docx'
    output_file = input_file_name + '_output.docx'

    # Convert pdf to docx
    time_1 = time.time()
    cv = Converter(input_file)
    cv.convert(output_file)  # all pages by default
    cv.close()
    time_c = time.time()  # Time khi kết thúc
    fps = time_c - time_1
    print("Thời gian chuyển từ pdf to sang word: {}".format(fps))
    return input_file , output_file

# Đếm số trang pdf
##def get_num_pages(pdf_path):
##    pdf = PdfFileReader(open(pdf_path,'rb'))
##    num_pages = pdf.getNumPages()
##    return num_pages

# Tạo folder ảnh theo các trang pdf
def pdf_to_img(input_file):

##    đổi từ PDF sang Image
##    input: đường dẫn
##    output: save ảnh .jpg
    time_1 = time.time()
    folder = input_file.split('.pd')[0] + '_img' # tên folder chứa ảnh
    input_folder,name = folder.split("/")
    all_pages = Img(filename=input_file, resolution=300) # PDF với nhiều trang
    for idx, page in enumerate(all_pages.sequence):
        with Img(page) as img:
            img.compression_quality = 99
            img.format = 'png' 
            img.background_color = Color('white')  # cài white background
            img.alpha_channel = 'remove'  # loại bỏ nền ảnh trong suốt
            img.save(filename=f'{folder}/{name}_{idx}.png')
    time_c = time.time()
    fps = time_c - time_1
    print("Thời gian chuyển pdf sang ảnh : {}".format(fps))
    return folder

# Dự đoán từ , tô và ghép ảnh
def ocr_folder_image(input_image):
##    lấy file trong thư mục input_image đưa vào hàm tesseract_predict
##    đọc ảnh, xử lý ảnh, trích xuất text và chuyển ảnh thành data truyền mạng
##    đơn thuần kết hợp các hàm
##    input: ảnh
##    output: results - text đọc qua pytesseract, ảnh dạng truyền trực tuyến
    time_t = time.time()
    results = {}
    img_org_base64 = {}
    files = os.listdir(input_image)
    for file in files:
        input_file_anh = input_image + '/' + file
        results[file] , img_org_base64[file] = tesseract_predict(input_file_anh)
    time_s = time.time()
    print("Thời gian xử lý và dự đoán ảnh : {}".format(time_s-time_t))
    return results,img_org_base64


def color_yellow(image, paint_list, results, text_change_org):
##    input: img, từ tìm kiếm, paint_list là
##    index của 1 từ (có thể hơn 2 chữ) trong ảnh == từ tìm kiếm
##    result là kiểu dict gồm tọa độ từ, text,...
##    
##    output: tô vàng phần chữ == chữ tìm kiếm => img được mã hóa
    input_img, img_end = os.path.splitext(image)
    image_output = input_img + '_output' + img_end
    img = cv2.imread(image)
    img1 = img.copy()
    text_change = no_end(no_accent_vietnamese(text_change_org))
    text_change = text_change.split(' ')
    text_change = [text_remove for text_remove in text_change if text_remove != '']
    h_max = 0
    x_index = paint_list[0]
    for i in range(len(paint_list)):
        # extract the bounding box coordinates of the text region from
        # the current result
        h = results["top"][paint_list[i]] + results["height"][paint_list[i]]
        
        if h > h_max:
            h_max = h
        if (i + 1) % len(text_change) == 0:
            x_t = results["left"][x_index]
            x_s = results["left"][paint_list[i]]
            y = min(results["top"][x_index: paint_list[i] + 1])
            w = results["width"][paint_list[i]]
            #kiểm tra nền tô hay không
            for j in range(x_t, x_s + w):
                for k in range(y, h_max):
                    if 175 < img1[k][j][0] <= 255 and 175 < img1[k][j][1] <= 255 and 175 < img1[k][j][2] <= 255:
                        img1[k][j][0] = 0
                        img1[k][j][1] = 255
                        img1[k][j][2] = 255

            #cv2.imwrite(image_output, img1)
            #cv2.imshow(image_output, img1)
            h_max = 0

            # chuyển sang chữ sau
            if i < len(paint_list) - 1:
                x_index = paint_list[i + 1]
            continue

        #nếu là từ cuối của dòng
        if results["word_num"][paint_list[i + 1]] - results["word_num"][paint_list[i]] < 0:
            x_t = results["left"][x_index]
            x_s = results["left"][paint_list[i]]
            y = min(results["top"][x_index:paint_list[i] + 1])
            w = results["width"][paint_list[i]]
            # Tô vàng
            for j in range(x_t, x_s + w):
                for k in range(y, h_max):
                    if 175 < img1[k][j][0] <= 255 and 175 < img1[k][j][1] <= 255 and 175 < img1[k][j][2] <= 255:
                        img1[k][j][0] = 0
                        img1[k][j][1] = 255
                        img1[k][j][2] = 255
            h_max = 0
            x_index = paint_list[i + 1]
            continue
    #cv2.imwrite(image_output, img1)
    return imageToBase64(img1)

def find_paint_list(text_change_org,input_image,results):
##    lấy danh sách index các từ qua hàm 
##    xử lý chuỗi tìm kiếm text_change_org
##    đếm trong ảnh vị trí từ == text_change_org
     
##    input: từ tìm kiếm, img, text trích xuất từ img
##    output: { STT: { img : [index,index] ...}, {}, ...}
##    STT của các từ == từ tìm kiếm (VD 10 từ: 123...10)
##    img: tên ảnh
##    danh sách index các từ == từ tìm kiếm
##    (index này là thứ tự của toàn bộ các chữ nhận diện được trong ảnh)
    
    paint_dic = {} # ảnh và vị trí của từ trong ảnh
    
    files = os.listdir(input_image)
    print(input_image)
    # Tìm chuỗi khớp trong từng ảnh
    for i in range(len(files)):
        file = files[i]
        paint_dic[file] = findText(text_change_org, results[file])
        if paint_dic[file] == []:
            del paint_dic[file]

    # print(paint_dic)
    text_change = no_end(no_accent_vietnamese(text_change_org))
    text_change = text_change.split(' ')
    text_change = [text_remove for text_remove in text_change if text_remove != '']
    # print(text_change)

    counter = -1
    dic_stt = {}  # số thứ tự của từ trong cả file pdf
    len_text_change = len(text_change)
    
    for file in paint_dic:
        list_paint_stt = []
        for i in range(len(paint_dic[file])):
            list_paint_stt.append(paint_dic[file][i])
            if (i + 1) % len_text_change == 0:
                counter += 1
                dic_stt[counter] = {file: list_paint_stt}
                list_paint_stt = []
    # print(dic_stt)
    return dic_stt


def text_processing(text_change_org,stt,input_image,results,dic_stt):
##    input: từ tìm kiếm, STT, ảnh, results, dic_stt
##    STT của các từ == từ tìm kiếm (VD 10 từ: 123...10)
##    img: tên ảnh
##    results: kiểu dict gồm tọa độ từ, text,...
##    dic_stt danh sách index các từ == từ tìm kiếm
##    (index này là thứ tự của toàn bộ các chữ nhận diện được trong ảnh)
##    img được tô vàng từ tìm kiếm, data theo kiểu truyền mạng
    for file in dic_stt[stt]:
        file = file
        paint_list = dic_stt[stt][file]
        image = input_image + '/' + file
        img_base64 = color_yellow(image, paint_list, results[file], text_change_org)
        return img_base64

def input_processing(input_file):
##    input: đường dẫn đến file cần xử lý
##    output: file đoc/docx, pdf, folder chứa images
##    text đọc qua pytesseract, ảnh dạng truyền trực tuyến
    input_pdf, output_file = input_file_processing(input_file)
    input_image = pdf_to_img(input_pdf)
    results , img_org_base64 = ocr_folder_image(input_image)
    return results , input_image , output_file , img_org_base64
