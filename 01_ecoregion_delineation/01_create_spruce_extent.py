# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert Picea foliar cover to spruce extent
# Author: Timm Nawrocki
# Last Updated: 2023-12-12
# Usage: Execute in Python 3.9+.
# Description: "Convert Picea foliar cover to spruce extent" combines the cover maps for Picea glauca and Picea mariana, thresholds them, and rescales the output data.
# ---------------------------------------------------------------------------

# Import packages
import glob
import os
import time
import numpy as np
import rasterio
from osgeo import gdal
from akutils import *

# Set nodata value
nodata = 255

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
foliar_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/AKVEG_Map/Data',
                             'Data_Output/data_package/version_1.0_20210517')
ecoregion_input = os.path.join(project_folder, 'Data_Input/ecoregion_inputs')
picgla_folder = os.path.join(foliar_folder, 'picgla/rasters')
picmar_folder = os.path.join(foliar_folder, 'picmar/rasters')

# Define input files
area_input = os.path.join(ecoregion_input, 'AlaskaYukon_MapDomain_10m_3338.tif')
watershed_input = os.path.join(ecoregion_input, 'Alaska_Watersheds_12Digit_3338.shp')

# Define list of Picea glauca files
os.chdir(picgla_folder)
picgla_files = glob.glob('*.tif')
picgla_list = []
for file in picgla_files:
    full_path = os.path.join(picgla_folder, file)
    picgla_list.append(full_path)

# Define list of Picea mariana files
os.chdir(picmar_folder)
picmar_files = glob.glob('*.tif')
picmar_list = []
for file in picmar_files:
    full_path = os.path.join(picmar_folder, file)
    picmar_list.append(full_path)

# Define output files
picgla_output = os.path.join(ecoregion_input, 'Picea_glauca_10m.tif')
picmar_output = os.path.join(ecoregion_input, 'Picea_mariana_10m.tif')
threshold_output = os.path.join(ecoregion_input, 'Picea_Threshold_5_10m_3338.tif')
picea_output = os.path.join(ecoregion_input, 'Picea_Threshold_5_50m_3338.tif')
area_output = os.path.join(ecoregion_input, 'AlaskaYukon_MapDomain_50m_3338.tif')

# Calculate area bounds
area_bounds = raster_bounds(area_input)

# Merge tiles for Picea glauca
if os.path.exists(picgla_output) == 0:
    print(f'Merging {len(picgla_files)} tiles for Picea glauca...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(picgla_output,
              picgla_list,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Byte,
              workingType=gdal.GDT_Byte,
              xRes=10,
              yRes=-10,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Merge tiles for Picea mariana
if os.path.exists(picmar_output) == 0:
    print(f'Merging {len(picmar_files)} tiles for Picea mariana...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(picmar_output,
              picmar_list,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Byte,
              workingType=gdal.GDT_Byte,
              xRes=10,
              yRes=-10,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='bilinear',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Combine picea cover and apply threshold using blocked read/write
if os.path.exists(threshold_output) == 0:
    print(f'Apply picea cover threshold...')
    iteration_start = time.time()
    input_raster = rasterio.open(picgla_output)
    input_profile = input_raster.profile.copy()
    area_raster = rasterio.open(area_input)
    picgla_raster = rasterio.open(picgla_output)
    picmar_raster = rasterio.open(picmar_output)
    with rasterio.open(threshold_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window,
                                          masked=False)
            picgla_block = picgla_raster.read(window=window,
                                              masked=False)
            picmar_block = picmar_raster.read(window=window,
                                              masked=False)
            # Add block data
            raster_block = picmar_block + picgla_block
            # Set no data values in input raster to 0
            raster_block = np.where((raster_block >= 5) & (raster_block <= 150), 1, 0)
            # Write results
            dst.write(raster_block,
                      window=window)
            # Report progress
            count, progress = raster_block_progress(100, len(window_list), count, progress)
    end_timing(iteration_start)

# Resample threshold raster to final output
if os.path.exists(picea_output) == 0:
    print(f'Resampling output threshold file...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(picea_output,
              threshold_output,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Byte,
              workingType=gdal.GDT_Byte,
              xRes=50,
              yRes=-50,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='near',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Resample area raster to final output
if os.path.exists(area_output) == 0:
    print(f'Resampling area raster...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(area_output,
              area_input,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Byte,
              workingType=gdal.GDT_Byte,
              xRes=50,
              yRes=-50,
              srcNodata=nodata,
              dstNodata=nodata,
              outputBounds=area_bounds,
              resampleAlg='near',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)
