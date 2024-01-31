# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process pixel change raster
# Author: Timm Nawrocki
# Last Updated: 2024-01-30
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Post-process pixel change raster" assigns attributes, calculates statistics, and builds pyramids for the pixel change raster.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from akutils import *
import arcpy

# Set version
version = 'v1.0_20240126'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
output_folder = os.path.join(project_folder,
                             'Data_Output/data_package/data_package_' + version,
                             'Data_Output/final_rasters')

# Define input datasets
status_input = os.path.join(output_folder, 'Landfire_EVT_Status_30m_3338.tif')

# Define attribute dictionaries
status_dictionary = {1: 'no change',
                     2: 'mapped type changed',
                     3: 'ecological systems changed',
                     4: 'floodplains removed',
                     5: 'manual review required'}

# Retrieve attribute code block
label_block = get_attribute_code_block()

# Post-process status results
print('Post-processing status results...')
iteration_start = time.time()
print('\tCalculating statistics...')
arcpy.management.CalculateStatistics(status_input)
arcpy.management.BuildRasterAttributeTable(status_input, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
label_expression = f'get_response(!VALUE!, {status_dictionary}, "value")'
arcpy.management.CalculateField(status_input,
                                'EVT_NAME',
                                label_expression,
                                'PYTHON3',
                                label_block)
# Build pyramids
print('\tBuilding pyramids...')
arcpy.management.BuildPyramids(status_input,
                               -1,
                               'NONE',
                               'NEAREST',
                               'LZ77',
                               '',
                               'OVERWRITE')
end_timing(iteration_start)
