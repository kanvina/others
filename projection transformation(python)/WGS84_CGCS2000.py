'''
create by WYD
根据WGS84地理坐标，转换为2000坐标系投影坐标
'''
from pyproj import Proj,transform
import math

def WGS84_CGCS2000(lon,lat,degree_type,is_zone_number):

    '''
    :param lon: 经度
    :param lat: 纬度
    :param degree_type:3度带或者6度带
    :param is_zone_number: 生成坐标是否包含带号
    :return:
    '''

    if int(lon)<75 or int(lon)>135:
        print('该区域不在中国境内')
    else:
        if degree_type==3:
            if is_zone_number==True:
                zone=math.floor( (lon-1.5)/3 )+1
                Epsg_test='45{0}'.format(str(zone-12) )
                p1 = Proj(init='epsg:4326')
                p2 = Proj(init='epsg:{0}'.format(Epsg_test))
                x, y = p1(lon,lat)
                x_prj, y_prj = transform(p1, p2, x, y)
                x_prj=int(x_prj)
                y_prj=int(y_prj)

            elif is_zone_number==False:
                zone=math.floor( (lon-1.5)/3 )+1
                Epsg_test = '45{0}'.format(str(zone+9))
                p1 = Proj(init='epsg:4326')
                p2 = Proj(init='epsg:{0}'.format(Epsg_test))
                x, y = p1(lon,lat)
                x_prj, y_prj = transform(p1, p2, x, y)
                x_prj=int(x_prj)
                y_prj=int(y_prj)

        elif degree_type==6:

            if is_zone_number==True:
                zone=math.floor(lon/6)+1
                epsg=str(4490+zone-12)
                p1 = Proj(init='epsg:4326')
                p2 = Proj(init='epsg:{0}'.format(epsg))
                x, y = p1(lon,lat)
                x_prj, y_prj = transform(p1, p2, x, y)
                x_prj=int(x_prj)
                y_prj=int(y_prj)

            elif is_zone_number==False:

                zone = math.floor(lon / 6) + 1
                epsg=4500+zone-11
                p1 = Proj(init='epsg:4326')
                p2 = Proj(init='epsg:{0}'.format(epsg))
                x, y = p1(lon,lat)
                x_prj, y_prj = transform(p1, p2, x, y)
                x_prj=int(x_prj)
                y_prj=int(y_prj)

    return x_prj,y_prj
def CGCS2000_WGS84(X,Y):

    p = Proj(init='epsg:4499')
    lon,lat = p(X,Y,inverse=True)
    lon=round(lon,6)
    lat=round(lat,6)
    return lon,lat

if __name__=='__main__':

    x_2000, y_2000 = WGS84_CGCS2000(117.181551,34.220359, 6, is_zone_number=True)
    print(x_2000,y_2000)

    print(CGCS2000_WGS84(x_2000,y_2000))