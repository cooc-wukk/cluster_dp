from class_gethalo import *
from numpy import *
import operator
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
###  将有标签的数据和噪声数据分开，噪声数据作为测试数据，标签数据作为训练数据
def getKnndataSet(dataSet, halo):
    trainSet = []
    testSet = []
    iId = []#记录噪声的id
    labTrain = []
    for i in range(len(dataSet)):
        if halo[i] == -1:
            testSet.append(dataSet[i])
            iId.append(i)
        else:
            trainSet.append(dataSet[i])
            trainI = halo[i]
            labTrain.append(trainI)
    return testSet, trainSet, labTrain, iId

###  调用kNN库的方法
def knnClassify0(testSet, traindataSet, trainlabels, iId, halo):
    knn = KNeighborsClassifier(n_neighbors = 1)
    knn.fit(traindataSet, trainlabels)
    iris_y_predict = knn.predict(testSet)

    leibie = []
    for i in range(len(halo)):
        leibie.append(int(halo[i]))
    for i in range(len(iId)):
        leibie[iId[i]] = iris_y_predict[i]
    return leibie

###  自定义的降噪方法
# def knnClassify0(testSet, dataSet, trainlabels, iId, halo, k):
#     inX = array(testSet)
#     arraydataset = np.array(dataSet)
#     dataSetSize = arraydataset.shape[0]
#     print("arraydataset",arraydataset)
#     # 根据欧式距离计算训练集中每个样本到测试点的距离
#     diffMat = tile(inX, (dataSetSize,1) - dataSet
#     sqDiffMat = diffMat**2
#     sqDistances = sqDiffMat.sum(axis=1)
#     distances = sqDistances**0.5
#     # 计算完所有点的距离后，对数据按照从小到大的次序排序
#     sortedDistIndicies = distances.argsort()
#     # 确定前k个距离最小的元素所在的主要分类，最后返回发生频率最高的元素类别
#     classCount={}
#     for i in range(k):
#         voteIlabel = trainlabels[sortedDistIndicies[i]]
#         classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
#     sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
#     leibie = []
#     for i in range(len(dataSet)):
#         leibie.append(int(halo[i]))
#     for i in range(len(sortedClassCount)):
#         leibie[iId[i]] = sortedClassCount[i]
#     return leibie