# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Prepare data for processing
# Author: Timm Nawrocki
# Last Updated: 2024-01-13
# Usage: Execute in Python 3.9+.
# Description: "Prepare data for processing" enforces a common grid, cell size, and extent on all raster input data.
# ---------------------------------------------------------------------------

# Import packages
import glob
import os
import time
from osgeo import gdal
from akutils import *

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
foliar_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/AKVEG_Map/Data',
                             'Data_Output/data_package/version_1.0_20210517')
output_folder = os.path.join(project_folder, 'Data_Input/akveg_foliar_30m')
intermediate_folder = os.path.join(project_folder, 'Data_Input/intermediate')

# Define input files
area_input = os.path.join(project_folder, 'Data_Input/NorthAmericanBeringia_v1_30m.tif')
landfire_input = os.path.join(project_folder, 'Data_Input/landfire_evt/LA16_EVT_200.tif')
zones_input = os.path.join(project_folder, 'Data_Output/zones/AlaskaYukon_VegetationZones_30m_3338.tif')

# Define output files
landfire_output = os.path.join(intermediate_folder, 'LA16_EVT_200.tif')
zones_output = os.path.join(intermediate_folder, 'AlaskaYukon_VegetationZones_30m_3338.tif')

# Define foliar cover input lists
species_list = ['alnus', 'betshr', 'bettre', 'dectre', 'dryas', 'empnig', 'erivag',
                'picgla', 'picmar', 'rhoshr', 'salshr', 'sphagn', 'vaculi', 'vacvit', 'wetsed']
pft_list = ['DeciduousShrub', 'EvergreenShrub', 'Forb', 'Graminoid', 'tmLichenLight']
pft_outnames = ['decshr', 'evrshr', 'forb', 'gramin', 'lichen']

# Calculate area bounds
area_bounds = raster_bounds(area_input)

# Process foliar cover species/aggregate input data in loop
for input_name in species_list:
    # Define input folder
    input_folder = os.path.join(foliar_folder, input_name, 'rasters')

    # Define output file
    foliar_output = os.path.join(output_folder, input_name + '_30m_3338.tif')

    # Define list of input files
    os.chdir(input_folder)
    file_list = glob.glob('*.tif')
    foliar_inputs = []
    for file in file_list:
        full_path = os.path.join(input_folder, file)
        foliar_inputs.append(full_path)

    # Merge tiles
    if os.path.exists(foliar_output) == 0:
        print(f'Merging {len(foliar_inputs)} tiles for {input_name}...')
        iteration_start = time.time()
        # Merge tiles
        gdal.Warp(foliar_output,
                  foliar_inputs,
                  srcSRS='EPSG:3338',
                  dstSRS='EPSG:3338',
                  outputType=gdal.GDT_Byte,
                  workingType=gdal.GDT_Byte,
                  xRes=30,
                  yRes=-30,
                  srcNodata=255,
                  dstNodata=255,
                  outputBounds=area_bounds,
                  resampleAlg='bilinear',
                  targetAlignedPixels=False,
                  creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
        end_timing(iteration_start)

# Process foliar cover species/aggregate input data in loop
count = 0
for input_name in pft_list:
    # Define input folder
    foliar_input = os.path.join(drive, root_folder,
                                'Data/biota/vegetation/Alaska_PFT_TimeSeries/projected_3338',
                                f'ABoVE_PFT_Top_Cover_{input_name}_2020_3338.tif')

    # Define output file
    foliar_output = os.path.join(output_folder, pft_outnames[count] + '_30m_3338.tif')

    # Merge tiles
    if os.path.exists(foliar_output) == 0:
        print(f'Warping {input_name}...')
        iteration_start = time.time()
        # Merge tiles
        gdal.Warp(foliar_output,
                  foliar_input,
                  srcSRS='EPSG:3338',
                  dstSRS='EPSG:3338',
                  outputType=gdal.GDT_Byte,
                  workingType=gdal.GDT_Byte,
                  xRes=30,
                  yRes=-30,
                  srcNodata=255,
                  dstNodata=255,
                  outputBounds=area_bounds,
                  resampleAlg='bilinear',
                  targetAlignedPixels=False,
                  creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
        end_timing(iteration_start)

    count += 1

# Process landfire input data
if os.path.exists(landfire_output) == 0:
    print(f'Standardizing Landfire EVT...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(landfire_output,
              landfire_input,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Int16,
              workingType=gdal.GDT_Int16,
              xRes=30,
              yRes=-30,
              srcNodata=32767,
              dstNodata=-32768,
              outputBounds=area_bounds,
              resampleAlg='near',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Process zones input data
if os.path.exists(zones_output) == 0:
    print(f'Standardizing Zones...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(zones_output,
              zones_input,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Byte,
              workingType=gdal.GDT_Byte,
              xRes=30,
              yRes=-30,
              srcNodata=255,
              dstNodata=255,
              outputBounds=area_bounds,
              resampleAlg='near',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)
