# coding=utf-8

# ----------------------------------------------------------------------------------------------------------------------
# What is the purpose of this Python script?

# shp2netCDF.py imports the psi-shapefile into a Space-Time-Cube (NetCDF Format).
# Merges psi results in Time (1 year) and Space (250m).
# ----------------------------------------------------------------------------------------------------------------------
# Import of the required modules
import os
import arcpy
# import pandas as pd
# import numpy as np
# from datetime import datetime
# import re

# https://www.adamerispaha.com/2017/01/24/reading-shapefiles-into-pandas-dataframes/
# https://pypi.org/project/pyshp/

# ----------------------------------------------------------------------------------------------------------------------
# directories
# ----------------------------------------------------------------------------------------------------------------------
# Root Directory:
root_dir = r'C:\Users\Judith\Documents\Studium\1_Bachelor_of_Science_Geoinformatik\Bachelorarbeit\BA'
print("Root Directory: " + root_dir)
# Directory where the input shape files are stored:
shp_dir = os.path.join(root_dir, 'Daten\A015_D139_32400_5712_20141001_20201231_BA-Bresser_v02')
print("Directory input shape files are stored: " + shp_dir)
print(os.listdir(shp_dir))
# Directory where the output geodatabase will be created:
out_gdb = os.path.join(root_dir, "shp2netCDF.gdb")
print("Directory output geodatabase will be created: " + out_gdb + "\n")

# ----------------------------------------------------------------------------------------------------------------------
# set arcgis workspace to folder and
# create empty list for the shapefiles in the input folder
# ----------------------------------------------------------------------------------------------------------------------
arcpy.env.workspace = root_dir
print("set arcgis workspace to folder has been done")
shp_files = []
print(shp_files)
print("empty list for the shapefiles were produced")

# ----------------------------------------------------------------------------------------------------------------------
# searching for shapefiles (recursive) in the input folder, append to list
# ----------------------------------------------------------------------------------------------------------------------
print("searching for shapefiles (recursive) in the input folder")
for root, dirs, files in os.walk(shp_dir):
    for file in files:
        if file.endswith(".shp") and "vertical" in file:
            # appends an element to the end of the list
            shp_files.append(os.path.join(root, file))
            print("An item has been added to the list.")
            print(shp_files)
            print()

# ----------------------------------------------------------------------------------------------------------------------
# You can use the ArcPy class Field Mappings
# ----------------------------------------------------------------------------------------------------------------------
# Create a Field Mappings object
fms_shp = arcpy.FieldMappings()
print("Create Field Mappings Object")
# Adds a table to the Field Mappings object
fms_shp.addTable(shp_files[0])
print("A table has been added to the FieldMappings object." + "\n")
print(fms_shp)
# Notice: Works as long as only one table adds to the Field Mappings object.

# ----------------------------------------------------------------------------------------------------------------------
# Loop through all attributes (columns)
# ----------------------------------------------------------------------------------------------------------------------
print("Loop through all attributes (columns)")
# print("Attribute count: ")
# print(len(fms_shp.fields))
# print()
# print("Loop starts now:")
# zaehler = 0
fields = ["lat", "lon"]
print(fields)
for field_idx in range(len(fms_shp.fields)):
    # Get current FieldMap
    field_map = fms_shp.getFieldMap(field_idx)
    # Get current Field
    field_outputField = field_map.outputField
    # Get current FieldName
    field_name = field_outputField.name
    # print("Get current FieldName:")
    # print(field_name)
    # zaehler = zaehler + 1
    # print("current attribute:" + str(zaehler))

    # Search for date columns starting with "D_20*"
    if field_name.startswith('D_20'):
        fields.append(field_name)
        print(field_name + " (starts with D_20*)")
print(fields)

# ----------------------------------------------------------------------------------------------------------------------
# The Python script runs fine up to this point. No changes necessary.
# ----------------------------------------------------------------------------------------------------------------------

'''
Function arcpy.management.CreateFolder(out_folder_path, out_name) creates a folder in the specified location
Parameters
- out_folder_path: The location on the disk where the folder will be created. (Data type: Folder)
- out_name: The folder to create. (Data type: String)
Return
The new output folder (data type: folder)
'''
out_folder_path = r'C:\Users\Judith\Documents\Studium\Test'
out_name = "folder_for_GDB"
folder_for_GDB = arcpy.management.CreateFolder(out_folder_path, out_name)
if not os.path.exists(r'C:\Users\Judith\Documents\Studium\Test\folder_for_GDB'):
    out_folder_path = r'C:\Users\Judith\Documents\Studium\Test'
    out_name = "folder_for_GDB"
    folder_for_GDB = arcpy.management.CreateFolder(out_folder_path, out_name)
