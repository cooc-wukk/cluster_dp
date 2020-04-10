import numpy as np
def read_file(file):
    for line in file:
        yield line.strip()

#load data 返回数据集的点坐标
def loadDataFromFile(fileName):
    locationquan = []
    print('Reading input coordinate matrix')
    fr = open(fileName)
    file = read_file(fr)
    lineArr = []
    curLine = []
    for line in file:
        curLine = line.split('	')
        for data in curLine:
            lineArr.append(float(data))
#        lineArr.pop()
        locationquan.append(lineArr)
        lineArr = []

    locationquan = np.array(locationquan)
    location = locationquan[:,0:2]
    real = np.array((locationquan[:,2]), dtype=int)
    fr.close()
    return location, real
