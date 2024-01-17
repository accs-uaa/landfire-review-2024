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
landfire_input = os.path.join(project_folder, 'Data_Input/landfire_evt/LA16_EVT_200.tif')

# Define intermediate files
zones_intermediate = os.path.join(workspace_geodatabase, 'AlaskaYukon_VegetationZones_Intermediate')
zones_selected = os.path.join(workspace_geodatabase, 'AlaskaYukon_VegetationZones_Selected')
zones_raster = os.path.join(output_folder, 'AlaskaYukon_VegetationZones_50m_3338.tif')
zones_30m_preliminary = os.path.join(output_folder, 'zones_preliminary.tif')
biomes_30m_preliminary = os.path.join(output_folder, 'biomes_preliminary.tif')

# Define output files
zones_vector = os.path.join(project_geodatabase, 'AlaskaYukon_VegetationZones_3338')
zones_30m_output = os.path.join(output_folder, 'AlaskaYukon_VegetationZones_30m_3338.tif')
biomes_30m_output = os.path.join(output_folder, 'AlaskaYukon_Biomes_30m_3338.tif')


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
bvalue_dictionary = {1: 'Temperate',
                     2: 'Temperate-Boreal',
                     3: 'Boreal',
                     4: 'Boreal-Northern Maritime',
                     5: 'Northern Maritime',
                     6: 'Boreal-Arctic',
                     7: 'Arctic'}

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
code_block = get_attribute_code_block()

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
    zone_expression = f'get_response(!VALUE!, {zone_dictionary}, "value")'
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
    zone_expression = f'get_response(!gridcode!, {zone_dictionary}, "value")'
    zvalue_expression = f'get_response(!zone!, {zone_dictionary}, "key")'
    biome_expression = f'get_response(!gridcode!, {biome_dictionary}, "value")'
    bvalue_expression = f'get_response(!biome!, {bvalue_dictionary}, "key")'
    # Calculate zone label
    arcpy.management.CalculateField(zones_vector,
                                    'zone',
                                    zone_expression,
                                    'PYTHON3',
                                    code_block)
    # Calculate zone value
    arcpy.management.AddField(zones_vector,
                              'zvalue',
                              'LONG',
                              '',
                              '',
                              '',
                              '',
                              'NULLABLE',
                              'NON_REQUIRED',
                              '')
    arcpy.management.CalculateField(zones_vector,
                                    'zvalue',
                                    zvalue_expression,
                                    'PYTHON3',
                                    code_block)
    # Calculate biome label
    arcpy.management.CalculateField(zones_vector,
                                    'biome',
                                    biome_expression,
                                    'PYTHON3',
                                    code_block)
    # Calculate biome value
    arcpy.management.AddField(zones_vector,
                              'bvalue',
                              'LONG',
                              '',
                              '',
                              '',
                              '',
                              'NULLABLE',
                              'NON_REQUIRED',
                              '')
    arcpy.management.CalculateField(zones_vector,
                                    'bvalue',
                                    bvalue_expression,
                                    'PYTHON3',
                                    code_block)
    # Delete extraneous fields
    print('\tDeleting extraneous fields...')
    arcpy.management.DeleteField(zones_vector,
                                 ['zone', 'zvalue', 'biome', 'bvalue'],
                                 'KEEP_FIELDS')
    end_timing(iteration_start)

# Set snap raster and extent
arcpy.env.snapRaster = landfire_input
arcpy.env.extent = Raster(landfire_input).extent

# Set cell size environment
cell_size = arcpy.management.GetRasterProperties(landfire_input, 'CELLSIZEX', '').getOutput(0)
arcpy.env.cellSize = int(cell_size)

# Convert polygon to zones raster
if arcpy.Exists(zones_30m_output) == 0:
    print('Creating zones raster...')
    iteration_start = time.time()
    # Convert polygon to raster
    print('\tConverting polygon to raster...')
    arcpy.conversion.PolygonToRaster(zones_vector,
                                     'zvalue',
                                     zones_30m_preliminary,
                                     'CELL_CENTER',
                                     '',
                                     cell_size,
                                     'DO_NOT_BUILD')
    arcpy.management.CopyRaster(zones_30m_preliminary,
                                zones_30m_output,
                                '',
                                '',
                                '255',
                                'NONE',
                                'NONE',
                                '8_BIT_UNSIGNED',
                                'NONE',
                                'NONE',
                                'TIFF',
                                'NONE',
                                'CURRENT_SLICE',
                                'NO_TRANSPOSE')
    print('\tBuilding attribute table...')
    arcpy.management.BuildRasterAttributeTable(zones_30m_output, 'Overwrite')
    print('\tBuilding pyramids...')
    arcpy.management.BuildPyramids(zones_30m_output, -1, 'NONE', 'NEAREST',
                                   'LZ77', '', 'OVERWRITE')
    # Calculate attribute label field
    print('\tCreating attributes...')
    zone_expression = f'get_response(!VALUE!, {zone_dictionary}, "value")'
    arcpy.management.CalculateField(zones_30m_output,
                                    'zone',
                                    zone_expression,
                                    'PYTHON3',
                                    code_block)
    end_timing(iteration_start)

# Convert polygon to biomes raster
if arcpy.Exists(biomes_30m_output) == 0:
    print('Creating biomes raster...')
    iteration_start = time.time()
    # Convert polygon to raster
    print('\tConverting polygon to raster...')
    arcpy.conversion.PolygonToRaster(zones_vector,
                                     'bvalue',
                                     biomes_30m_preliminary,
                                     'CELL_CENTER',
                                     '',
                                     cell_size,
                                     'DO_NOT_BUILD')
    arcpy.management.CopyRaster(biomes_30m_preliminary,
                                biomes_30m_output,
                                '',
                                '',
                                '255',
                                'NONE',
                                'NONE',
                                '8_BIT_UNSIGNED',
                                'NONE',
                                'NONE',
                                'TIFF',
                                'NONE',
                                'CURRENT_SLICE',
                                'NO_TRANSPOSE')
    print('\tCalculating raster statistics...')
    arcpy.management.CalculateStatistics(biomes_30m_output)
    print('\tBuilding attribute table...')
    arcpy.management.BuildRasterAttributeTable(biomes_30m_output, 'Overwrite')
    print('\tBuilding pyramids...')
    arcpy.management.BuildPyramids(biomes_30m_output,
                                   -1,
                                   'NONE',
                                   'NEAREST',
                                   'LZ77',
                                   '',
                                   'OVERWRITE')
    # Calculate attribute label field
    print('\tCreating attributes...')
    biome_expression = f'get_response(!VALUE!, {bvalue_dictionary}, "value")'
    arcpy.management.CalculateField(biomes_30m_output,
                                    'biome',
                                    biome_expression,
                                    'PYTHON3',
                                    code_block)
    end_timing(iteration_start)

# Delete intermediate datasets
if arcpy.Exists(zones_intermediate) == 1:
    arcpy.management.Delete(zones_intermediate)
if arcpy.Exists(zones_selected) == 1:
    arcpy.management.Delete(zones_selected)
if arcpy.Exists(zones_30m_preliminary) == 1:
    arcpy.management.Delete(zones_30m_preliminary)
if arcpy.Exists(biomes_30m_preliminary) == 1:
    arcpy.management.Delete(biomes_30m_preliminary)
