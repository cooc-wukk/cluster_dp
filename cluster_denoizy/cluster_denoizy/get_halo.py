from numpy import *

def getHalo(mark, nclust, imark, dist, dc, rho):
    length = len(mark)
    bord_rho = zeros(nclust)
    halo = mark.copy()
    ## 获取每一个 cluster 中平均密度的一个界 bord_rho
    for i in range(length):
        for j in range(i + 1, length):
            if mark[i] != mark[j] and dist[i, j] <= dc:
                rho_aver = (rho[i] + rho[j]) / 2.0  # 取 i,j 两点的平均局部密度
                if rho_aver > bord_rho[mark[i]]:
                    bord_rho[mark[i]] = rho_aver
                if rho_aver > bord_rho[mark[j]]:
                    bord_rho[mark[j]] = rho_aver

    ## 计算离群点 outlier
    # for i in range(length):
    #     if mark[i] != 1:
    #         if rho[i] < bord_rho[mark[i]]:
    #             halo[i] = -1
    for i in range(length):
            if rho[i] < bord_rho[mark[i]]:
                halo[i] = -1
            # 逐一处理每个 cluster
    for i in range(nclust):
        na = 0  # 用于累计当前 cluster 中数据点的个数
        nc = 0  # 用于累计当前 cluster 中核心数据点的个数
        for j in range(length):
            if mark[j] == i:
                na = na + 1
            if halo[j] == i:
                nc = nc + 1
        cord = 'CLUSTER： ' + str(i + 1) + ' CENTER： ' + str(imark[i])
        cord = cord + ' ELEMENTS： ' + str(na) + ' CORE： ' + str(nc) + ' HALO： ' + str(na - nc)
        print(cord)
    return halo