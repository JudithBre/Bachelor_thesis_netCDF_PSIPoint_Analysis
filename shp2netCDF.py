# coding=utf-8

# ----------------------------------------------------------------------------------------------------------------------
# What is the purpose of this Python script?
# ----------------------------------------------------------------------------------------------------------------------
# shp2netCDF.py imports the psi-shapefile into a Space-Time-Cube (NetCDF Format).
# Merges psi results in Time (1 year) and Space (250m).

# ----------------------------------------------------------------------------------------------------------------------
# Import of the required modules
# ----------------------------------------------------------------------------------------------------------------------
import os
print("os has been imported")
import arcpy
print("arcpy has been imported" + "\n")

from datetime import datetime
import re

# ----------------------------------------------------------------------------------------------------------------------
# directories
# ----------------------------------------------------------------------------------------------------------------------
# Root Directory:
root_dir = r'C:\Users\Judith\Documents\Studium\1 - Bachelor of Science Geoinformatik\Bachelorarbeit\BA'
print("Root Directory: " + root_dir)
# Directory where the input shape files are stored:
shp_dir = os.path.join(root_dir, 'Daten\A015_D139_32400_5712_20141001_20201231_BA-Bresser_v02')
print("Directory input shape files are stored: " + shp_dir)
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
# You can use the ArcPy classes Field Mappings and Field Map to get the field maps for a specific index.
# ----------------------------------------------------------------------------------------------------------------------
    # Create a Field Mappings object
    fms_shp = arcpy.FieldMappings()
    # Adds a table to the Field Mappings object
    fms_shp.addTable(shp_files[0])
    print("A table has been added to the FieldMappings object." + "\n")
    print(fms_shp)
    print()
    # Notice: Works as long as only one table adds to the Field Mappings object.

    # get field index (fi)
    # Find a field map within the field mappings by name.
    # Return value: Integer, the index position of the field map.
    fi_lon = fms_shp.findFieldMapIndex("lon")
    print("field index for lon:")
    print(fi_lon)
    fi_lat = fms_shp.findFieldMapIndex("lat")
    print("field index for lat:")
    print(fi_lat)

    # get field map (fm) of field index (fi)
    # Return value: FieldMap, the FieldMap object from the FieldMappings object.
    fm_lon = fms_shp.getFieldMap(fi_lon)
    print("get field map (fm) of field index (fi_lon):")
    print(fm_lon)
    fm_lat = fms_shp.getFieldMap(fi_lat)
    print("get field map (fm) of field index (fi_lat):")
    print(fm_lat)
    print()

# ----------------------------------------------------------------------------------------------------------------------
# Loop through all attributes (columns)
# ----------------------------------------------------------------------------------------------------------------------
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
    
    voids = arcpy.da.FeatureClassToNumPyArray(shapedateiParameter, fields)
    list = []
    for void in voids:
        
    
        '''
           
       
        # Run the Spatial Join tool, using the defaults for the join operation and join type
        arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field, {template_cube}, {time_step_interval},
                                       {time_step_alignment}, {reference_time}, {distance_interval}, summary_fields,
                                       {aggregation_shape_type}, {defined_polygon_locations}, {location_id})
        '''
