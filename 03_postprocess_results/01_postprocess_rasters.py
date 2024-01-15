# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process landfire automated review
# Author: Timm Nawrocki
# Last Updated: 2023-05-31
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Post-process landfire automated review" creates attribute tables and pyramids.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from akutils import *
import arcpy

# Set round date
round_date = 'round_20240114'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
data_folder = os.path.join(drive,
                           root_folder,
                           'Projects/VegetationEcology/Landfire_BpS/Data')
work_geodatabase = os.path.join(data_folder, 'Landfire_BpS.gdb')
parsed_folder = os.path.join(data_folder, 'Data_Output/automated_checks')
output_folder = os.path.join(data_folder, 'Data_Output/final_rasters')

# Define input datasets
parsed_input = os.path.join(parsed_folder, round_date, 'AKVEG_Parsed_30m_3338.tif')

# Define dictionary of types for AKVEG parsed results
parsed_dictionary = {1: 'spruce-lichen woodland',
                     2: 'white spruce woodland',
                     3: 'white spruce-hardwood woodland',
                     4: 'black spruce woodland',
                     5: 'black spruce-hardwood woodland',
                     6: 'mixed spruce woodland',
                     7: 'mixed spruce-hardwood woodland',
                     8: 'white spruce forest',
                     9: 'black spruce forest',
                     10: 'mixed spruce forest',
                     11: 'white spruce-hardwood forest',
                     12: 'black spruce-hardwood forest',
                     13: 'mixed spruce-hardwood forest',
                     14: 'black spruce-tussock woodland',
                     15: 'black spruce peatland (or fen)',
                     16: 'deciduous trees',
                     17: 'alder',
                     18: 'low shrub-tussock tundra',
                     19: 'dwarf shrub-tussock tundra',
                     20: 'mesic alder-willow',
                     21: 'wet alder-willow',
                     22: 'mesic willow',
                     23: 'wet willow',
                     24: 'wet shrub-sedge',
                     25: 'mesic birch-willow',
                     26: 'wet birch-willow',
                     27: 'mesic birch shrub',
                     28: 'wet sedge meadow',
                     29: 'sphagnum peatland',
                     30: 'dwarf shrub-sphagnum',
                     31: 'lichen dominant or co-dominant',
                     32: 'dwarf shrub-lichen',
                     33: 'ericaceous (dryas) dwarf shrub',
                     34: 'dryas dwarf shrub',
                     35: 'herbaceous mix',
                     36: 'sparse',
                     37: 'barren',
                     253: 'retain original'}

# Post-process parsed results
print('Post-processing parsed foliar cover results...')
iteration_start = time.time()
print('\tCalculating statistics...')
arcpy.management.CalculateStatistics(parsed_input)
arcpy.management.BuildRasterAttributeTable(parsed_input, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
label_block = get_attribute_code_block()
label_expression = f'get_response(!VALUE!, {parsed_dictionary}, "value")'
arcpy.management.CalculateField(parsed_input,
                                'label',
                                label_expression,
                                'PYTHON3',
                                label_block)
# Build pyramids
print('\tBuilding pyramids...')
arcpy.management.BuildPyramids(parsed_input,
                               -1,
                               'NONE',
                               'NEAREST',
                               'LZ77',
                               '',
                               'OVERWRITE')
end_timing(iteration_start)
