"""
Do you have gdal shell commands but do know how to do those on Python? You hate subprocess? Come here, boy.

ex: georeferencing
"""

from osgeo import gdal, osr
from gdal import GCP as GCP_g
from pathlib import Path
import shutil

# This is useful if you read netcdf
gdal.UseExceptions()

# our files
src_nc = r"testdata/netcdfs/wrf_20200214_00_1.nc"
dst_nc = r"testdata/netcdfs/out/viagdal.tiff"
var_name = "t2_0"

# our georeferencing points
GCPList_gdal = [GCP_g(6.830896, 50.69396, 0.0, 0.0, 0.0),
                GCP_g(6.830896, 28.65548, 0.0, 0.0, 816.0),
                GCP_g(52.5051, 28.65548, 0.0, 1690.0, 816.0),
                GCP_g(52.5051, 50.69396, 0.0, 1690.0, 0.0)]

# Watch it! You still need to set variable of netcdf
src_raster = gdal.Open(f"NETCDF:{src_nc}:{var_name}")

# gdal and warp parameters
opts = "-of GTiff -gcp 0.0 0.0 6.8309 50.694 -gcp 0.0 816.0 6.8309 28.6555 -gcp 1690 816.0 52.5051 28.6555 -gcp 1690.0 0.0 52.5051 50.694"
warp_opts = "-r near -order 1 -co COMPRESS=NONE"

translateOptions = gdal.TranslateOptions(gdal.ParseCommandLine(opts))
warpOptiosn = gdal.WarpOptions(gdal.ParseCommandLine(warp_opts))

gdal.Translate(dst_nc, src_raster, options=translateOptions)
# todo: I didnt solve warp yet. You can try it till I've done.
gdal.Warp()