# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert vegetation zones to generalized vector
# Author: Timm Nawrocki
# Last Updated: 2023-12-12
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Convert vegetation zones to generalized vector" converts the vegetation zone raster to a finalized raster and a vector.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
from arcpy.sa import Expand
from arcpy.sa import ExtractByAttributes
from arcpy.sa import Nibble
from arcpy.sa import Raster
from arcpy.sa import RegionGroup
from arcpy.sa import SetNull
import os
import time
from akutils import *

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
ecoregion_folder = os.path.join(project_folder, 'Data_Input/ecoregion_inputs')
output_folder = os.path.join(project_folder, 'Data_Output/zones')

# Define geodatabases
project_geodatabase = os.path.join(project_folder, 'Landfire_BpS.gdb')
workspace_geodatabase = os.path.join(project_folder, 'Landfire_Workspace.gdb')

# Define input files
area_input = os.path.join(ecoregion_folder, 'AlaskaYukon_MapDomain_50m_3338.tif')
zones_input = os.path.join(ecoregion_folder, 'intermediate/AlaskaYukon_VegetationZones_50m_3338.tif')

# Define intermediate files
zones_intermediate = os.path.join(workspace_geodatabase, 'AlaskaYukon_VegetationZones_Intermediate')
zones_selected = os.path.join(workspace_geodatabase, 'AlaskaYukon_VegetationZones_Selected')

# Define output files
zones_raster = os.path.join(output_folder, 'AlaskaYukon_VegetationZones_50m_3338.tif')
zones_vector = os.path.join(project_geodatabase, 'AlaskaYukon_VegetationZones_3338')

# Define zone dictionary
zone_dictionary = {1: 'Alaska-Canada Temperate North Pacific',
                   2: 'Alaska-Canada Temperate-Boreal Transition',
                   3: 'Alaska-Canada Boreal Southern',
                   4: 'Alaska-Yukon Boreal Central',
                   5: 'Alaska-Yukon Boreal Northern',
                   6: 'Alaska Boreal Western',
                   7: 'Alaska Boreal Southwest',
                   8: 'Alaska Boreal-Northern Maritime Transition',
                   9: 'Alaska North Pacific-Bering Maritime',
                   10: 'Alaska Boreal-Arctic Transition Southwest',
                   11: 'Alaska Arctic Western',
                   12: 'Alaska-Yukon Arctic Northern'}
biome_dictionary = {1: 'Temperate',
                    2: 'Temperate-Boreal',
                    3: 'Boreal',
                    4: 'Boreal',
                    5: 'Boreal',
                    6: 'Boreal',
                    7: 'Boreal',
                    8: 'Boreal-Northern Maritime',
                    9: 'Northern Maritime',
                    10: 'Boreal-Arctic',
                    11: 'Arctic',
                    12: 'Arctic'}

# Set overwrite option
arcpy.env.overwriteOutput = True

# Specify core usage
arcpy.env.parallelProcessingFactor = "75%"

# Set snap raster and extent
arcpy.env.snapRaster = area_input
arcpy.env.extent = Raster(area_input).extent

# Set cell size environment
cell_size = arcpy.management.GetRasterProperties(area_input, 'CELLSIZEX', '').getOutput(0)
arcpy.env.cellSize = int(cell_size)

# Set environment workspace
arcpy.env.workspace = workspace_geodatabase

# Define code block
code_block = '''def get_attribute(test, dictionary):
                for response, output in dictionary.items():
                    if test == response:
                        return output'''

# Create raster attributes
if arcpy.Exists(zones_raster) == 0:
    print('Post-processing raster...')
    iteration_start = time.time()
    print('\tExpanding raster zones against Boreal Southwest...')
    expand_initial = Expand(zones_input, 1, [4, 5, 6, 11, 12], 'MORPHOLOGICAL')
    print('\tExpanding raster zones against Boreal Western...')
    expand_final = Expand(expand_initial, 1, [5, 11, 12], 'MORPHOLOGICAL')
    print('\tCalculating contiguous value areas...')
    raster_regions = RegionGroup(expand_final,
                                 'FOUR',
                                 'WITHIN',
                                 'NO_LINK',
                                 '')
    print('\tRemoving contiguous areas below minimum mapping unit...')
    criteria = 'COUNT > 120000'
    raster_mask = ExtractByAttributes(raster_regions, criteria)
    print('\tReplacing removed data...')
    raster_nibble = Nibble(expand_final,
                           raster_mask,
                           'ALL_VALUES',
                           'PRESERVE_NODATA')
    print('\tExporting expanded raster...')
    arcpy.management.CopyRaster(raster_nibble,
                                zones_raster,
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
    print('\tCalculating raster statistics...')
    arcpy.management.CalculateStatistics(zones_raster)
    print('\tBuilding attribute table...')
    arcpy.management.BuildRasterAttributeTable(zones_raster, 'Overwrite')
    print('\tBuilding pyramids...')
    arcpy.management.BuildPyramids(zones_raster, -1, 'NONE', 'NEAREST',
                                   'LZ77', '', 'OVERWRITE')
    # Calculate attribute label field
    print('\tCreating attributes...')
    zone_expression = f'get_label(!VALUE!, {zone_dictionary})'
    arcpy.management.CalculateField(zones_raster,
                                    'zone',
                                    zone_expression,
                                    'PYTHON3',
                                    code_block)
    end_timing(iteration_start)

# Convert raster to polygon
if arcpy.Exists(zones_vector) == 0:
    print('Post-processing polygon...')
    iteration_start = time.time()
    print('\tConverting raster to polygon...')
    arcpy.conversion.RasterToPolygon(zones_raster,
                                     zones_vector,
                                     'SIMPLIFY',
                                     'VALUE',
                                     'SINGLE_OUTER_PART',
                                     '')
    # Calculate attribute label field
    print('\tBuilding attributes...')
    arcpy.management.DeleteField(zones_vector, ['Id'], 'DELETE_FIELDS')
    zone_expression = f'get_attribute(!gridcode!, {zone_dictionary})'
    arcpy.management.CalculateField(zones_vector,
                                    'zone',
                                    zone_expression,
                                    'PYTHON3',
                                    code_block)
    biome_expression = f'get_attribute(!gridcode!, {biome_dictionary})'
    arcpy.management.CalculateField(zones_vector,
                                    'biome',
                                    biome_expression,
                                    'PYTHON3',
                                    code_block)
    end_timing(iteration_start)
