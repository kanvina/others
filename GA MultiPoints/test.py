from osgeo import gdal


ds = gdal.Open('data_figure/埋深_100_西区.tif')
band = ds.GetRasterBand(1)#DEM数据只有一种波段
data = band.ReadAsArray()#data即为dem图像像元的数值矩阵
