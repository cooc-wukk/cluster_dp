from numpy import *
# In[27]:
### 点坐标系距离计算函数
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

### Caculate distance 返回数据集的距离矩阵、阈值dc
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
### 求点的局部密度(local density)
def calDensity(dist, dc):
    length = shape(dist)[0]
    rho = zeros(length)
    print('Computing Rho with gaussian kernel of radius：', dc)
    for i in range(length - 1):
        for j in range(length - i - 1):
            jj = j + i + 1
            ## Gaussian kernel
            rho[i] = rho[i] + exp(-(dist[i][jj] / dc) * (dist[i][jj] / dc))
            rho[jj] = rho[jj] + exp(-(dist[i][jj] / dc) * (dist[i][jj] / dc))
    return rho


### 求比点的局部密度大的点到该点的最小距离即 delta 距离
def calDelta(dist, rho):
    length = len(rho)
    delta = zeros(length)
    nneigh = zeros(length)
    ## 将 rho 按降序排列，ordrho 原rho的索引
    ordrho = argsort(-array(rho))

    ## 生成 delta 和 nneigh 数组
    for i in range(1, length):
        delta[ordrho[i]] = inf
        for j in range(0, i):
            if dist[ordrho[i], ordrho[j]] < delta[ordrho[i]]:
                delta[ordrho[i]] = dist[ordrho[i], ordrho[j]]
                nneigh[ordrho[i]] = ordrho[j]

                ## 生成 rho 值最大数据点的 delta 值
    delta[ordrho[0]] = max(delta)
    nneigh[ordrho[0]] = 0
    return delta, nneigh


### 确定聚类类别
def getMark(rho, delta, nneigh, rhomin, deltamin):
    ordrho = argsort(-array(rho))
    length = len(rho)
    mark = ones(length, dtype=int) * (-1)
    imark = []  # 逆映射,统计每个中心点分别为哪个数据点
    num = 0
    ## 统计聚类中心的个数
    for i in range(length):  # items:
        if rho[i] > rhomin and delta[i] > deltamin:
            mark[i] = num
            imark.append(i)
            num = num + 1
    print('NUMBER OF CLUSTERS：', num)
    ## 将其他数据点归类 (assignation)
    print('Performing assignation')
    shu = 0
    for i in range(length):
        if mark[ordrho[i]] == -1:
            shu = shu + 1
            mark[ordrho[i]] = mark[int(nneigh[int(ordrho[i])])]
    return num, mark, imark


# In[29]:

### 处理噪音
