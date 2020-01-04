import requests
import json
from coordTransform import bd09_to_wgs84
import pandas as pd
import numpy as np

def get_location_84(poi_name,ak):

    # url='http://api.map.baidu.com/place/v2/search?query='+poi_name+'&tag=房地产&region=徐州&output=json&ak='+ak
    url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak={0}&address={1}'.format(ak,poi_name)
    res = requests.get(url)
    jd = json.loads(res.text)
    location_dict=jd['result']['location']# json转字典
    lng=location_dict['lng']
    lat=location_dict['lat']
    location_84 = bd09_to_wgs84(lng, lat)
    return location_84

if __name__=="__main__":


    '''
    密钥收集：
    1w96poA4G1mQM7noqGUO86aS
    1b7ddac06e2b9a3622aa586959c99733
    1XjLLEhZhQNUzd93EjU5nOGQ
    
    zbLsuDDL4CS2U0M4KezOZZbGUY9iWtVf
    nSxiPohfziUaCuONe4ViUP2N 
    PlhFWpA02aoURjAOpnWcRGqw7AI8EEyO
    OBdehyusfGE2KRAvik4jhzb0gQ1VgfA
    DD279b2a90afdf0ae7a3796787a0742e

    '''
    plot_list=np.array(pd.read_excel('data_result/no_match_list.xls'))
    data_out_list=[]
    no_match_list=[]
    for plot_line in plot_list:
        plot_name = plot_line[0]

        try:
            location=get_location_84(plot_name,'1w96poA4G1mQM7noqGUO86aS')
            lng=location[0]
            lat=location[1]
            data_out_list.append([plot_name,lng,lat])
            print(plot_name,lng,lat)
        except:
            no_match_list.append([plot_name])
            print('no location information',plot_name)

    pd.DataFrame(data_out_list,columns=['plot_name','lng','lat']).to_csv('data_result/徐州小区数据.csv',index=0,header=0,mode='a+')
    pd.DataFrame(no_match_list,columns=['plot_name']).to_excel('data_result/no_match_list.xls',index=0)





