import numpy as np
# import matplotlib.pyplot as plt
from osgeo import gdal
import matplotlib.pyplot as plt



def get_ori_pop(num_points,num_pop,x_max,y_max):
    '''
    :param num_points: 点数量
    :param num_pop: 种群数量
    :param x_max: x最大值
    :param y_max: y最大值
    :return:
    '''
    ori_pop=[]
    n=0
    while n < num_pop:
        pop=[]
        i=0
        while i < num_points:#生成一套方案
            locationA = np.random.randint(0, x_max)
            locationB = np.random.randint(0, y_max)
            if [locationA,locationB] not in pop:
                pop.append([locationA,locationB])
                i = len(pop)

        if pop not in ori_pop:
            ori_pop.append(pop)
            n=len(ori_pop)

    ori_pop=np.array(ori_pop)
    return ori_pop

def select(pop, fitness):    # 根据概率选择
    idx = np.random.choice(np.arange(len(pop)), size=len(pop), replace=True,p=(fitness/fitness.sum()))
    return pop[idx]

def crossover(parent_a, parent_b_list,cross_rate,x_max,y_max):     # 随机交叉

    if np.random.rand() < cross_rate:

        x_max_cross,y_max_cross,a=np.shape(parent_b_list)

        index_parent_b = np.random.randint(0, len(parent_b_list), size=1)[0]
        parent_b=parent_b_list[index_parent_b]
        index_cross_list = np.random.randint(0, 2, size=len(parent_b)).astype(np.bool)

        child = []
        for i in range(len(parent_a)):
            is_cross=index_cross_list[i]
            if is_cross == True :

                if list(parent_b[i]) not in child:
                    child.append(list(parent_b[i]))
                elif list(parent_a[i]) not in child :
                    child.append(list(parent_a[i]))
                else:
                    is_add=0
                    while i ==0:
                        locationA = np.random.randint(0, x_max_cross)
                        locationB = np.random.randint(0, y_max_cross)
                        if [locationA,locationB] not in child:
                            child.append([locationA,locationB])
                            is_add = 1
            else:

                if list(parent_a[i]) not in child:
                    child.append(list(parent_a[i]))
                else:
                    is_add=0
                    while i ==0:
                        locationA = np.random.randint(0, x_max)
                        locationB = np.random.randint(0, y_max)
                        if [locationA,locationB] not in child:
                            child.append([locationA,locationB])
                            is_add = 1


        child=np.array(child)

    else:
        child=parent_a

    return child

def mutate(child,x_max,y_max): #变异

    for i in range(len(child)):
        if np.random.rand() < MUTATION_RATE:
            row=np.random.randint(0, x_max)
            column=np.random.randint(0, y_max)

            if [row,column] not in child:
                child[i] =[row,column]

    return child

def target_fun(data,points_list):
    target_value=0
    for points in points_list:
        points_x=points[0]
        points_y=points[1]
        value=data[points_x,points_y]
        target_value=target_value+value
    return target_value

def draw_fig(data,r_max):
    data_show = np.array(data)
    x_list=[]
    y_list=[]
    for r_c in data_show:
        x_list.append(r_c[1])
        y_list.append(r_max-r_c[0])
    plt.scatter(x_list,y_list)
    plt.pause(0.1)
    plt.cla()

if __name__=="__main__":
    num_points = 100

    num_iteration=2000
    num_population=100
    CROSS_RATE = 0.8
    MUTATION_RATE = 0.01

    ds = gdal.Open('data_figure/埋深_100_西区.tif')
    band = ds.GetRasterBand(1)  # DEM数据只有一种波段
    data = band.ReadAsArray()  # data即为dem图像像元的数值矩阵
    x_max,y_max=np.shape(data)

    pop=get_ori_pop(num_points,num_population, x_max,y_max)

    n_iteration_text=0
    max_result=0
    max_n_iteration=0
    pop_max_result = []

    for i in range (num_iteration):
        n_iteration_text=n_iteration_text+1
        target_value_list=[]
        for points_list in pop:

            target_value=target_fun(data,points_list)
            target_value_list.append(target_value)
        target_value_list=np.array(target_value_list)
        idx = np.random.choice(len(target_value_list), size=len(target_value_list), replace=True,p=(target_value_list/target_value_list.sum()))

        pop=pop[idx]
        pop_copy=pop.copy()

        for parent in pop:
            child=crossover(parent,pop_copy,CROSS_RATE,x_max,y_max)
            child = mutate(child,x_max,y_max)
            parent = child

        i = 0
        mean_value = 0
        max_value = 0
        pop_max_value=[]

        for pop_list in pop:
            i = i + 1
            value = target_fun(data, pop_list)
            if value >max_value:
                max_value=value
                pop_max_value=pop_list
            mean_value=mean_value+value
        mean_value=mean_value/i
        if max_value > max_result:
            max_n_iteration=n_iteration_text
            max_result=max_value
            pop_max_result=pop_max_value

            draw_fig(pop_max_result, x_max)

        if n_iteration_text %50==0:

            print('当前代数：',n_iteration_text,'均值：',int(mean_value),
                  '当前代数最大值：',int(max_value),'全局最大值所在代数：',max_n_iteration,'全局最大值：',int(max_result))
    print(pop_max_result)
    draw_fig(pop_max_result,x_max)



















