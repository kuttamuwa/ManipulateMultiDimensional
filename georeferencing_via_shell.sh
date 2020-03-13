# you need to install gdal

# this is georeferencing via ground control points. You can change with your gcps
# shit thing is you cannot georeference netcdf via gdal. you need to convert them into geotiff - what a silly - and

# btw, you may want to check "georeferencing_via_gdal.py" out.

gdal_translate -of GTiff -gcp 0.0 0.0 6.8309 50.694 -gcp 0.0 816.0 6.8309 28.6555 -gcp 1690.0 816.0 52.5051 28.6555 -gcp 1690.0 0.0 52.5051 50.694
 "testdata/netcdfs/wrf_20200214_00_1.nc:t2_0" "testdata/netcdfs/wrf_20200214_00_1_t2.tiff"

# after that you need to warp it. You can use EPSG
gdalwarp -r near -order 1 -co COMPRESS=NONE -dstSRS EPSG:4326 "testdata/netcdfs/wrf_20200214_00_1_t2.tiff"
"testdata/netcdfs/wrf_20200214_00_1_t2_4326.tiff"