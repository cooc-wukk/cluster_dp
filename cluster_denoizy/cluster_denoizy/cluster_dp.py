# coding: utf-8
# In[26]:
from loaddata import *
from class_gethalo import *
from get_halo import getHalo
from kn1 import setHalo
from calAccuricy import calAcc
from arrLeb import arrLeb
from drawPt import draw
from knn import getKnndataSet
from knn import knnClassify0
from halo_remo import setHaloRemo
from dataout import *
from chartZ import draw_score
from gradu_sethall import *

#加载数据
dataSet, real = loadDataFromFile('data3/wh.txt')
#计算距离矩阵、阈值dc
dist,dc = getDist(dataSet, 0.02)
#求点的局部密度(local density)
rho = calDensity(dist, dc)
#print('当前数据集所有点的局部密度为：',rho)
#求比点的局部密度大的点到该点的最小距离即 delta 距离
delta, nneigh = calDelta(dist, rho)
#设置参数
# rhomin = 60; deltamin = 0.6   # wh2center
#rhomin = 20; deltamin = 0.2   # wh3center
# rhomin = 75; deltamin = 0.5   # bj2center
#rhomin = 50; deltamin = 0.3   # bj3center
# rhomin = 40; deltamin = 0.21   # mnh2center
# rhomin = 40; deltamin = 0.17   # mnh3center
#rhomin = 40; deltamin = 0.07   # mnh4center
#rhomin = 40; deltamin = 0.05   # mnh5center
#rhomin = 20; deltamin = 0.2   # mnh5center
# rhomin = 10; deltamin = 0.2   # wh3cmi
rhomin = 45; deltamin = 0.05   # mnh4cmi


#确定聚类类别，将所有数据点归类
num, mark,imark = getMark(rho, delta, nneigh, rhomin, deltamin)
# 得到噪声
halo = getHalo(mark, num, imark, dist, dc, rho)
###三种降噪的方法###
#@@ 1   knn降噪
#testSet, trainSet, trainlab, iId = getKnndataSet(dataSet, halo)
#leb1 = knnClassify0(testSet, trainSet, trainlab,iId, halo)
#@@ 2   haohao循环生长降噪 更合理的样子
#leb2 = setHalo(dataSet, halo)
leb2 = Gradu_setHalo(dataSet, halo)
#@@ 3   yan 最邻近kn1降噪
#leb3 = setHaloRemo(dataSet, halo)
#聚类结果二类化
newleb = arrLeb(dataSet[:,0], dataSet[:,1], leb2)
#newleb = arrLeb(dataSet[:,0], dataSet[:,1], mark)
#绘制结果，第三个参数按需改变（halo,leb,newleb)
draw(rho, delta, leb2, dataSet)
#计算精度
precision_score, recall_score, f1_score, accuracy_score = calAcc(real, newleb)
print("precision_score\t",precision_score,"\n""recall_score\t",recall_score,"\n"+"f1_score\t",f1_score,"\n"+"accuracy_score\t",accuracy_score)
#将分类结果导入excel
# data_write(newleb, 'wh')

#draw_score(f1_score ,accuracy_score)