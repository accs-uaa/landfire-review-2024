# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Enforce minimum mapping unit
# Author: Timm Nawrocki
# Last Updated: 2024-01-28
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Enforce minimum mapping unit" removes and replaces map units less than 1 acre in area.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from akutils import *
import arcpy
from arcpy.sa import Con
from arcpy.sa import ExtractByAttributes
from arcpy.sa import ExtractByMask
from arcpy.sa import Nibble
from arcpy.sa import Raster
from arcpy.sa import RegionGroup
from arcpy.sa import SetNull

# Set round date
round_date = 'round_20240125'
version = 'v1.0_20240126'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
work_geodatabase = os.path.join(project_folder, 'Landfire_BpS.gdb')
input_folder = os.path.join(project_folder, 'Data_Output/final_rasters')
output_folder = os.path.join(project_folder, 'Data_Output/data_package/data_package_' + version, 'Data_Output/final_rasters')

# Define workspace geodatabase
workspace_geodatabase = os.path.join(project_folder, 'Landfire_Workspace.gdb')

# Define input datasets
area_input = os.path.join(project_folder, 'Data_Input/Landfire_Domain_30m_3338.tif')
revised_input = os.path.join(input_folder, round_date, 'Landfire_EVT_Revised_30m_3338.tif')

# Define output datasets
region_output = os.path.join(input_folder, round_date, 'region_output.tif')
mask_output = os.path.join(input_folder, round_date, 'mask_output.tif')
nibble_output = os.path.join(input_folder, round_date, 'nibble_output.tif')
revised_output = os.path.join(output_folder, 'Landfire_EVT_Revised_30m_3338.tif')

# Define attribute dictionaries
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

# Set overwrite option
arcpy.env.overwriteOutput = True

# Specify core usage
arcpy.env.parallelProcessingFactor = '0'

# Set workspace
arcpy.env.workspace = workspace_geodatabase

# Set snap raster and extent
arcpy.env.snapRaster = area_input
arcpy.env.extent = Raster(area_input).extent

# Set output coordinate system
arcpy.env.outputCoordinateSystem = Raster(area_input)

# Set cell size environment
cell_size = arcpy.management.GetRasterProperties(area_input, 'CELLSIZEX', '').getOutput(0)
arcpy.env.cellSize = int(cell_size)

# Enforce MMU
print('Enforcing minimum mapping unit...')
iteration_start = time.time()
# Calculate regions
print('\tCalculating contiguous value areas...')
revised_raster = Raster(revised_input)
region_initial = RegionGroup(revised_raster,
                             'EIGHT',
                             'WITHIN',
                             'NO_LINK')
print('\tExporting region raster...')
arcpy.management.CopyRaster(region_initial,
                            region_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '32_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(region_output)
# Create mask
print('\tCalculating mask...')
criteria = f'COUNT > 1'
mask_1 = ExtractByAttributes(region_initial, criteria)
mask_2 = SetNull((revised_raster == 7292) | (revised_raster == 7296) | (revised_raster == 7297)
                 | (revised_raster == 7298) | (revised_raster == 7299) | (revised_raster == 7300),
                 mask_1)
print('\tExporting mask raster...')
mask_export = Con(mask_2 >= 32767, 32767, mask_2)
arcpy.management.CopyRaster(mask_export,
                            mask_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '16_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(mask_output)
# Replace removed data
print('\tReplacing contiguous areas below minimum mapping unit...')
nibble_initial = Nibble(revised_raster,
                        mask_2,
                        'DATA_ONLY',
                        'PROCESS_NODATA')
# Export nibble raster
print('\tExporting modified raster...')
arcpy.management.CopyRaster(nibble_initial,
                            nibble_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '16_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(nibble_output)
# Add removed data
print('\tReplacing removed values for linear features...')
replace_raster = Con((revised_raster == 7292) | (revised_raster == 7296) | (revised_raster == 7297)
                     | (revised_raster == 7298) | (revised_raster == 7299) | (revised_raster == 7300),
                     revised_raster, nibble_initial)
# Extract raster to study area
print('\tExtracting raster to Landfire domain...')
extract_raster = ExtractByMask(replace_raster, area_input)
# Export modified raster
print('\tExporting modified raster...')
arcpy.management.CopyRaster(extract_raster,
                            revised_output,
                            '',
                            '',
                            '-32768',
                            'NONE',
                            'NONE',
                            '16_BIT_SIGNED',
                            'NONE',
                            'NONE',
                            'TIFF',
                            'NONE',
                            'CURRENT_SLICE',
                            'NO_TRANSPOSE')
arcpy.management.CalculateStatistics(revised_output)
arcpy.management.BuildRasterAttributeTable(revised_output, 'Overwrite')
# Calculate attribute label field
print('\tBuilding attribute table...')
label_expression = f'get_response(!VALUE!, {landfire_dictionary}, "value")'
arcpy.management.CalculateField(revised_output,
                                'label',
                                label_expression,
                                'PYTHON3',
                                label_block)
# Build pyramids
print('\tBuilding pyramids...')
arcpy.management.BuildPyramids(revised_output,
                               -1,
                               'NONE',
                               'NEAREST',
                               'LZ77',
                               '',
                               'OVERWRITE')
end_timing(iteration_start)
