# -*- coding: utf-8 -*-

from numpy import *
import matplotlib.pyplot as plt
import random

# In[27]:

def read_file(file):
    for line in file:
        yield line.strip()

# load data 返回数据集的点坐标
def loadDataFromFile(fileName):
    location = []
    print('Reading input coordinate matrix')
    fr = open(fileName)
    file = read_file(fr)
    lineArr = []
    curLine = []
    for line in file:
        curLine = line.split(',')
        for data in curLine:
            lineArr.append(float(data))
#        lineArr.pop()
        location.append(lineArr)
        lineArr = []
                
    location = array(location)
    fr.close()
    
    return location

### 点坐标系距离计算函数
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))   

### 经纬度距离计算函数
def distSLC(vecA, vecB):#Spherical Law of Cosines
    lon1, lat1, lon2, lat2 = map(radians, [vecA[0], vecA[1], vecB[0], vecB[1]])  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2  
    c = 2 * arcsin(sqrt(a))   
    r = 6378.1 # 地球平均半径，单位为公里  
 
    return c * r * 1000 #pi is imported with numpy

### Caculate distance 返回数据集的距离矩阵、阈值dc
### location : dataset ; percent : threshold
def getDist(location, percent = 0.02, distComp = distEclud):  
    length = len(location)
    dist = zeros((length, length))  
    print('Computing input distance matrix')
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
    dc = sortedll[position - 1] #计算阈值dc
    print('average percentage of neighbours (hard coded)：', percent)    
    return dist,dc

### load data 返回数据集的点坐标
def getDistFromFile(fileName, percent=0.02):
    numDim = len(open(fileName).readline().strip().split(' '))     #get column
    location = []
    
    print('Reading input distance matrix')
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(' ')
        lineArr = []
        for i in range(numDim):
            lineArr.append(float(curLine[i]))
        location.append(lineArr)
    fr.close()
    set = array(location)
    nd = max(set[:,1])
    nl = max(set[:,0])
    if(nd < nl):
          nd = nl;        #确保 dn 取为第一二列最大值中的较大者，并将其作为数据点总数
    dist = zeros((nd, nd))
    n = shape(set)[0]
    for i in range(n):
        dist[set[i,0] - 1,set[i,1] - 1] = set[i,2]
        dist[set[i,1] - 1,set[i,0] - 1] = set[i,2]
    
    position = int(n * percent)
    sortedSet = sort(set[:,2])
    dc = sortedSet[position - 1] #计算阈值dc
    print('average percentage of neighbours (hard coded)：', percent)
    return dist,dc


# In[ ]:




# In[28]:

### 求点的局部密度(local density)
def calDensity(dist, dc):
    length = shape(dist)[0]
    rho = zeros(length)
    print('Computing Rho with gaussian kernel of radius：',dc)
#    print('Computing Rho with cut-off kernel of radius：',dc)
    for i in range(length - 1):
        for j in range(length - i - 1):
            jj = j + i + 1
            ## Gaussian kernel
            rho[i] = rho[i] + exp(-(dist[i][jj]/dc) * (dist[i][jj]/dc))
            rho[jj] = rho[jj] + exp(-(dist[i][jj]/dc) * (dist[i][jj]/dc))

            ## "cut-off" kernel
#            if dist[i][jj] < dc:
#                rho[i] = rho[i] + 1
#                rho[jj] = rho[jj] + 1
    return rho

### 求比点的局部密度大的点到该点的最小距离即 delta 距离
def calDelta(dist, rho):
    length = len(rho)
    delta = zeros(length)
    nneigh = zeros(length)
    ## 将 rho 按降序排列，ordrho 原rho的索引  
    ordrho = argsort(-array(rho))     

    ## 生成 delta 和 nneigh 数组  
    for i in range(1,length):  
        delta[ordrho[i]] = inf  
        for j in range(0,i):  
            if dist[ordrho[i],ordrho[j]] < delta[ordrho[i]]:
                delta[ordrho[i]] = dist[ordrho[i],ordrho[j]]  
                nneigh[ordrho[i]] = ordrho[j]    
    
    ## 生成 rho 值最大数据点的 delta 值  
#    delta[ordrho[0]] = max(dist[ordrho[0],:])
    delta[ordrho[0]] = max(delta)
    nneigh[ordrho[0]] = 0
    return delta,nneigh

