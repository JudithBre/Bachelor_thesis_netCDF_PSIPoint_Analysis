# coding=utf-8
import numpy as np
print("numpy as np has been imported")
import pandas as pd
print("pandas as pd has been imported")
import xarray as xr
print("xarray as xr has been imported")

# import of a single netCDF file
dataDIR = 'C:/Users/Judith/Documents/Studium/1 - Bachelor of Science Geoinformatik/Bachelorarbeit/BA/Daten/NC_Vector_Cube/NC/dcb.nc'
print(dataDIR)
dataSet = xr.open_dataset(dataDIR)
print(dataSet)