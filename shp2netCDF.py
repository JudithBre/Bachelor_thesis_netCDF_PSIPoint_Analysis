# coding=utf-8

# ----------------------------------------------------------------------------------------------------------------------
# What is the purpose of this Python script?

# shp2netCDF.py imports the psi-shapefile into a Space-Time-Cube (NetCDF Format).
# Merges psi results in Time (1 year) and Space (250m).
# ----------------------------------------------------------------------------------------------------------------------
# Import of the required modules
import os
import arcpy
import pandas as pd
import numpy as np
from datetime import datetime
import re

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
# Create a Folder (Data Management)
# ----------------------------------------------------------------------------------------------------------------------
folder_for_GDB = arcpy.management.CreateFolder(out_gdb, "folder_for_GDB")
print(folder_for_GDB)
'''
arcpy.management.CreateFolder(out_folder_path, out_name)

out_folder_path: Der Speicherort auf dem Datenträger, an dem der Ordner erstellt wird. (Datentyp Folder)
out_folder_path: Der zu erstellende Ordner. (Datentyp String)
'''
# ----------------------------------------------------------------------------------------------------------------------
# Create a file Geodatabase (Data Management)
# ----------------------------------------------------------------------------------------------------------------------
arcpy.management.CreateFileGDB(folder_for_GDB, "shp2netCDF.gdb")

'''
arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})

out_folder_path: Der Ordner, in dem die neue File-GDB erstellt wird (Datentyp Folder)
out_name: Der Name der zu erstellenden File-GDB (Datentyp String)
'''

# ----------------------------------------------------------------------------------------------------------------------
# Converts a shapefile into a feature class
# ----------------------------------------------------------------------------------------------------------------------
arcpy.conversion.FeatureClassToFeatureClass(shp_dir, out_gdb, "out_psi_featureClass")

'''
arcpy.conversion.FeatureClassToFeatureClass(in_features, out_path, out_name, 
                                           {where_clause}, {field_mapping}, {config_keyword})
                                           
in_features: Die zu konvertierende Feature-Class bzw. der zu konvertierende Feature-Layer. (Datentyp Feature Layer)
out_path: Der Speicherort, an dem die Ausgabe-Feature-Class erstellt wird. 
          Dies kann eine GDB oder ein Ordner sein. 
          Wird ein Ordner als Speicherort angegeben, ist die Ausgabe ein Shapefile. (Datentyp Workspace;Feature Dataset)  
out_name: Der Name der Ausgabe-Feature-Class. (Datentyp String)                             
'''

# ----------------------------------------------------------------------------------------------------------------------
# Converts a feature class into a structured NumPy array
# ----------------------------------------------------------------------------------------------------------------------
voids = arcpy.da.FeatureClassToNumPyArray("out_psi_featureClass", fields)
print(voids)

'''
FeatureClassToNumPyArray (in_table, field_names, 
                         {where_clause}, {spatial_reference}, {explode_to_points}, {skip_nulls}, {null_value})

in_table: Die Feature-Class, der Layer, die Tabelle oder die Tabellensicht (Datentyp String)
field_names: Eine Liste (oder ein Tupel) von Feldnamen. 
             Geben Sie anstelle einer Felderliste ein Sternchen (*) an, 
             um auf alle Felder der Eingabetabelle zuzugreifen 
'''


# df = pd.DataFrame(voids) # eine Idee von vielleicht ein DataFrame nutzen?????!!!!!
# feature_list = []
# for void in voids:
#    temp = []
#    for x in void:
#        temp.append(x)
# feature_list.append(temp)
# array = np.asarray(feature_list)
# Daten sind alle eingelesen und in einem Format in dem wir dies beliebig weiterverwenden können....
'''TODO: array into Space-Time-Cube'''


# arcpy.management.MakeFeatureLayer(shp_dir, featureLayer)

'''
arcpy.management.MakeFeatureLayer(in_features, out_layer, {where_clause}, {workspace}, {field_info})

in_features: Die Eingabe-Feature-Class oder der Eingabe-Feature-Layer, aus der bzw. dem der neue Layer erstellt wird. 
          Komplexe Feature-Classes wie Annotation- und Dimension-Feature-Classes sind als Eingaben nicht zulässig.
          (Datentyp Feature Layer)
out_layer: Der Name des zu erstellenden Feature-Layers. Der neu erstellte Layer kann als Eingabe bei jedem beliebigen 
           Geoverarbeitungswerkzeug verwendet werden, für das Feature-Layer eingegeben werden können. 
           (Datentyp Feature Layer)

https://pro.arcgis.com/de/pro-app/latest/tool-reference/data-management/make-feature-layer.htm
'''

# ----------------------------------------------------------------------------------------------------------------------
# Creates a space-time cube

# Funktion arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field)
# Parameters
# in_features: The input point feature class to aggregate to space-time sections. (Data type: Feature layer)
# output_cube: The output netCDF data cube to be created,
#              which contains the number and summaries of point data from input features. (Data type: File)
# time_field:  The field containing date and time information (timestamp) for each point.
#              This field must be of type "Date". (Data type: Field)
# ----------------------------------------------------------------------------------------------------------------------
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
