from class_gethalo import *
import numpy as np
### hh噪音归类
def setHalo(dataSet, halo):
    X = []
    Y = []
    lb = []
    for i in range(len(dataSet)):
        X.append(float(dataSet[i][0]))
        Y.append(float(dataSet[i][1]))
        lb.append(int(halo[i]))
    Ass = []
    dismin = []
    labid = []
    mindislb = []
    for i in range(len(X)):
        if lb[i] == -1:
            labid.append(i)#记录噪声点的标号
            Assenst = []  # 距离
            AssenstId = []
            for j in range(len(X)):
                if lb[j] != -1:
                    ass = (X[i] - X[j]) * (X[i] - X[j]) + (Y[i] - Y[j]) * (Y[i] - Y[j])
                    Assenst.append(ass)
                    Ass = min(Assenst)#每一个噪声点都对应一个最近距离
                    AssenstId.append(lb[j])#非噪声点的标签复制给assentId
                    weizhi = Assenst.index(min(Assenst))
                    minlb = AssenstId[weizhi]#离此噪声点最近的点的标签是什么

    dismin.append(Ass)#所有噪声点对应的最近距离
    iddismin = dismin.index(min(dismin))
    mindislb.append(minlb)  # 所有噪声点最临近的标签
    lab = mindislb[iddismin]#
    for i in range(len(dismin)):


    min(dismin)
    weizhi = Assenst.index(min(Assenst))
    lb[i] = AssenstId[weizhi]
    lable = np.array(lb)
    return lable