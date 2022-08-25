
import xarray as xr
# import of a single netCDF file
dataDIR = 'C:/Users/Judith/Documents/Studium/1 - Bachelor of Science Geoinformatik/Bachelorarbeit/BA/Daten/NC_Vector_Cube/NC/dcb.nc'
# store in a DataSet
DS = xr.open_dataset(dataDIR)