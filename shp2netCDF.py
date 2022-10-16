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

# ----------------------------------------------------------------------------------------------------------------------
# directories
# ----------------------------------------------------------------------------------------------------------------------
# Root Directory:
root_dir = r'C:\Users\Judith\Documents\Studium\1_Bachelor_of_Science_Geoinformatik\Bachelorarbeit\BA'
# print("Root Directory: " + root_dir)
# Directory where the input shape files are stored:
shp_dir = os.path.join(root_dir, 'Daten\A015_D139_32400_5712_20141001_20201231_BA-Bresser_v02')
# print("Directory input shape files are stored: " + shp_dir)
# print(os.listdir(shp_dir))
# Directory where the output geodatabase will be created:
out_gdb = os.path.join(root_dir, "shp2netCDF.gdb")
# print("Directory output geodatabase will be created: " + out_gdb + "\n")

# ----------------------------------------------------------------------------------------------------------------------
# set arcgis workspace to folder and
# create empty list for the shapefiles in the input folder
# ----------------------------------------------------------------------------------------------------------------------
arcpy.env.workspace = root_dir
# print("set arcgis workspace to folder has been done")
shp_files = []
# print(shp_files)
# print("empty list for the shapefiles were produced")

# ----------------------------------------------------------------------------------------------------------------------
# searching for shapefiles (recursive) in the input folder, append to list
# ----------------------------------------------------------------------------------------------------------------------
# print("searching for shapefiles (recursive) in the input folder")
for root, dirs, files in os.walk(shp_dir):
    for file in files:
        if file.endswith(".shp") and "vertical" in file:
            # appends an element to the end of the list
            shp_files.append(os.path.join(root, file))
            # print("An item has been added to the list.")
            # print(shp_files)
            # print()

# ----------------------------------------------------------------------------------------------------------------------
# You can use the ArcPy class Field Mappings
# ----------------------------------------------------------------------------------------------------------------------
# Create a Field Mappings object
fms_shp = arcpy.FieldMappings()
# print("Create Field Mappings Object")
# Adds a table to the Field Mappings object
fms_shp.addTable(shp_files[0])
# print("A table has been added to the FieldMappings object." + "\n")
# print(fms_shp)
# Notice: Works as long as only one table adds to the Field Mappings object.

# ----------------------------------------------------------------------------------------------------------------------
# Loop through all attributes (columns)
# ----------------------------------------------------------------------------------------------------------------------
# print("Loop through all attributes (columns)")
# print("Attribute count: ")
# print(len(fms_shp.fields))
# print()
# print("Loop starts now:")
# zaehler = 0
fields = ["lat", "lon"]
# print(fields)
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
# print(fields)

'''
Function FeatureClassToNumPyArray(in_table, field_names) converts a feature class 
into a numpy array
Parameters
- in_table: The feature class, layer, table or table view (data type: string)
- field_names: A list (or tuple) of field names (data type: string)
Source
https://pro.arcgis.com/en/pro-app/latest/arcpy/data-access/featureclasstonumpyarray.htm
'''
# save the file path to the shapefile feature class, data type: String
featureClass = os.path.join(shp_dir, "A015_D139_32400_5712_20141001_20201231_BA-Bresser_v02_decomposed_vertical.shp")
# Conversion of the list "fields" with the attribute names into the data type String
stringFields = "".join(fields)
# As required, the function now receives inputs in the form of a string as parameters
print("Start with the process FeatureClassToNumpyArray")
numpyArray = arcpy.da.FeatureClassToNumPyArray(featureClass, fields)
print("Process FeatureClassToNumpyArray finished")
df = pd.DataFrame(numpyArray)
print(df)
print()
df.info()

feature_list = []
for step in numpyArray:
    temp = []
    for x in step:
        temp.append(x)
    feature_list.append(temp)
    # print(step)
array = np.asarray(feature_list)
print(array)

'''
Function NumPyArrayToFeatureClass (in_array, out_table, shape_fields, {spatial_reference}) 
converts a structured NumPy array into a point feature class.
Parameters
- in_array: A structured NumPy array (data type: NumPyArray).
- out_table: The output point feature class to which the records from the NumPy array will be written 
             (data type: String).
- shape_fields: A list (or tuple) of field names used to create the 
                feature class' geometry. 
                Coordinates are specified in the order of x, y, z, and m. z-coordinate 
                and m-value fields are optional.
Source
https://pro.arcgis.com/de/pro-app/latest/arcpy/data-access/numpyarraytofeatureclass.htm
'''
#numpyArray_to_fc = arcpy.da.NumPyArrayToFeatureClass(array, "numpyArray_to_fc", ("x", "y", "z", "lat", "lon"))
#print(numpyArray_to_fc)

'''
Function arcpy.management.MakeFeatureLayer(in_features, out_layer)  
creates a Feature-Layer
Parameters
- in_features: The input feature class or layer from which the new layer is created. 
               Complex feature classes such as annotation and dimension feature classes 
               are not allowed as inputs. (Data type: Feature Layer)
- out_layer: The name of the feature layer to be created. 
             The newly created layer can be used as an input to any geoprocessing tool for 
             which feature layers can be entered. (Data type: Feature Layer)
Source
https://pro.arcgis.com/de/pro-app/latest/tool-reference/data-management/
make-feature-layer.htm
'''
# featureLayer =  arcpy.management.MakeFeatureLayer(numpyArray_to_fc, featureLayer)

'''
Function arcpy.stpm.CreateSpaceTimeCube(in_features, output_cube, time_field) 
creates a space-time cube
Parameters
- in_features: The input point feature class to aggregate to space-time sections. 
               (Data type: Feature layer)
- output_cube: The output netCDF data cube to be created,
               which contains the number and summaries of point data from input features. 
               (Data type: File)
- time_field:  The field containing date and time information (timestamp) for each point.
               This field must be of type "Date". (Data type: Field)
Source
https://desktop.arcgis.com/de/arcmap/10.3/tools/space-time-pattern-mining-toolbox/
create-space-time-cube.htm
'''
# cube = arcpy.stpm.CreateSpaceTimeCube(featureLayer, PSI.nc, time_field)