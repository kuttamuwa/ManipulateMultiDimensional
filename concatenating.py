import netCDF4
from netCDF4 import Dataset
import numpy as np
import datetime
import rioxarray, rasterio, xarray as xr
from osgeo import gdal
from rasterio.control import GroundControlPoint as GCP_r
from gdal import GCP as GCP_g
from rasterio.control import GroundControlPoint as GCP_r
import cv2
from affine import Affine as AffineLib

# ncpath_1 = r"/home/umut/PycharmProjects/MGM/raster/testdata/5layers/source/wrf_20200214_00_1.nc"
ncpath_2 = r"testdata/netcdfs/wrf_20200214_00_1.nc"
ncpath_3 = r"testdata/netcdfs/wrf_20200214_00_3.nc"

ncpath_4 = r"testdata/netcdfs/wrf_20200214_00_4.nc"
ncpath_5 = r"testdata/netcdfs/wrf_20200214_00_5.nc"
ncpath_6 = r"testdata/netcdfs/wrf_20200214_00_6.nc"

ncout_path = r"testdata/netcdfs/out/wrf_20200214_00_a.nc"

# nc_in_1 = Dataset(ncpath_1, 'r', format='NETCDF4')
nc_in_2 = Dataset(ncpath_2, 'r', format='NETCDF4')
nc_in_3 = Dataset(ncpath_3, 'r', format='NETCDF4')

nc_in_4 = Dataset(ncpath_4, 'r', format='NETCDF4')
nc_in_5 = Dataset(ncpath_5, 'r', format='NETCDF4')
nc_in_6 = Dataset(ncpath_6, 'r', format='NETCDF4')


latitude = nc_in_2.variables['latitude']
longitude = nc_in_2.variables['longitude']
times = [datetime.datetime(2019, 10, 1) + datetime.timedelta(hours=i) for i in range(5)]
units = 'hours since 2019-10-01 00:00'
calendar = 'standard'

# temperature_2 = nc_in_2.variables['t2_0']

temperature_2 = np.array([np.float32(i) for i in nc_in_2.variables['t2_0']])
temperature_3 = np.array([np.float32(i) for i in nc_in_3.variables['t2_0']])
temperature_4 = np.array([np.float32(i) for i in nc_in_4.variables['t2_0']])
temperature_5 = np.array([np.float32(i) for i in nc_in_5.variables['t2_0']])
temperature_6 = np.array([np.float32(i) for i in nc_in_6.variables['t2_0']])

# create netcdf
nc_out = Dataset(ncout_path, 'w', format='NETCDF4')

# dimensions
nc_out.createDimension('time', size=len(times))  # unlimited
nc_out.createDimension('x_loc', size=len(latitude))
nc_out.createDimension('y_loc', size=len(longitude))

# create latitude axis
lat = nc_out.createVariable('lat', np.dtype('double').char, ('lat'))
lat.standard_name = 'latitude'
lat.long_name = 'latitude'
lat.units = 'degrees_north'
lat.axis = 'Y'

# create longitude axis
lon = nc_out.createVariable('lon', np.dtype('double').char, ('lon'))
lon.standard_name = 'longitude'
lon.long_name = 'longitude'
lon.units = 'degrees_east'
lon.axis = 'X'

# create time axis
time = nc_out.createVariable('time', np.dtype('double').char, ('time',))
time.long_name = 'time'
time.units = 'hours since 2019-10-01 00:00:00'
time.calendar = 'standard'
time.axis = 'T'
time[:] = netCDF4.date2num(times, units=units, calendar=calendar)
time = netCDF4.num2date(time[:], units=units, calendar=calendar)


# create variable array
temp_out = nc_out.createVariable('t2_0', np.dtype('double').char, ('time', 'lat', 'lon'))
temp_out.long_name = '2 metre temperature'
temp_out.units = 'K'

# copy axis from original dataset
# print(first_latitude, first_longitude)
lon[:] = longitude[:]
lat[:] = latitude[:]

# lon[:] = longitude[:]
# lat[:] = latitude[:]
concat_temp = np.concatenate([temperature_2, temperature_3, temperature_4, temperature_5, temperature_6])
temp_out[:] = concat_temp[:]
nc_out.close()

nc_in_2.close()
nc_in_3.close()
nc_in_4.close()
nc_in_5.close()
nc_in_6.close()
