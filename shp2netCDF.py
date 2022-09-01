# coding=utf-8

# ----------------------------------------------------------------------------------------------------------------------
# What is the purpose of this Python script?

# shp2netCDF.py imports the psi-shapefile into a Space-Time-Cube (NetCDF Format).
# Merges psi results in Time (1 year) and Space (250m).
# ----------------------------------------------------------------------------------------------------------------------

# Import of the required modules
import os
import arcpy
from datetime import datetime
import re

# TODO: Pfade im System ändern und im Code anpassen, keine Leer- oder Sonderzeichen verwenden
# Set directories
# Root Directory:
root_dir = r'C:\Users\Judith\Documents\Studium\1 - Bachelor of Science Geoinformatik\Bachelorarbeit\BA'
# Directory where the input shape files are stored:
shp_dir = os.path.join(root_dir, 'Daten\A015_D139_32400_5712_20141001_20201231_BA-Bresser_v02')
# Directory where the output geodatabase will be created:
out_gdb = os.path.join(root_dir, 'shp2netCDF.gdb')

# set arcgis workspace to folder and create empty list for the shapefiles in the input folder
arcpy.env.workspace = root_dir
shp_files = []

# searching for shapefiles (recursive) in the input folder, append to list
for root, dirs, files in os.walk(shp_dir):
    for file in files:
        if file.endswith(".shp") and "vertical" in file:
            # appends an element to the end of the list
            shp_files.append(os.path.join(root, file))

# Create a Field Mappings object
fms_shp = arcpy.FieldMappings()
# Adds a table to the Field Mappings object
fms_shp.addTable(shp_files[0])
# Notice: Works as long as only one table adds to the Field Mappings object.

# Loop through all attributes (columns)
fields = ["lat", "lon"]  
for field_idx in range(len(fms_shp.fields)):
    # Get current FieldMap
    field_map = fms_shp.getFieldMap(field_idx)
    # Get current Field
    field_outputField = field_map.outputField
    # Get current FieldName
    field_name = field_outputField.name

    # Search for date columns starting with "D_20*"
    if field_name.startswith('D_20'):
        fields.append(field_name)
    
voids = arcpy.da.FeatureClassToNumPyArray(shp_dir, fields)
feature_list = []
for void in voids:
    temp = []
        for x in void:
            temp.append(x)
    feature_list.append(temp)
array = np.asarray(feature_list)    
# Daten sind alle eingelesen und in einem Format in dem wir dies beliebig weiterverwenden können....
#TODO: array into Space-Time-Cube
    
'''     
# Run the Spatial Join tool, using the defaults for the join operation and join type
arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field, {template_cube}, {time_step_interval},
                              {time_step_alignment}, {reference_time}, {distance_interval}, summary_fields,
                              {aggregation_shape_type}, {defined_polygon_locations}, {location_id})
'''
