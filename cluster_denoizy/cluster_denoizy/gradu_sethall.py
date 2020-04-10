from class_gethalo import *
import numpy as np
### hh噪音归类
def Gradu_setHalo(dataSet, halo):
    X = []
    Y = []
    lb = []
    for i in range(len(dataSet)):
        X.append(float(dataSet[i][0]))
        Y.append(float(dataSet[i][1]))
        lb.append(int(halo[i]))

    for i in range(len(X)):
        if lb[i] == -1:
            Assenst = []  # 距离
            AssenstId = []
            for j in range(len(X)):
                if lb[j] != -1:
                    ass = (X[i] - X[j]) * (X[i] - X[j]) + (Y[i] - Y[j]) * (Y[i] - Y[j])
                    Assenst.append(ass)
                    dis_sot = sorted(Assenst)
                    AssenstId.append(lb[j])
            weizhi = Assenst.index(min(Assenst))
            lb[i] = AssenstId[weizhi]
    lable = np.array(lb)
    return lable