from docxPdfImage import *

def color_string(key,countKey,p1,p):
##    tô vàng key
##    input: key, số thứ tự key, đoạn văn chứa key, đoạn mới chứa key được tô vàng
##    output: đoạn văn đã được tô vàng, số thứ tự key
    substrings = p1.split(key) # split đoạn
    for substring in substrings[:-1]:
        countKey += 1
        p.add_run(substring)
        font = p.add_run(key).font.highlight_color = WD_COLOR_INDEX.YELLOW # tô vàng key
        count = str(countKey)
        font = p.add_run(count).font.highlight_color = WD_COLOR_INDEX.RED # tô đỏ số thứ tự của key
    p.add_run(substrings[-1])
    return countKey
    
def findColor(filename,key,newName):
##    tìm và tô vàng key
##    input: file cần xử ký, key cần tìm và tô vàng
##    output: file đã tô vàng và đánh thứ tự cho key
    countKey = 0 # khởi tạo số thứ tự key
    doc = Document(filename)
    for posPara in range(len(doc.paragraphs)): # duyệt đoạn
        p = doc.paragraphs[posPara] 
        p1 = p.text
        match = re.search(key,p1,re.IGNORECASE)
        if match: #so khớp không phân biệt hoa thường
            p.text = ""
            countKey=color_string(match.group(),countKey,p1,p)

    for table in doc.tables: #duyệt bảng
        for row in table.rows:
            for p in row.cells:
                p1 = p.text
                match = re.search(key,p1,re.IGNORECASE)
                if match: #so khớp không phân biệt hoa thường
                    p.text = ""
                    p = p.add_paragraph()
                    countKey=color_string(match.group(),countKey,p1,p)
    doc.save(newName)
    return countKey

def replace_string(key,value,numberList,countKey,p):
##    split đoạn văn và key thành list
##    kiểm tra xem key có xuất hiện trong đoạn không
##    đếm số lần xuất hiện của key, nếu thứ tự nằm trong numberList thì thay đổi key
##    thay đổi: xóa các từ khác, giữ lại từ đầu tiên của key, thay bằng value
##    chuyển đoạn văn từ list về đoạn
##    
##    input: key, từ để đổi, danh sách vị trí đổi, số thứ tự key, đoạn văn chứa key
##    output: đoạn văn đã được đổi từ ở vị trí chỉ định, số thứ tự key
    line_split = p.text.split() # split đoạn
    key_split = key.split() # split key
    len_key = len(key_split)
    for i in range(len(line_split)):
        if re.search(key_split[0],line_split[i],re.IGNORECASE):# nếu từ đầu trong key xuất hiện
            count = 0 # đếm từ trong key
            while count < len_key:
                if re.search(key_split[count],line_split[i+count],re.IGNORECASE): ##so khớp không phân biệt hoa thường
                    count+=1 # đếm xem các từ trong key xuất hiện đủ chưa
                else:
                    break
            if count == len_key: # nếu đủ
                countKey += 1
                punctuation =""
                if re.match(r'\S', p.text): #so khớp với ký tự không phải chữ
                    punctuation = line_split[i+count-1][-1] # dấu câu
                if countKey in numberList:  # bắt đầu thay đổi ở các vị trí cần thiết
                    count_1 = 1
                    while count_1 < len_key:
                        line_split[i+count_1] = u"" #thêm u ở phía trước để xử lý ký tự tiếng việt nhá
                        count_1+=1
                    line_split[i] = value +punctuation
                p.text = u" ".join(line_split) 
    return countKey

def replace(filename,key,value,numberList,output_file):
##    hàm duyệt từng đoạn trong file
##    tìm và thay thế từ ở vị trí chỉ định
##    input: tên file, từ muốn đổi, từ để đổi, danh sách vị trí đổi
##    output: file word đã được thay từ ở những vị trí chỉ định
    countKey = 0 # khởi tạo số thứ tự key
    doc = Document(filename)
    for posPara in range(len(doc.paragraphs)): # duyệt đoạn
        p = doc.paragraphs[posPara]
        if re.search(key,p.text,re.IGNORECASE): #so khớp không phân biệt hoa thường
            countKey = replace_string(key,value,numberList,countKey,p)

    for table in doc.tables:
        for row in table.rows:
            for p in row.cells:
                if re.search(key,p.text,re.IGNORECASE): #so khớp không phân biệt hoa thường
                    countKey = replace_string(key,value,numberList,countKey,p)    
    doc.save(output_file)

#replace ('/content/mot.docx', u'công ty cổ phần thanh toán hưng hà', u'Công Ty Cổ Phần Thanh Toán Bảo Thịnh ABC')
#numberList = [1,3]
#replace_string ('/content/mot.docx',u'Công Ty Cổ Phần Thanh Toán', u'Ban giám đốc',numberList)
