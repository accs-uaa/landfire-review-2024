# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert spruce extent to generalized vector
# Author: Timm Nawrocki
# Last Updated: 2023-12-12
# Usage: Execute in ArcGIS Pro Python 3.9+.
# Description: "Convert spruce extent to generalized vector" converts the raster spruce extent to a vector with generalization. NOTE: The spruce extent vector MUST be manually corrected after running this script.
# ---------------------------------------------------------------------------

# Import packages
import arcpy
from arcpy.sa import FocalStatistics
from arcpy.sa import NbrRectangle
from arcpy.sa import Raster
from arcpy.sa import SetNull
import os
import time
from akutils import *

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
ecoregion_input = os.path.join(project_folder, 'Data_Input/ecoregion_inputs')

# Define geodatabases
landfire_workspace = os.path.join(project_folder, 'Landfire_Workspace.gdb')

# Define input files
area_input = os.path.join(ecoregion_input, 'AlaskaYukon_MapDomain_10m_3338.tif')
watershed_input = os.path.join(ecoregion_input, 'Alaska_Watersheds_12Digit_3338.shp')
picea_input = os.path.join(ecoregion_input, 'Picea_Threshold_5_10m_3338.tif')

# Define intermediate files
rescale_output = os.path.join(ecoregion_input, 'Picea_Threshold_5_1000m_3338.tif')
polygon_output = os.path.join(landfire_workspace, 'Picea_Threshold_Polygon')
buffer_output = os.path.join(landfire_workspace, 'Picea_Threshold_Buffer_1000m')
dissolve_output = os.path.join(landfire_workspace, 'Picea_Threshold_Dissolve')

# Define output files
watershed_output = os.path.join(ecoregion_input, 'Alaska_Watersheds_12Digit_3338.tif')
zonal_output = os.path.join(ecoregion_input, 'Picea_ZonalSum_50m_3338.tif')

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
arcpy.env.workspace = landfire_workspace

# Rescale raster to 1000 m
if arcpy.Exists(rescale_output) == 0:
    print('Rescaling Picea raster...')
    iteration_start = time.time()
    focal_raster = FocalStatistics(picea_input, NbrRectangle(101, 101, 'CELL'), 'MEAN', 'DATA')
    con_raster = SetNull(focal_raster < 0.1, 1)
    arcpy.management.Resample(con_raster, rescale_output, '1000', 'NEAREST')
    end_timing(iteration_start)

# Convert resampled raster to polygon
if arcpy.Exists(polygon_output) == 0:
    print('Converting raster to polygon...')
    iteration_start = time.time()
    arcpy.conversion.RasterToPolygon(rescale_output,
                                     polygon_output,
                                     'SIMPLIFY',
                                     'VALUE',
                                     'SINGLE_OUTER_PART',
                                     '')
    end_timing(iteration_start)

# Buffer by 1000 m
if arcpy.Exists(buffer_output) == 0:
    print('Buffering Picea polygon...')
    iteration_start = time.time()
    arcpy.analysis.PairwiseBuffer(polygon_output,
                                  buffer_output,
                                  '1000 METERS',
                                  'NONE',
                                  '',
                                  'PLANAR',
                                  '')
    end_timing(iteration_start)

# Dissolve polygons
if arcpy.Exists(buffer_output) == 0:
    print('Buffering Picea polygon...')
    iteration_start = time.time()
    arcpy.analysis.PairwiseDissolve(buffer_output,
                                    dissolve_output,
                                    '',
                                    [['VALUE', 'SUM']],
                                    'SINGLE_PART',
                                    '')
    end_timing(iteration_start)

# Eliminate polygon parts less than 10000 sq km (surrounded)

