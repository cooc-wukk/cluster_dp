# encoding=utf-8
from matplotlib import pyplot
import matplotlib.pyplot as plt
from calAccuricy import calAcc

def draw_score(f1_score ,accuracy_score, ran):
    names = range(1, ran)
    names = [str(x) for x in list(names)]

    x = range(len(names))
    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')
    # pl.xlim(-1, 11)  # 限定横轴的范围
    # pl.ylim(-1, 110)  # 限定纵轴的范围


    plt.plot(x, f1_score, marker='o', mec='r', mfc='w', label='f1')
    plt.plot(x, accuracy_score, marker='*', ms=10, label='accuracy')
    plt.legend()  # 让图例生效
    plt.xticks(x, names, rotation=1)

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('k')  # X轴标签
    plt.ylabel("score")  # Y轴标签
    pyplot.yticks([0.7,0.8,0.9,1])
    # plt.title("A simple plot") #标题
    plt.savefig('D:\\knn_chart.jpg', dpi=900)
