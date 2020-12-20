# !/usr/bin/env python3
# ----------------------------------
# Read GRD and GeoTiffs with xarray or pygmt
# (differences among the 2 methods can depend on the interpolation method used)
# ----------------------------------
# Author: Stefano Bertone
# Created: 15-Sep-2020
#

import numpy as np
import pandas as pd
import time

import xarray as xr
import pyproj
import pygmt  # needs GMT 6.1.1 installed, plus linking of GMTdir/lib64/libgmt.so to some general lib dir (see bottom of https://www.pygmt.org/dev/install.html)

debug = False

def get_demz_tiff(filin,lon,lat):

    # Read the data
    da = xr.open_rasterio(filin)

    # Rasterio works with 1D arrays (but still need to pass whole mesh, flattened)
    # convert lon/lat to xy using intrinsic crs, then generate additional dimension for
    # advanced xarray interpolation
    p = pyproj.Proj(da.crs)
    xi, yi = p(lon, lat, inverse=False)
    xi = xr.DataArray(xi, dims="z")
    yi = xr.DataArray(yi, dims="z")

    if debug:
        print(da)
        print("x,y len:", len(xi),len(yi))

    da_interp = da.interp(x=xi,y=yi)

    return da_interp.data*1.e-3 # convert to km for compatibility with grd

def get_demz_grd(filin,lon,lat):

    da = xr.open_dataset(filin)
    # for LDAM_8, rename coordinates
    da = da.rename({'x':'lon','y':'lat'})

    lon[lon < 0] += 360.
    lon = xr.DataArray(lon, dims="x")
    lat = xr.DataArray(lat, dims="x")

    if debug:
        print(da)
        print("lon,lat len:", len(lon),len(lat))

    da_interp = da.interp(lon=lon,lat=lat)

    return da_interp.z.values


def read_dem(dem_to_read, method):

    start = time.time()

    if method == 'xarray':


        if dem_to_read.split('.')[-1] == 'GRD':  # to read grd/netcdf files
            z = get_demz_grd(dem_to_read, lon, lat)
        elif dem_to_read.split('.')[-1] == 'TIF':  # to read geotiffs usgs
            z = np.squeeze(get_demz_tiff(dem_to_read, lon, lat))

        out = pd.DataFrame([lon, lat, z], index=['lon', 'lat', 'z']).T

    elif method == 'pygmt':

        points = pd.DataFrame([lon, lat], index=['lon', 'lat']).T
        out = pygmt.grdtrack(points, dem_to_read, newcolname='z')

    end = time.time()

    return out, end-start

if __name__ == '__main__':

    start = time.time()

    methods = ['xarray','pygmt']

    # select elevation model to read
    dem_to_read = '../data/LDAM_8.GRD'

    # get random lat/lon list where to request elevation
    number_of_samples = 100000
    rng = np.random.default_rng()
    lon = rng.random((number_of_samples))*360. # if grd lon is [0,360)
    lat = (rng.random((number_of_samples))*2-1)*90. # if grd lat is [-90,90)

    # read using both methods and compare results
    for m in methods:
        out, runt = read_dem(dem_to_read=dem_to_read, method=m)
        print(out)
        print(f"## Reading/interpolation of {number_of_samples} samples finished "
              f"after {np.round(runt,2)} sec using method {m}!")
