def replace_string(filename, key, value, numberList):
##    hàm duyệt từng đoạn trong file
##    split đoạn văn và key thành list
##    kiểm tra xem key có xuất hiện trong đoạn không
##    đếm số lần xuất hiện của key, nếu thứ tự nằm trong numberList thì thay đổi key
##    thay đổi: xóa các từ khác, giữ lại từ đầu tiên của key, thay bằng value
##    chuyển đoạn văn từ list về, lưu file lại
##    
##    input: tên file, từ muốn đổi, từ để đổi, danh sách vị trí đổi
##    output: file word đã được thay từ ở những vị trí chỉ định
    key_split = key.split() # split key
    len_key = len(key_split)
    countKey = 0
    doc = Document(filename)
    for posPara in range(len(doc.paragraphs)):
        p = doc.paragraphs[posPara] # duyệt đoạn
        print(p.text)
        line_split = p.text.split() # split đoạn
        indexList = [] # lưu lại index của key để thay đổi
        if key in p.text:
            for i in range(len(line_split)):
                if key_split[0] == line_split[i]: # nếu từ đầu trong key xuất hiện
                    count = 0 #saveIndex = i
                    while count < len_key:
                        if key_split[count] == line_split[i+count]:
                            count+=1 # đếm xem các từ trong key xuất hiện đủ chưa
                        else:
                            break
                    if count == len_key: # nếu đủ
                        countKey += 1
                        if countKey in numberList:
                            indexList.append(i) #indexList.append(saveIndex)
        for index in indexList: # bắt đầu thay đổi ở các vị trí cần thiết
            count = 1
            while count < len_key:
                line_split[index+count] = u"" #thêm u ở phía trước để xử lý ký tự tiếng việt nhá
                count+=1 
            line_split[index] = value
        p.text = u" ".join(line_split)
    print("="*50)
    for posPara in range(len(doc.paragraphs)):
        p = doc.paragraphs[posPara]
        print(p.text)
    doc.save('dest1.docx') # lưu lại thôi

numberList = [1,3]
#replace_string ('/content/mot.docx',u'Công Ty Cổ Phần Thanh Toán', u'Ban giám đốc',numberList)
