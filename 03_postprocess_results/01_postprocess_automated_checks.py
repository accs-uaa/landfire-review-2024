# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Post-process automated checks
# Author: Timm Nawrocki
# Last Updated: 2024-01-27
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Post-process automated checks" creates attribute tables and pyramids for rasters that result from the automated checks.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from akutils import *
import arcpy

# Set round date
round_date = 'round_20240125'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
work_geodatabase = os.path.join(project_folder, 'Landfire_BpS.gdb')
output_folder = os.path.join(project_folder, 'Data_Output/automated_checks')

# Define input datasets
parsed_input = os.path.join(output_folder, round_date, 'AKVEG_Parsed_30m_3338.tif')
evt_input = os.path.join(output_folder, round_date, 'AKVEG_Landfire_Combined_30m_3338.tif')
evt_color = os.path.join(output_folder, round_date, 'AKVEG_Landfire_Combined_30m_3338.tif.clr')

# Define attribute dictionaries
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
                     17: 'mesic alder',
                     18: 'wet alder',
                     19: 'low shrub-tussock tundra',
                     20: 'dwarf shrub-tussock tundra',
                     21: 'mesic alder-willow',
                     22: 'wet alder-willow',
                     23: 'mesic willow',
                     24: 'wet willow',
                     25: 'wet shrub-sphagnum',
                     26: 'mesic birch-willow',
                     27: 'wet birch-willow',
                     28: 'mesic birch shrub',
                     29: 'wet sedge meadow',
                     30: 'sphagnum peatland',
                     31: 'dwarf shrub-sphagnum',
                     32: 'lichen dominant or co-dominant',
                     33: 'dwarf shrub-lichen',
                     34: 'ericaceous (dryas) dwarf shrub',
                     35: 'dryas dwarf shrub',
                     36: 'herbaceous mix',
                     37: 'sparse',
                     38: 'barren',
                     253: 'no type assigned',
                     254: 'undistinguished spruce'}
