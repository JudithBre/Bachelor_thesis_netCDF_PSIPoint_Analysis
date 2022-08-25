# General information

For the development, I use
- [the development environment PyCharm](https://www.jetbrains.com/pycharm/)
- [ArcGIS Pro](https://www.esri.com/de-de/arcgis/products/arcgis-pro/overview)

First, create a new ArcGIS Pro project. 
You must be in the university network or connected via VPN if you use the university license of ArcGIS.
Under Project and Python in the ArcGIS Pro Project, you can set the Python Package Manager.
Here it is essential to clone the familiar environment of Python under Manage Environments to be able to install its packages later. 
[see figure](https://github.com/JudithBre/Bachelor_thesis_netCDF_PSIPoint_Analysis/issues/2) or
[see for further information if you need help](https://developers.arcgis.com/python/guide/install-and-set-up/#Installation-using-Python-Package-Manager) 

After creating a new ArcGIS Pro project, create a new PyCharm project and set the Python interpreter to the environment created in ArcGIS Pro! [see figure](https://github.com/JudithBre/Bachelor_thesis_netCDF_PSIPoint_Analysis/issues/1)

- - -

# Use of the file shp2netCDF.py

**Getting started**

1. If you want to use arcpy, you must be on the university network or connected via VPN if you use the university license of ArcGIS.

2. Customization of the directories

3. Integration of a shapefile


**Useful links for working with netCDF**

- [What are netCDF data?](https://desktop.arcgis.com/de/arcmap/latest/manage-data/netcdf/what-is-netcdf-data.htm)
- [Basic netCDF terminology](https://desktop.arcgis.com/de/arcmap/latest/manage-data/netcdf/essential-netcdf-vocabulary.htm)
- [CF Metadata Conventions](http://cfconventions.org/)
- [Network Common Data Form (NetCDF)](https://www.unidata.ucar.edu/software/netcdf/)

**Useful links to work with ArcGIS**

- [Definition of workspace in ArcGIS](https://pro.arcgis.com/de/pro-app/latest/tool-reference/environment-settings/current-workspace.htm)
- [Overview of the "Space Time Pattern Mining" Toolbox](https://desktop.arcgis.com/de/arcmap/latest/tools/space-time-pattern-mining-toolbox/an-overview-of-the-space-time-pattern-mining-toolbox.htm)
- [Create space-time cube by aggregating points](https://desktop.arcgis.com/de/arcmap/latest/tools/space-time-pattern-mining-toolbox/create-space-time-cube.htm)

**Useful links when dealing with ArcPy**

- [What is ArcPy?](https://pro.arcgis.com/de/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm)
- [Importing ArcPy](https://pro.arcgis.com/de/pro-app/latest/arcpy/get-started/importing-arcpy.htm)
- [An overview of ArcPy classes](https://pro.arcgis.com/de/pro-app/latest/arcpy/classes/alphabetical-list-of-arcpy-classes.htm)
- [FieldMappings](https://pro.arcgis.com/de/pro-app/latest/arcpy/classes/fieldmappings.htm)
- [FieldMap](https://pro.arcgis.com/de/pro-app/latest/arcpy/classes/fieldmap.htm)

- - -

# Use of the file analyse_nc_xarray.py

**Getting started**

- To work with the xarray package, manually install it. 
Do this in the Package Manager environment in ArcGIS Pro.
[see figure](https://github.com/JudithBre/Bachelor_thesis_netCDF_PSIPoint_Analysis/issues/3)


**Useful links to work with xarray**

- [Xarray documentation](https://docs.xarray.dev/en/stable/)
