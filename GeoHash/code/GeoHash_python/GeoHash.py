'''
create by wyd
GeoHash示例代码
'''
'''
base32码
'''
BASE32 = ['0','1','2','3','4','5','6','7','8',
          '9','b','c','d','e','f','g','h','j',
          'k','m','n','p','q','r','s',
          't','u','v','w','x','y','z']


def get_2_geocode(lng,lat,n):

    LngRange=[-180,180]
    LatRange=[-90,90]
    geocode_2_lng=[]
    geocode_2_lat=[]
    geocode_2_all=[]
    is_n_odd=False
    if n %2 !=0:
        n=n+1
        is_n_odd=True
    len_geocode_2= int(n*5/2)
    for i in range(len_geocode_2):
        if lng<=(LngRange[0]+LngRange[1])/2 and lng > LngRange[0]:
            geocode_2_lng.append(0)
            LngRange[1]=(LngRange[0]+LngRange[1])/2

        else:
            geocode_2_lng.append(1)
            LngRange[0] = (LngRange[0] + LngRange[1]) / 2

        if lat <= (LatRange[0] + LatRange[1]) / 2 and lat > LatRange[0]:
            geocode_2_lat.append(0)
            LatRange[1]=(LatRange[0] + LatRange[1]) / 2
        else:
            geocode_2_lat.append(1)
            LatRange[0]=(LatRange[0] + LatRange[1]) / 2
    del i
    for i in range(len_geocode_2):

        geocode_2_all.append(geocode_2_lng[i])
        geocode_2_all.append(geocode_2_lat[i])
    del i

    GeoHash_code = ''

    if is_n_odd == True:
        n=n-1
    for i in range(n):
        code_list=geocode_2_all[i*5:i*5+5]
        number=0
        for code_num in range(5):
            number=number+(code_list[code_num])*(2**(4-code_num))
        GeoHash_code=GeoHash_code+BASE32[number]


    print(GeoHash_code)





if __name__=="__main__":
    lng=114
    lat=39
    n=8
    get_2_geocode(lng, lat, n)