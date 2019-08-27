'''
可视化空间点数据
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from collections import Counter


if __name__ =="__main__":
    lng_lat_list=np.array(pd.read_csv('data/上海市银行坐标信息.csv'))[:,[1,2]]
    name=np.array(pd.read_csv('data/上海市银行坐标信息.csv'))[:,0]

    '''
    DBSCAN
    '''
    # # eps和min_samples 需要进行调参
    # y_pred = DBSCAN(eps=0.01, min_samples=10).fit_predict(lng_lat_list)
    # print(y_pred)
    # plt.scatter(lng_lat_list[:, 0], lng_lat_list[:, 1], c=y_pred)
    # plt.show()

    '''
    K-mean
    '''
    k = 10  # 聚类的类别
    iteration = 500  # 聚类最大循环次数
    model = KMeans(n_clusters=k, max_iter=iteration)  # 分为k类，并发数4
    model.fit(lng_lat_list)  # 开始聚类
    index_labels_list=model.labels_
    print((np.concatenate(([name],[index_labels_list]),axis=0)).transpose())
    plt.scatter(lng_lat_list[:, 0], lng_lat_list[:, 1], c=index_labels_list)
    plt.show()




