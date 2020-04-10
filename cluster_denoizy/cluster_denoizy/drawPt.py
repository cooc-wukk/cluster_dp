import matplotlib.pyplot as plt
from class_gethalo import *

#绘图
def draw(rho, delta, mark, dataSet):
    length = len(rho)
    # 决策图
    plt.figure(1)
    plt.plot(rho, delta, 'o')
    plt.title('Decision Graph')
    plt.xlabel('rho'), plt.ylabel('delta')
    plt.draw()
    # gamma图
    # 将 rho 按降序排列，ordrho 原rho的索引
    plt.figure(2)
    gama = rho * delta
    ordgama = argsort(-array(gama))
    plt.xlim(-0.06 * length, length)
    plt.plot(range(length), gama[ordgama], 'o')
    plt.title('Gama Graph')
    plt.xlabel('n'), plt.ylabel('gama')
    plt.draw()

    R = array(range(256))
    R_0 = R[200]
    R_0 = R_0 / 255.0
    R_1 = R[131]
    R_1 = R_1 / 255.0
    R_2 = R[32]
    R_2 = R_2 / 255.0
    R_3 = R[236]
    R_3 = R_3 / 255.0
    R_4 = R[58]
    R_4 = R_4 / 255.0

    G = array(range(256))
    G_0 = G[46]
    G_0 = G_0 / 255.0
    G_1 = G[199]
    G_1 = G_1 / 255.0
    G_2 = G[90]
    G_2 = G_2 / 255.0
    G_3 = G[135]
    G_3 = G_3 / 255.0
    G_4 = G[40]
    G_4 = G_4 / 255.0

    B = array(range(256))
    B_0 = B[49]
    B_0 = B_0 / 255.0
    B_1 = B[93]
    B_1 = B_1 / 255.0
    B_2 = B[167]
    B_2 = B_2 / 255.0
    B_3 = B[14]
    B_3 = B_3 / 255.0
    B_4 = B[133]
    B_4 = B_4 / 255.0

    colors = []

    colors.append((R_0, G_0, B_0))
    colors.append((R_2, G_2, B_2))
    colors.append((R_1, G_1, B_1))
    colors.append((R_3, G_3, B_3))
    colors.append((R_4, G_4, B_4))

    #散点图
    plt.figure(3)
    for i in range(len(rho)):
        index = mark[i]
        if index == -1:
            plt.plot(dataSet[i][0], dataSet[i][1], color = (0,0,0), marker = 'o', markersize=4)
        else:
            plt.plot(dataSet[i][0], dataSet[i][1], color=colors[index], marker='o', markersize=4)
    plt.title('Cluster Result')
    plt.xlabel('x'), plt.ylabel('y')
    plt.show()

    # #异常点图
    # plt.figure(4)
    # for i in range(len(dataSet)):
    #     index = mark[i]
    #     if i == 1260:
    #         plt.plot(dataSet[i][0], dataSet[i][1], color = (0,0,0), marker = '*', markersize=6)
    #
    #     else:
    #         plt.plot(dataSet[i][0], dataSet[i][1], color=colors[index], marker='o', markersize=4)
    # plt.title('异常点')
    # plt.xlabel('x'), plt.ylabel('y')
    # plt.show()