else:
    print("a folder exists already")

'''
Function arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version}) 
creates a file GDB (Data Management)
Parameters
- out_folder_path: The folder where the new file GDB will be created (data type: Folder).
- out_name: The name of the file GDB to be created (data type: string).
- out_version: The ArcGIS version of the new GDB, CURRENT creates a GDB that is compatible with the currently 
               installed version of ArcGIS. This is the default setting.
Return
The new output file GDB (data type: workspace)
'''
if not os.path.exists(r'C:\Users\Judith\Documents\Studium\Test\folder_for_GDB\shp2netCDF.gdb'):
    arcpy.management.CreateFileGDB(folder_for_GDB, "shp2netCDF.gdb", "CURRENT")
else:
    print("file GDB exists already")
'''
Function arcpy.conversion.FeatureClassToFeatureClass(in_features, out_path, out_name)
converts a shapefile into a feature class
Parameters
- in_features: The feature class or feature layer to be converted. (Data type: Feature layer)
- out_path: The location where the output feature class is created. This can be a GDB or a folder
            If a folder is specified as the location, the output is a shapefile. (Datatype: Workspace;Feature Dataset)
- out_name: The name of the output feature class. (Data type: String)     
Return
The output feature class. (Data type: Feature Class)
'''
arcpy.conversion.FeatureClassToFeatureClass(shp_files[0], folder_for_GDB, "out_shpAs_featureClass")

'''
Function FeatureClassToNumPyArray (in_table, field_names) converts a feature class into a numpy array
Parameters
- in_table: The feature class, layer, table or table view (data type: string)
- field_names: A list (or tuple) of field names. Specify an asterisk (*) instead of a list of fields, 
               to access all fields of the input table 
Return

'''
numpyArray = arcpy.da.FeatureClassToNumPyArray("out_shpAs_featureClass", fields)
print(numpyArray)
# df = pd.DataFrame(voids) # an idea maybe use a DataFrame?????!!!!!
# feature_list = []
# for void in voids:
#    temp = []
#    for x in void:
#        temp.append(x)
# feature_list.append(temp)
# array = np.asarray(feature_list)
# Data are all read in and in a format where we can use this as we wish....
'''TODO: array into Space-Time-Cube'''

'''
Function arcpy.management.MakeFeatureLayer(in_features, out_layer)  creates a Feature-Layer
Parameters
- in_features: The input feature class or layer from which the new layer is created. 
               Complex feature classes such as annotation and dimension feature classes are not allowed as inputs.
               (Data type: Feature Layer)
- out_layer: The name of the feature layer to be created. 
             The newly created layer can be used as an input to any geoprocessing tool for which feature layers 
             can be entered. (Data type: Feature Layer)
'''
# arcpy.management.MakeFeatureLayer(shp_dir, featureLayer)

'''
Function arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field) creates a space-time cube
Parameters
- in_features: The input point feature class to aggregate to space-time sections. (Data type: Feature layer)
- output_cube: The output netCDF data cube to be created,
               which contains the number and summaries of point data from input features. (Data type: File)
- time_field:  The field containing date and time information (timestamp) for each point.
              This field must be of type "Date". (Data type: Field)
'''
# cube = arcpy.stpm.CreateSpaceTimeCube(featureLayer, PSI.nc, time_field)


# ----------------------------------------------------------------------------------------------------------------------
# Idea collection, programming ideas
# ----------------------------------------------------------------------------------------------------------------------
# Check and Create GDB
# if not arcpy.Exists(os.path.join(root_dir, out_gdb)):
#   arcpy.management.CreateFileGDB(root_dir, 'shp2netCDF.gdb', 'CURRENT')

# Check and Remove Feature Class
# if arcpy.Exists(os.path.join(out_path, out_name)):
#   arcpy.Delete_management(out_name)

# Save Feature Class to GDB
# arcpy.conversion.FeatureClassToFeatureClass(in_features, out_path, out_name, '#', fms_out)
