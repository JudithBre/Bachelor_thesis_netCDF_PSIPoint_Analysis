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

#for shp_file in shp_files:

    # Get FieldMappings from current shape file
    fms_shp = arcpy.FieldMappings()
    print("Get FieldMappings from current shape file")
    # Adds a table to the field mappings object.
    fms_shp.addTable(shp_files[0])
    # TODO: Works as long as only one table is passed to the FieldMappings object to work with.

    print("A table has been added to the FieldMappings object." + "\n")
    #print(fms_shp)
    #print()

    # get field index (fi)
    # Find a field map within the field mappings by name.
    # Return value: Integer, the index position of the field map.
    fi_lon = fms_shp.findFieldMapIndex("lon")
    print("field index for lon:")
    print(fi_lon)
    fi_lat = fms_shp.findFieldMapIndex("lat")

    print(fi_lat)
    print()

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
# Test access to the attributes (optional)
# The attributes correspond to the column headers in my shapefile.
# ----------------------------------------------------------------------------------------------------------------------
    print("Test access to attributes now:")
    fID = fms_shp.findFieldMapIndex("FID")
    print(fID)
    shape = fms_shp.findFieldMapIndex("Shape")
    print(shape)
    velocity = fms_shp.findFieldMapIndex("Velocity")
    print(velocity)
    vprecision = fms_shp.findFieldMapIndex("Vprecision")
    print(vprecision)
    dEM = fms_shp.findFieldMapIndex("DEM")
    print(dEM)
    print("Test finished." + "\n")
    # TODO: Why do the FID and Shape attributes have the same index?!

# ----------------------------------------------------------------------------------------------------------------------
# Loop through all attributes (columns)
# ----------------------------------------------------------------------------------------------------------------------
    print("Loop through all attributes (columns)")
    print("Attribute count: ")
    print(len(fms_shp.fields))
    print()
    print("Loop starts now:")
    zaehler = 0
    for field_idx in range(len(fms_shp.fields)):
        # Get current FieldMap
        field_map = fms_shp.getFieldMap(field_idx)
        # Get current Field
        field_outputField = field_map.outputField
        # Get current FieldName
        field_name = field_outputField.name
        print("Get current FieldName:")
        print(field_name)
        zaehler = zaehler + 1
        print("current attribute:" + str(zaehler))

        # Search for date columns starting with "D_20*"
        if field_name.startswith('D_20'):
            print(field_name + " (starts with D_20*)")

            # Get FieldMap from Shapefile at current Field Index
            fm_dH = fms_shp.getFieldMap(field_idx)
            fm_dH.addInputField(fms_shp.getFieldMap(field_idx), 'dH')
            fm_dH.outputField.name = 'dH'
            fm_dH.outputField.aliasName = 'delta Height'
            # TODO: For some reason, all values in 'dH' becoming 0

            # Create new FieldMappings Object for Output Feature Class
            fms_out = arcpy.FieldMappings()

            # Fill Output Feature Class with 'lat' and 'lon' for every Date-Column, add FieldMaps to FieldMappings()
            fms_out.addFieldMap(fm_lon)
            fms_out.addFieldMap(fm_lat)
#            fms_out.addFieldMap(fm_dH)
#            print(fms_out)

            # TODO: Get Date String from FieldName and modify to Datetime ('yyyy/mm/dd hh:mm:ss')
            # TODO: Create new 'Datetime' Field
            # TODO: Fill new Field with Datetime Value
            '''
            field_date = "date"
            with arcpy.da.UpdateCursor(fms_shp, [field_date]) as rows:
                for row in rows:
                    rows.updateRow([datetime.date.today()])

            arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale},
                                      {field_length}, {field_alias}, {field_is_nullable}, {field_is_required},
                                      {field_domain})
            '''

            # Prepare Output Names
#            shp_name = shp_file.split('\\')[-1]
#            shp_name = shp_name.split('.shp')[0]
#            date_name = field_name.split('D_')[1]

            # Set Parameter for 'FeatureClassToFeatureClass'
#            in_features = shp_file
#            out_path = os.path.join(root_dir, out_gdb)
#            out_name = shp_name + "_" + date_name

            # Check and Create GDB
#            if not arcpy.Exists(os.path.join(root_dir, out_gdb)):
#               arcpy.management.CreateFileGDB(root_dir, 'shp2netCDF.gdb', 'CURRENT')

            # Check and Remove Feature Class
#            if arcpy.Exists(os.path.join(out_path, out_name)):
#                arcpy.Delete_management(out_name)

            # Save Feature Class to GDB
#            arcpy.conversion.FeatureClassToFeatureClass(in_features, out_path, out_name, '#', fms_out)

        '''
        # Run the Spatial Join tool, using the defaults for the join operation and join type
        arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field, {template_cube}, {time_step_interval},
                                       {time_step_alignment}, {reference_time}, {distance_interval}, summary_fields,
                                       {aggregation_shape_type}, {defined_polygon_locations}, {location_id})
        '''
