import rasterio
from rasterio.crs import CRS
from rasterio.control import GroundControlPoint as rGCP
from gdal import GCP as gGCP
import osr
from rasterio.warp import calculate_default_transform, reproject
import gdal
import numpy as np
import shutil
import xarray
import matplotlib
import matplotlib.pyplot as plt


src_tiff = r"testdata/tiffs/t2.tif"
dest_tiff = r"testdata/tiffs/t2_modified.tif"
dest_tiff_v2 = r"testdata/tiffs/t2_modifiedv2.tif"  # it will be use for another solution

# lets copy it and then georeference target
shutil.copy(src_tiff, dest_tiff)

# reading with rasterio
src_tiff_rasterio = rasterio.open(src_tiff, driver='GTiff', crs=None)

# reading with gdal
src_tiff_gdal = gdal.Open(src_tiff)

# CAUTION: You cannot read netcdf data via gdal.GA_UPDATE. Shit.
dest_tiff_gdal = gdal.Open(dest_tiff, gdal.GA_Update)

# length of x, y axis
src_xsize, src_ysize = src_tiff_gdal.RasterXSize, src_tiff_gdal.RasterYSize

# coordinate systems
src_epsg = CRS({'init': 'EPSG:4326'})
sr = osr.SpatialReference()
sr.ImportFromEPSG(4326)

"""
Please research how to import gcp for rasterio and gdal. For gdal, there is Z parameter as third order.
"""
# gcp
r_gcps = [
    rGCP(0.0, 0.0, 6.830896, 50.69396),
    rGCP(0.0, src_ysize, 6.830896, 28.65548),
    rGCP(src_xsize, src_ysize, 52.5051, 28.65548),
    rGCP(src_xsize, 0.0, 52.5051, 50.69396),
]

g_gcps = [
    gGCP(0.0, 0.0, 0.0, 6.830896, 50.69396),
    gGCP(0.0, src_ysize, 0.0, 6.830896, 28.65548),
    gGCP(src_xsize, src_ysize, 0.0, 52.5051, 28.65548),
    gGCP(src_xsize, 0.0, 0.0, 52.5051, 50.69396),
]

# setting and closing. But I am not sure below one.
dest_tiff_gdal.SetGCPs(g_gcps, sr.ExportToWkt())
dest_tiff_gdal = None

"""
I found another way. If above one does not work, please check this:
"""
tiff_opened_rasterio = rasterio.open(src_tiff, mode='r', driver='GTiff')

# you will see there is many things around profile of rasterio data
src_tiff_rasterio_profile = tiff_opened_rasterio.profile
dst_tiff_rasterio_profile = src_tiff_rasterio_profile.copy()

rasterio_affine = rasterio.transform.from_gcps(
    gcps=r_gcps
)  # return Affine

# This affine object is very useful. I read this but those formula did not make sense to me. Maybe you can explain ha?
# https://www.perrygeo.com/python-affine-transforms.html

# this is key
dst_tiff_rasterio_profile["transform"] = rasterio_affine

# I don't know maybe my data is silly
dst_tiff_rasterio_profile["height"], dst_tiff_rasterio_profile["width"] = dst_tiff_rasterio_profile["width"], \
                                                                          dst_tiff_rasterio_profile["height"]

# final processes
dst_rasterio = rasterio.open(dest_tiff_v2, 'w', **dst_tiff_rasterio_profile)
dst_rasterio.write(tiff_opened_rasterio.read())
dst_rasterio.close()
