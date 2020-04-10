from class_gethalo import *
import numpy as np
def setHaloRemo(dataSet, halo):
    X = []
    Y = []
    leibie = []
    result = []

    for i in range(len(dataSet)):
        X.append(float(dataSet[i][0]))
        Y.append(float(dataSet[i][1]))
        leibie.append(int(halo[i]))
        result.append(int(halo[i]))
    for i in range(len(X)):
        if leibie[i] == -1:
            Assenst = []  # 距离
            AssenstId = []
            for j in range(len(X)):
                if leibie[j] != -1:
                    ass = (X[i] - X[j]) * (X[i] - X[j]) + (Y[i] - Y[j]) * (Y[i] - Y[j])
                    Assenst.append(ass)
                    AssenstId.append(leibie[j])
            location_id = Assenst.index(min(Assenst))
            result[i] = AssenstId[location_id ]
    label = np.array(result)
    return label