landfire_dictionary = {1: 'no assignment',
                       255: 'not mapped',
                       4401: 'Alaska Arctic Coastal Sedge-Dwarf-Shrubland',
                       4404: 'Alaska Arctic Mesic Alder Shrubland',
                       4405: 'Alaska Arctic Permafrost Plateau Dwarf-Shrub Lichen Tundra',
                       4406: 'Alaska Arctic Tidal Flat',
                       4407: 'Alaska Sub-boreal and Maritime Alpine Mesic Herbaceous Meadow',
                       4408: 'Alaska Sub-boreal Mesic Subalpine Alder Shrubland',
                       4409: 'Alaska Sub-boreal Mountain Hemlock-White Spruce Forest',
                       4412: 'Alaskan Pacific Alpine-Subalpine Dwarf-shrubland and Heath',
                       4415: 'Alaskan Pacific Maritime Avalanche Slope Shrubland',
                       4416: 'Alaskan Pacific Maritime Coastal Meadow and Slough-Levee',
                       4417: 'Alaskan Pacific Maritime Mesic Herbaceous Meadow',
                       4418: 'Alaskan Pacific Maritime Mountain Hemlock-Shore Pine Peatland',
                       4419: 'Alaskan Pacific Maritime Western Hemlock Forest',
                       4420: 'Alaskan Pacific Mesic Western Hemlock-Yellow-cedar Forest',
                       4421: 'Alaskan Pacific Mountain Hemlock Forest and Subalpine Woodland',
                       4422: 'Alaskan Pacific Poorly Drained Conifer Woodland',
                       4423: 'Alaskan Pacific Sitka Spruce Forest and Beach Ridge',
                       4425: 'Alaskan Pacific-Aleutian Alder-Salmonberry-Copperbush Shrubland',
                       4426: 'Alaskan Pacific-Aleutian Coastal Dune, Beach, and Beach Meadow',
                       4427: 'Alaskan Pacific-Aleutian Fen and Wet Meadow',
                       4428: 'Alaskan Pacific-Aleutian Rocky Coastline and Sea Cliff',
                       4429: 'Aleutian Ericaceous Dwarf-shrubland, Heath, and Fell-field',
                       4430: 'Aleutian Mesic Herbaceous Meadow',
                       4431: 'Aleutian Mesic-Wet Willow Shrubland',
                       4432: 'Aleutian Volcanic Rock and Talus',
                       4434: 'North American Arctic Bedrock and Talus',
                       4435: 'North American Arctic Dryas Tundra',
                       4436: 'North American Arctic Dwarf-Shrub Lichen Tundra',
                       4437: 'North American Arctic Dwarf-shrub-Wet Sedge-Sphagnum Peatland',
                       4438: 'North American Arctic Freshwater Marsh',
                       4439: 'North American Arctic Lichen Tundra',
                       4440: 'North American Arctic Mesic Herbaceous Meadow',
                       4442: 'North American Arctic Mesic-Wet Low Willow Shrubland',
                       4444: 'North American Arctic Scrub Birch-Ericaceous Shrubland',
                       4445: 'North American Arctic Sparse Tundra',
                       4446: 'North American Arctic Wet Sedge Tundra and Polygonal Ground',
                       4448: 'North American Arctic-Subarctic Shrub-Tussock Tundra',
                       4449: 'North American Arctic-Subarctic Tidal Salt and Brackish Marsh',
                       4450: 'North American Arctic-Subarctic Tussock Tundra',
                       4453: 'Western North American Boreal Alpine Dwarf-shrubland',
                       4454: 'Western North American Boreal Alpine Mesic Herbaceous Meadow',
                       4456: 'Western North American Boreal Black Spruce Bog and Dwarf-Tree Peatland',
                       4458: 'Western North American Boreal Cliff, Scree, and Rock',
                       4459: 'Western North American Boreal Dry Aspen-Steppe Bluff',
                       4460: 'Western North American Boreal Dry Grassland',
                       4461: 'Western North American Boreal Freshwater Emergent Marsh',
                       4463: 'Western North American Boreal Mesic Birch-Aspen Forest',
                       4464: 'Western North American Boreal Mesic Bluejoint-Forb Meadow',
                       4465: 'Western North American Boreal Mesic Scrub Birch-Willow Shrubland',
                       4467: 'Western North American Boreal Mesic-Wet Black Spruce Forest and Woodland',
                       4471: 'Western North American Boreal Shrub Swamp',
                       4472: 'Western North American Boreal Shrub-Sedge Bog and Acidic Fen',
                       4474: 'Western North American Boreal Spruce-Lichen Woodland',
                       4476: 'Western North American Boreal Wet Black Spruce-Tussock Woodland',
                       4477: 'Western North American Boreal Wet Meadow',
                       4479: 'Western North American Boreal Treeline White Spruce-Hardwood Woodland',
                       4481: 'Western North American Boreal Mesic White Spruce-Hardwood Forest',
                       4483: 'Alaska Sub-boreal White-Lutz Spruce-Hardwood Forest and Woodland',
                       4911: 'Alaskan Pacific Acidic Shrub-Sedge Peatland',
                       4947: 'North American Arctic-Subarctic Coastal Dune and Beach',
                       7178: 'North Pacific Hypermaritime Western Red-cedar-Western Hemlock Forest',
                       7191: 'Recently Logged-Herb and Grass Cover',
                       7192: 'Recently Logged-Shrub Cover',
                       7193: 'Recently Logged-Tree Cover',
                       7195: 'Recently Burned-Herb and Grass Cover',
                       7196: 'Recently Burned-Shrub Cover',
                       7197: 'Recently Burned-Tree Cover',
                       7198: 'Recently Disturbed Other-Herb and Grass Cover',
                       7199: 'Recently Disturbed Other-Shrub Cover',
                       7292: 'Open Water',
                       7295: 'Quarries-Strip Mines-Gravel Pits-Well and Wind Pads',
                       7296: 'Developed-Low Intensity',
                       7297: 'Developed-Medium Intensity',
                       7298: 'Developed-High Intensity',
                       7299: 'Developed-Roads',
                       7300: 'Developed-Open Space',
                       7662: 'Temperate Pacific Freshwater Emergent Marsh',
                       7663: 'North Pacific Shrub Swamp',
                       7668: 'Temperate Pacific Tidal Salt and Brackish Marsh',
                       7669: 'Temperate Pacific Intertidal Flat',
                       7733: 'North Pacific Montane Massive Bedrock, Cliff, and Talus',
                       7735: 'North American Glacier and Ice Field',
                       7737: 'North American Glacial Outwash',
                       7754: 'Agriculture-Pasture and Hay',
                       7755: 'Agriculture-Cultivated Crops and Irrigated Agriculture',
                       10004: 'Western North American Boreal Mixed Spruce-Hardwood Forest & Woodland',
                       10005: 'Western North American Boreal Mesic Alder Shrubland'}

# Retrieve attribute code block
label_block = get_attribute_code_block()

# Post-process parsed foliar cover results
print('Post-processing parsed foliar cover results...')
iteration_start = time.time()
print('\tCalculating statistics...')
arcpy.management.CalculateStatistics(parsed_input)
arcpy.management.BuildRasterAttributeTable(parsed_input, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
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

# Post-process parsed evt results
print('Post-processing parsed evt results...')
iteration_start = time.time()
print('\tCalculating statistics...')
arcpy.management.CalculateStatistics(evt_input)
arcpy.management.BuildRasterAttributeTable(evt_input, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
label_expression = f'get_response(!VALUE!, {landfire_dictionary}, "value")'
arcpy.management.CalculateField(evt_input,
                                'EVT_NAME',
                                label_expression,
                                'PYTHON3',
                                label_block)
# Build pyramids
print('\tBuilding pyramids...')
arcpy.management.BuildPyramids(evt_input,
                               -1,
                               'NONE',
                               'NEAREST',
                               'LZ77',
                               '',
                               'OVERWRITE')
end_timing(iteration_start)
