from wand.image import Image as Img
from wand.color import Color
from docx import Document
from docx2pdf import convert
import base64
import cv2
import os
import time

def input_file_processing(input_file):
##    input: file docx cần xử lý
##    output: file pdf/doc/docx, lưu trong folder chứa input_file
##    cần chuyển docx sang pdf
    input_file_name, input_file_end = os.path.splitext(input_file)
    
    # convert trên window
    convert(input_file)
    
    # convert trên linux
##    LIBRE_OFFICE = r"/usr/bin/lowriter"
##    from subprocess import Popen
##    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
##               out_folder, input_file])
    # print([LIBRE_OFFICE, '--convert-to', 'pdf', input_file])
    #p.communicate()
    
    input_pdf = input_file_name + '.pdf'
    #output_file = input_file_name + '_output.docx'
    #doc = Document(input_file)
    #doc.save(output_file) #lưu lại output_file
    return input_pdf, input_file
    
def pdf_to_img(input_file):
##    đổi từ PDF sang Image
##    input: đường dẫn
##    output: save ảnh .png
    time_1 = time.time()
    folder = input_file.split('.pd')[0] + '_img' # tên folder chứa ảnh
    if not os.path.exists(folder):#nếu chưa có folder thì tạo folder
        os.makedirs(folder)
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

##from pdf2image import convert_from_path
##def pdf_to_img(input_pdf):
##    from PyPDF2 import PdfFileReader
##    pdf = PdfFileReader(open(input_pdf,'rb'))
##    number_page = pdf.getNumPages()
##    folder = input_pdf.split('.pd')[0] + '_img'
##    if not os.path.exists(folder):
##        os.makedirs(folder)
##    pages = convert_from_path(input_pdf, 200)
##    counter = 0
##    for page in pages:
##        myfile = folder+'/'+str(counter)
##        page.save(myfile, 'PNG')
##        counter = counter+1
##        if counter > number_page:
##            break
##    return folder
        
def imageToBase64(image):
##    imencode mã hóa định dạng img thành data truyền trực tuyến và gán nó vào bộ nhớ đệm
##    nén định dạng dữ liệu hình ảnh để tạo điều kiện cho việc truyền mạng
##    b64encode mã hóa hình ảnh thành nhị phân hiển thị bằng ASCII
##    decode chuyển dạng mã hóa về string
    image = cv2.imread(image)
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    image_data = jpg_as_text.decode("utf-8")
    image_data = str(image_data)
    #print(image_data)
    image_data = 'data:image/png;base64,' + image_data
    return image_data

def input_processing(input_file):
##    input: đường dẫn đến file docx cần xử lý
##    output: file đoc/docx, pdf, folder chứa images
##    docx - pdf - folder ảnh - chuyển ảnh thành data truyền mạng
    input_pdf, output_file = input_file_processing(input_file)
    input_image = pdf_to_img(input_pdf)
    img_org_base64 = {}
    files = os.listdir(input_image)
    for file in files:
        image = input_image + '/' + file
        img_org_base64[file] = imageToBase64(image)
    return input_image,output_file,img_org_base64
