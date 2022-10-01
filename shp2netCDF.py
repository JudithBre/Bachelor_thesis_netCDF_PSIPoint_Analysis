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
out_gdb = os.path.join(root_dir, 'shp2netCDF.gdb')
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

voids = arcpy.da.FeatureClassToNumPyArray(root_dir, fields)
print(voids)
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

in_layer: Die Eingabe-Feature-Class oder der Eingabe-Feature-Layer, aus der bzw. dem der neue Layer erstellt wird. 
          Komplexe Feature-Classes wie Annotation- und Dimension-Feature-Classes sind als Eingaben nicht zulässig.
          (Datentyp Feature Layer)
out_layer: Der Name des zu erstellenden Feature-Layers. Der neu erstellte Layer kann als Eingabe bei jedem beliebigen 
           Geoverarbeitungswerkzeug verwendet werden, für das Feature-Layer eingegeben werden können. 
           (Datentyp Feature Layer)

https://pro.arcgis.com/de/pro-app/latest/tool-reference/data-management/make-feature-layer.htm
'''

# cube = arcpy.stpm.CreateSpaceTimeCube(featureLayer, PSI.nc, time_field)

'''
arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field, {template_cube}, {time_step_interval},
                              {time_step_alignment}, {reference_time}, {distance_interval}, summary_fields,
                              {aggregation_shape_type}, {defined_polygon_locations}, {location_id})
                              
in_features: Die Eingabe-Punkt-Feature-Class, die zu Raum-Zeit-Abschnitten aggregiert werden soll.
             (Datentyp Feature Layer)
output_cube: Der zu erstellende Ausgabe-netCDF-Datenwürfel,
             der die Anzahl und Zusammenfassungen der Punktdaten von Eingabe-Features enthält. (Datentyp File)
time_field:  Das Feld mit Datums- und Uhrzeitangaben (Zeitstempel) für jeden Punkt.
             Dieses Feld muss vom Typ "Datum" sein. (Datentyp Field)                              
'''


            # Check and Create GDB
#            if not arcpy.Exists(os.path.join(root_dir, out_gdb)):
#               arcpy.management.CreateFileGDB(root_dir, 'shp2netCDF.gdb', 'CURRENT')

            # Check and Remove Feature Class
#            if arcpy.Exists(os.path.join(out_path, out_name)):
#                arcpy.Delete_management(out_name)

            # Save Feature Class to GDB
#            arcpy.conversion.FeatureClassToFeatureClass(in_features, out_path, out_name, '#', fms_out)