### 确定聚类类别
def getMark(rho, delta, nneigh, rhomin, deltamin):
#    rhomin = rate1 * (max(rho) - min(rho)) + min(rho)
#    deltamin = rate2 * (max(delta) - min(delta)) + min(delta)
    ordrho = argsort(-array(rho))
    length = len(rho)
    mark = ones(length, dtype = int) * (-1)
    imark = []    #逆映射,统计每个中心点分别为哪个数据点
    num = 0
    print(min(rho))
    print(min(delta))
    ## 统计聚类中心的个数 
    for i in range(length): #items:
        if rho[i] > rhomin and delta[i] > deltamin:
            mark[i] = num
            imark.append(i)
            num = num + 1
    print('NUMBER OF CLUSTERS：', num)
    ## 将其他数据点归类 (assignation)  
    print('Performing assignation')
    for i in range(length):  
        if mark[ordrho[i]] == -1:
            mark[ordrho[i]] = mark[nneigh[ordrho[i]]]  

    return num,mark,imark


# In[29]:

### 处理噪音
def getHalo(mark, nclust, imark, dist, dc):
    length = len(mark)
    bord_rho = zeros(nclust) 
    halo = mark.copy()
  
    ## 获取每一个 cluster 中平均密度的一个界 bord_rho  
    for i in range(length): 
        for j in range(i+1,length):  
            if mark[i] != mark [j] and dist[i,j] <= dc: 
                rho_aver = (rho[i] + rho[j]) / 2.0   #取 i,j 两点的平均局部密度  
                if rho_aver > bord_rho[mark[i]]:   
                    bord_rho[mark[i]] = rho_aver  
                if rho_aver > bord_rho[mark[j]]:
                    bord_rho[mark[j]] = rho_aver

    ## 计算离群点 outlier
    for i in range(length):
        if rho[i] < bord_rho[mark[i]]:
            halo[i] = -1 
    ## 逐一处理每个 cluster  
    for i in range(nclust):
        na = 0    #用于累计当前 cluster 中数据点的个数  
        nc = 0    #用于累计当前 cluster 中核心数据点的个数  
        for j in range(length):
            if mark[j] == i:   
                na = na + 1  
            if halo[j] == i:   
                nc = nc + 1 
        cord = 'CLUSTER： ' + str(i + 1) + ' CENTER： ' + str(imark[i])
        cord = cord + ' ELEMENTS： ' + str(na) + ' CORE： ' + str(nc) + ' HALO： ' + str(na - nc)
        print(cord)
    return halo


# In[30]:

def draw(rho, delta, mark):    
    length = len(rho)
    ## 绘制决策图
    plt.figure(1)
    plt.plot(rho, delta, 'o')
    plt.title('Decision Graph')
    plt.xlabel('rho'), plt.ylabel('delta')
    plt.draw()


    ## 将 rho 按降序排列，ordrho 原rho的索引
    plt.figure(2)
    gama = rho * delta
    ordgama = argsort(-array(gama)) 
    plt.xlim(-0.06 * length, length)
    plt.plot(range(length), gama[ordgama], 'o')
    plt.title('Gama Graph')
    plt.xlabel('n'), plt.ylabel('gama')
    plt.draw()
    
    
    R = array(range(256))
    random.shuffle(R)
    R = R/255.0
    G = array(range(256))
    random.shuffle(G)
    G = G/255.0
    B = array(range(256))
    random.shuffle(B)
    B = B/255.0
    colors = []
    for i in range(256):
        colors.append((R[i], G[i], B[i]))

    ## 绘制聚类结果
    plt.figure(3)
    for i in range(len(rho)):
        index = mark[i]
        if index == -1:
            plt.plot(dataSet[i][0], dataSet[i][1], color = (0,0,0), marker = 'o')
        else:
            plt.plot(dataSet[i][0], dataSet[i][1], color = colors[index % 255], marker = 'o')
    plt.title('Cluster Result')
    plt.xlabel('x'), plt.ylabel('y')
    plt.show()    


# In[31]:

#加载数据
dataSet = loadDataFromFile('data/beijingcmi.txt')
#print(dataSet)
#计算或加载数据集的距离矩阵、阈值dc
dist,dc = getDist(dataSet, 0.02)
#dist,dc = getDistFromFile('data/clusting/Compound_dist.txt')
#print(dist, dc)

#求点的局部密度(local density)
rho = calDensity(dist, dc)
#print('当前数据集所有点的局部密度为：',rho)

#求比点的局部密度大的点到该点的最小距离即 delta 距离
delta, nneigh = calDelta(dist, rho)

#设置参数
#rhomin = 4.5565; deltamin = 4.0873    #Compound   nclust = 5
#rhomin = 5.0403; deltamin = 5.9127    #Compound   nclust = 4
rhomin = 50; deltamin = 0.8    #Spiral
#rhomin = 4.5323; deltamin = 6.5873    #Flame
#rhomin = 39.1935; deltamin = 1.4286    #D31

#确定聚类类别，将所有数据点归类
num, mark,imark = getMark(rho, delta, nneigh, rhomin, deltamin)
#print('当前数据集聚类标签为：', mark)

# 处理噪音
halo = getHalo(mark, num, imark, dist, dc)

#绘制结果
draw(rho, delta, halo)


# In[ ]:



