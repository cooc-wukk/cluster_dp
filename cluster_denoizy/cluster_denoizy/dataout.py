import xlwt
import numpy as np
import xlsxwriter

def text_create(name, dataSet, leb):
    desktop_path = "C:\\Users\\lenovo\\Desktop\\"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    ifile = open(full_path, 'w')
    strtile = str("id") + ',' + str("label")+ '\n'
    ifile.write(strtile)
    for i in range(len(dataSet)):
        strs =  str(int(i))+ ',' + str(int(leb[i])) + '\n'
        ifile.write(strs)
    ifile.close()
    print("output over")


#  将数据写入新文件
def data_write1(leb, name):
    desktop_path = "C:\\Users\\lenovo\\Desktop\\"  # 新创建的excel文件的存放路径
    full_path = desktop_path + name + '.xls'
    f = xlwt.Workbook(full_path)
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'id', u'label']#初始化表头
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    id = []
    for j in range(len(leb)):
        id.append(j)
    id = np.array(id)
    leb = np.array(leb)
    resultFix = np.transpose(np.vstack((id, leb)))
    for n in range(len(leb)):
        for k in range(2):
            a = int(resultFix[n][k])
            sheet1.write(n+1, k, a)
            # sheet1.write(j + 1, 2, col3_data[j].decode('utf-8'))
    #print("output over")
    f.save(full_path)

def data_write(leb, name):
    desktop_path = "C:\\Users\\lenovo\\Desktop\\"  # 新创建的excel文件的存放路径
    full_path = desktop_path + name + '.xlsx'
    f = xlsxwriter.Workbook(full_path)
    # f = xlwt.Workbook(full_path)
    worksheet = f.add_worksheet()
    # sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'id', u'label']  # 初始化表头
    for i in range(0, len(row0)):
        worksheet.write(0, i, row0[i])
    id = []
    for j in range(len(leb)):
        id.append(j)
    id = np.array(id)
    leb = np.array(leb)
    resultFix = np.transpose(np.vstack((id, leb)))
    for n in range(len(leb)):
        for k in range(2):
            a = int(resultFix[n][k])
            worksheet.write(n + 1, k, a)
            # sheet1.write(j + 1, 2, col3_data[j].decode('utf-8'))
    # print("output over")
    f.close()



