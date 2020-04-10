from numpy import *
import matplotlib.pyplot as plt

import numpy as np


# In[27]:
def read_file(file):
    for line in file:
        yield line.strip()


# load data
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
    location = locationquan[:, 0:2]
    real = np.array((locationquan[:, 2]), dtype=int)
    fr.close()
    return location, real

    return location


#
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


#
def distSLC(vecA, vecB):  # Spherical Law of Cosines
    lon1, lat1, lon2, lat2 = map(radians, [vecA[0], vecA[1], vecB[0], vecB[1]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * arcsin(sqrt(a))
    r = 6378.1

    return c * r * 1000  # pi is imported with numpy


# Caculate distance
# location : dataset ; percent : threshold
def getDist(location, percent=0.02, distComp=distEclud):
    length = len(location)
    dist = zeros((length, length))
    print('Computing input distan ce matrix')
    ldist = []
    begin = 0
    while begin < length - 1:
        end = begin + 1
        while end < length:
            dd = distComp(location[begin], location[end])
            dist[begin][end] = dd
            dist[end][begin] = dd
            ldist.append(dd)
            end = end + 1
        begin = begin + 1
    ldist = array(ldist)
    position = int(len(ldist) * percent)
    sortedll = sort(ldist)
    dc = sortedll[position - 1]
    print('average percentage of neighbours (hard coded)', percent)
    return dist, dc



# (local density)
def calDensity(dist, dc):
    length = shape(dist)[0]
    rho = zeros(length)
    print('Computing Rho with gaussian kernel of radius', dc)
    #    print('Computing Rho with cut-off kernel of radius',dc)
    for i in range(length - 1):
        for j in range(length - i - 1):
            jj = j + i + 1
            ## Gaussian kernel
            rho[i] = rho[i] + exp(-(dist[i][jj] / dc) * (dist[i][jj] / dc))
            rho[jj] = rho[jj] + exp(-(dist[i][jj] / dc) * (dist[i][jj] / dc))

            ## "cut-off" kernel
    #            if dist[i][jj] < dc:
    #                rho[i] = rho[i] + 1
    #                rho[jj] = rho[jj] + 1
    return rho


# 
def calDelta(dist, rho):
    length = len(rho)
    delta = zeros(length)
    nneigh = zeros(length)
    ## 
    ordrho = argsort(-array(rho))

    ## delta  nneigh
    for i in range(1, length):
        delta[ordrho[i]] = inf
        for j in range(0, i):
            if dist[ordrho[i], ordrho[j]] < delta[ordrho[i]]:
                delta[ordrho[i]] = dist[ordrho[i], ordrho[j]]
                nneigh[ordrho[i]] = ordrho[j]

    #    delta[ordrho[0]] = max(dist[ordrho[0],:])
    delta[ordrho[0]] = max(delta)
    nneigh[ordrho[0]] = 0
    return delta, nneigh


#
def getMark(rho, delta, nneigh, rhomin, deltamin):
    #    rhomin = rate1 * (max(rho) - min(rho)) + min(rho)
    #    deltamin = rate2 * (max(delta) - min(delta)) + min(delta)
    ordrho = argsort(-array(rho))
    length = len(rho)
    mark = ones(length, dtype=int) * (-1)
    imark = []  #
    num = 0
    print(max(rho))
    print(max(delta))
    ##
    for i in range(length):  # items:
        if rho[i] > rhomin and delta[i] > deltamin:
            mark[i] = num
            imark.append(i)
            num = num + 1
    print('NUMBER OF CLUSTERS', num)
    ## (assignation)
    print('Performing assignation')
    for i in range(length):
        if mark[ordrho[i]] == -1:
            mark[ordrho[i]] = mark[int(nneigh[int(ordrho[i])])]

    return num, mark, imark


# In[29]:

#
def getHalo(mark, nclust, imark, dist, dc):
    length = len(mark)
    bord_rho = zeros(nclust)
    halo = mark.copy()

    ## cluster bord_rho
    for i in range(length):
        for j in range(i + 1, length):
            if mark[i] != mark[j] and dist[i, j] <= dc:
                rho_aver = (rho[i] + rho[j]) / 2.0
                if rho_aver > bord_rho[mark[i]]:
                    bord_rho[mark[i]] = rho_aver
                if rho_aver > bord_rho[mark[j]]:
                    bord_rho[mark[j]] = rho_aver

    ##outlier
    for i in range(length):
        if rho[i] < bord_rho[mark[i]]:
            halo[i] = -1
            ## cluster
    for i in range(nclust):
        na = 0  # cluster
        nc = 0  # cluster
        for j in range(length):
            if mark[j] == i:
                na = na + 1
            if halo[j] == i:
                nc = nc + 1
        cord = 'CLUSTER ' + str(i + 1) + ' CENTER ' + str(imark[i])
        cord = cord + ' ELEMENTS ' + str(na) + ' CORE ' + str(nc) + ' HALO ' + str(na - nc)
        print(cord)
    return halo

def setHalo(dataSet, halo):
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
            Assenst = []
            AssenstId = []
            for j in range(len(X)):
                if leibie[j] != -1:
                    ass = (X[i] - X[j]) * (X[i] - X[j]) + (Y[i] - Y[j]) * (Y[i] - Y[j])
                    Assenst.append(ass)
                    AssenstId.append(leibie[j])
            weizhi = Assenst.index(min(Assenst))
            result[i] = AssenstId[weizhi]
    leibie1 = np.array(result)
    return leibie1
def arrLeb(x, y, label):
    r_mean = []
    xy_result = np.transpose(np.vstack((x, y, label)))
    labels = np.unique(label)
    for label in labels:
        equal2label = xy_result[xy_result[:, 2] == label]
        mean = np.mean(equal2label, axis=0)
        r_mean.append(mean[0] * mean[1])
    index = r_mean.index(max(r_mean))
    xy_result = np.where(xy_result[:, 2] == labels[index], 0, 1)
    return xy_result
# In[30]:

def draw(rho, delta, mark):


    R = array(range(256))
    R_0 = R[200]
    R_0 = R_0 / 255.0
    R_1 = R[131]
    R_1 = R_1 / 255.0
    R_2 = R[32]
    R_2 = R_2 / 255.0
    R_3 = R[236]
    R_3 = R_3 / 255.0

    G = array(range(256))
    G_0 = G[46]
    G_0 = G_0 / 255.0
    G_1 = G[199]
    G_1 = G_1 / 255.0
    G_2 = G[90]
    G_2 = G_2 / 255.0
    G_3 = G[135]
    G_3 = G_3 / 255.0

    B = array(range(256))
    B_0 = B[49]
    B_0 = B_0 / 255.0
    B_1 = B[93]
    B_1 = B_1 / 255.0
    B_2 = B[167]
    B_2 = B_2 / 255.0
    B_3 = B[14]
    B_3 = B_3 / 255.0

    colors = []

    colors.append((R_0, G_0, B_0))
    colors.append((R_2, G_2, B_2))
    colors.append((R_1, G_1, B_1))
    colors.append((R_3, G_3, B_3))

    plt.figure(3)
    for i in range(len(rho)):
        index = mark[i]
        if index == -1:
            plt.plot(dataSet[i][0], dataSet[i][1], color=(0, 0, 0), marker='o', markersize=4)
        else:
            plt.plot(dataSet[i][0], dataSet[i][1], color=colors[index], marker='o', markersize=4)
    plt.title('Cluster Result')
    plt.xlabel('x'), plt.ylabel('y')
    plt.show()


# In[31]:

dataSet, real = loadDataFromFile('data3/wh.txt')
print(dataSet)

dist, dc = getDist(dataSet, 0.02)

rho = calDensity(dist, dc)

delta, nneigh = calDelta(dist, rho)

rhomin = 20
deltamin = 0.2


#
num, mark, imark = getMark(rho, delta, nneigh, rhomin, deltamin)
print('the type of this dataset is', num)

#
halo = getHalo(mark, num, imark, dist, dc)
leb_hh = setHalo(dataSet, halo)
newleb = arrLeb(dataSet[:,0], dataSet[:,1], leb_hh)

draw(rho, delta, halo)
# draw(rho, delta, mark)





