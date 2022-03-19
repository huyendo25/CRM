from pdf2image import convert_from_path
from subprocess import check_output
from docx2pdf import convert
import argparse
from docx import Document
from OCR_CRM import *
from findText import *
from replaceString import *
import time
from pdf2docx import Converter
import base64
from subprocess import Popen
import time


#result: dạng dict gồm level,page_num,block_num,par_num,line_num,word_num,
#left,top,weight,height,conf,text


input_file = 'output/Bao_cao_ky_thuat_-_Phong_8.docx'
#print(input_file_processing('output/Bao_cao_ky_thuat_-_Phong_8.docx'))
input_pdf, output_file = input_file_processing(input_file)
input_image = pdf_to_img(input_pdf)
print (input_image)

##image = cv2.imread('Bao_cao_ky_thuat_-_Phong_8_img_0.png')
##imageToBase64(image)

#input_pdf, output_file = input_file_processing(input_file)

#input_processing(input_file)
#print(get_num_pages(input_file))
#number_page = get_num_pages(input_file)
#print(number_page)
#file = input_file.split('.pd')[0] + '_img'
#input_folder,file_name = input_file.split("/")

#input_image = "output/Bao_cao_ky_thuat_-_Phong_8_img"
#text_change_org = "Du an"
#results,img_org_base64 = ocr_folder_image(input_image)
#paint_dic = {}
#files = os.listdir(input_image)
#file = files[0]
##for i in range(len(files)):
##    file = files[i]
##    paint_dic[file] = findText(text_change_org, results[file])
##    if paint_dic[file] == []:
##        del paint_dic[file]
#paint_dic[file] = findText(text_change_org, results[file])
##paint_list = findText(text_change_org, results[file])
#print(results[file])
#print(paint_dic)
#print(find_paint_list(text_change_org,input_image,results))

#print (tesseract_predict('output/Bao_cao_ky_thuat_-_Phong_8_img/Bao_cao_ky_thuat_-_Phong_8_img_0.png'))
#print ('='*100)
#print (tesseract_predict('Bao_cao_ky_thuat_-_Phong_8_img_0.png'))
##image = 'output/Bao_cao_ky_thuat_-_Phong_8_img/Bao_cao_ky_thuat_-_Phong_8_img_0.png'
##
##dic_stt = {0: {'Bao_cao_ky_thuat_-_Phong_8_img_0.png': [148, 149]}, 1: {'Bao_cao_ky_thuat_-_Phong_8_img_0.png': [211, 212]}, 2: {'Bao_cao_ky_thuat_-_Phong_8_img_1.png': [45, 46]}, 3: {'Bao_cao_ky_thuat_-_Phong_8_img_1.png': [174, 175]}, 4: {'Bao_cao_ky_thuat_-_Phong_8_img_1.png': [260, 261]}, 5: {'Bao_cao_ky_thuat_-_Phong_8_img_2.png': [152, 153]}, 6: {'Bao_cao_ky_thuat_-_Phong_8_img_3.png': [163, 164]}, 7: {'Bao_cao_ky_thuat_-_Phong_8_img_3.png': [231, 232]}, 8: {'Bao_cao_ky_thuat_-_Phong_8_img_4.png': [22, 23]}, 9: {'Bao_cao_ky_thuat_-_Phong_8_img_4.png': [72, 73]}, 10: {'Bao_cao_ky_thuat_-_Phong_8_img_4.png': [113, 114]}, 11: {'Bao_cao_ky_thuat_-_Phong_8_img_4.png': [147, 148]}, 12: {'Bao_cao_ky_thuat_-_Phong_8_img_4.png': [169, 170]}}
##paint_list = dic_stt[0][file]
##img_base64 = color_yellow(image, paint_list, results[file], text_change_org)
##from PIL import Image
##from base64 import decodestring
##
##image = Image.fromstring('RGB',(width,height),decodestring(imagestr))
##image.save("foo.png")
