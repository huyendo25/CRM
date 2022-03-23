from findColorReplace import *
from docxPdfImage import *
import shutil

def deleteFileFolder(input_file_name):
    file = input_file_name+'.pdf'
    if os.path.exists(file):
        os.remove(file)
    folder_path = input_file_name+'_img'
    #print(folder_path)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def start(input_file):
##    Bước đầu tiên
##    Đọc file word, chuyển pdf, chuyển sang ảnh
##    chuyển ảnh thành data truyền mạng
##
##    input: file word đầu vào
##    output: ảnh base64 để hiển thị

    output_file,img_org_base64 = input_processing(input_file)
    # Xóa file pdf,folder chứa ảnh khi đã chuyển qua base64 xong
    input_file_name = os.path.splitext(input_file)[0]
    deleteFileFolder(input_file_name)
    return img_org_base64

def stage2(input_file,key):
##    Bước thứ 2
##    Tìm kiếm và tô vàng key, lưu lại file word
##    Đọc file word, chuyển pdf, chuyển sang ảnh
##    chuyển ảnh thành data truyền mạng
##
##    input: file word đầu vào, key
##    output: ảnh base64 để hiển thị
    input_file_name, input_file_end = os.path.splitext(input_file)
    input_file_name = input_file_name+'_colored'
    output_file = input_file_name+input_file_end
    countKey = findColor(input_file,key,output_file)
    output_file,img_org_base64 = input_processing(output_file)
    # Xóa file pdf,folder chứa ảnh khi đã chuyển qua base64 xong
    deleteFileFolder(input_file_name)
    file = input_file_name+'.docx'
    if os.path.exists(file):
        os.remove(file)
    return img_org_base64, countKey
    
def stage3(input_file,key,value,numberList):
##    Bước thứ 3
##    Tìm kiếm và thay thế key bằng value ở những vị trí trong numberList
##    lưu lại file word
##    Đọc file word, chuyển pdf, chuyển sang ảnh
##    chuyển ảnh thành data truyền mạng
##
##    input: file word đầu vào, key, value, những vị trí cần thay thế
##    output: ảnh base64 để hiển thị
    input_file_name, input_file_end = os.path.splitext(input_file)
    input_file_name = input_file_name+'_replaced'
    output_file = input_file_name+input_file_end
    replace(input_file,key,value,numberList,output_file)
    output_file,img_org_base64 = input_processing(output_file)
    # Xóa file pdf,folder chứa ảnh khi đã chuyển qua base64 xong
    deleteFileFolder(input_file_name)
    return img_org_base64,output_file
    
input_file = 'output/mot.docx'
input_file = os.path.abspath(input_file)
#file = os.getcwd() + "/" + input_file
'''key = u'công ty cổ phần thanh toán hưng hà'
value = u'Công Ty Cổ Phần Thanh Toán Bảo Thịnh ABC'
numberList=[1,3,6,8]
start(input_file)
stage2(input_file,key)
stage3(input_file,key,value,numberList)'''
