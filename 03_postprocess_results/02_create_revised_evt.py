# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create revised Landfire EVT
# Author: Timm Nawrocki
# Last Updated: 2024-01-27
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Create revised Landfire EVT" combines the EVT that resulted from the automated checks with the original Landfire 2016 EVT.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
import numpy as np
import rasterio
from osgeo import gdal
from akutils import *

# Set no data
nodata = -32768

# Set round date
round_date = 'round_20240125'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
landfire_folder = os.path.join(project_folder, 'Data_Input/landfire_evt')
intermediate_folder = os.path.join(project_folder, 'Data_Input/intermediate')
check_folder = os.path.join(project_folder, 'Data_Output/automated_checks')
output_folder = os.path.join(project_folder, 'Data_Output/final_rasters')
workspace_folder = os.path.join(output_folder, 'workspace')
if os.path.exists(workspace_folder) == 0:
    os.mkdir(workspace_folder)

# Define input datasets
area_input = os.path.join(project_folder, 'Data_Input/Landfire_Domain_30m_3338.tif')
landfire_input = os.path.join(landfire_folder, 'LA16_EVT_200.tif')
subboreal_input = os.path.join(intermediate_folder, 'Alaska_EcologicalSystems_Subboreal_30m_3338.tif')
evt_input = os.path.join(check_folder, round_date, 'AKVEG_Landfire_Combined_30m_3338.tif')

# Define output datasets
evt_intermediate = os.path.join(workspace_folder, 'AKVEG_Landfire_Combined_30m_3338.tif')
subboreal_intermediate = os.path.join(workspace_folder, 'Alaska_EcologicalSystems_Subboreal_30m_3338.tif')
revised_output = os.path.join(output_folder, round_date, 'Landfire_EVT_Revised_30m_3338.tif')

# Calculate area bounds
area_bounds = raster_bounds(area_input)

# Process sub-boreal input data
if os.path.exists(subboreal_intermediate) == 0:
    print(f'Standardizing sub-boreal zone...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(subboreal_intermediate,
              subboreal_input,
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

# Set extent of automated checks to match landfire domain
if os.path.exists(evt_intermediate) == 0:
    print(f'Standardizing automated check results...')
    iteration_start = time.time()
    # Merge tiles
    gdal.Warp(evt_intermediate,
              evt_input,
              srcSRS='EPSG:3338',
              dstSRS='EPSG:3338',
              outputType=gdal.GDT_Int16,
              workingType=gdal.GDT_Int16,
              xRes=30,
              yRes=-30,
              srcNodata=-32768,
              dstNodata=-32768,
              outputBounds=area_bounds,
              resampleAlg='near',
              targetAlignedPixels=False,
              creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    end_timing(iteration_start)

# Prepare input rasters
area_raster = rasterio.open(area_input)
landfire_raster = rasterio.open(landfire_input)
subboreal_raster = rasterio.open(subboreal_intermediate)
evt_raster = rasterio.open(evt_intermediate)

# Merge automated and original EVTs
print('Merging automated and original EVTs...')
iteration_start = time.time()
input_profile = landfire_raster.profile.copy()
input_profile.update(nodata=nodata)
with rasterio.open(revised_output, 'w', **input_profile, BIGTIFF='YES') as dst:
    # Find number of raster blocks
    window_list = []
    for block_index, window in area_raster.block_windows(1):
        window_list.append(window)
    # Iterate processing through raster blocks
    count = 1
    progress = 0
    for block_index, window in area_raster.block_windows(1):
        #### LOAD BLOCKS
        area_block = area_raster.read(window=window, masked=False)
        subboreal_block = subboreal_raster.read(window=window, masked=False)
        lf_block = landfire_raster.read(window=window, masked=False)
        evt_block = evt_raster.read(window=window, masked=False)

        # Set base value
        out_block = np.where(area_block == 1, 1, nodata)

        # Integrate automated checks
        out_block = np.where(evt_block > 255, evt_block, out_block)

        # Integrate original landfire 2016 EVT
        out_block = np.where(out_block == 1, lf_block, out_block)

        # Apply type corrections
        out_block = np.where(out_block == 4457, 4456, out_block)
        out_block = np.where(out_block == 4484, 4467, out_block)
        out_block = np.where(out_block == 4475, 4479, out_block)
        out_block = np.where(out_block == 4478, 4479, out_block)
        out_block = np.where(out_block == 4462, 4481, out_block)
        out_block = np.where(out_block == 4466, 4481, out_block)
        out_block = np.where(out_block == 4468, 4481, out_block)
        out_block = np.where(out_block == 4469, 4481, out_block)
        out_block = np.where(out_block == 4480, 4481, out_block)
        out_block = np.where(out_block == 4410, 4483, out_block)
        out_block = np.where(out_block == 4482, 4483, out_block)
        out_block = np.where(out_block == 4402, 4463, out_block)
        out_block = np.where(out_block == 4403, 4463, out_block)
        out_block = np.where(out_block == 4485, 4463, out_block)
        out_block = np.where(out_block == 4486, 4463, out_block)
        out_block = np.where(out_block == 4487, 4463, out_block)
        out_block = np.where(out_block == 4488, 4463, out_block)
        out_block = np.where(out_block == 4489, 4463, out_block)
        out_block = np.where(out_block == 4490, 4463, out_block)
        out_block = np.where(out_block == 4491, 4463, out_block)
        out_block = np.where(out_block == 4492, 4463, out_block)
        out_block = np.where(out_block == 4441, 4442, out_block)
        out_block = np.where(out_block == 4473, 4472, out_block)
        out_block = np.where(out_block == 4937, 4437, out_block)
        out_block = np.where(out_block == 4443, 4448, out_block)
        out_block = np.where(out_block == 4943, 4450, out_block)
        out_block = np.where(out_block == 4973, 4477, out_block)
        out_block = np.where(out_block == 4411, 4911, out_block)
        out_block = np.where(out_block == 4455, 4458, out_block)
        out_block = np.where(out_block == 7734, 7733, out_block)
        out_block = np.where(out_block == 4413, 4423, out_block)
        out_block = np.where(out_block == 4913, 4423, out_block)
        out_block = np.where(out_block == 4414, 4425, out_block)
        out_block = np.where(out_block == 4985, 4425, out_block)
        out_block = np.where(out_block == 4986, 4425, out_block)
        out_block = np.where(out_block == 4902, 4442, out_block)
        out_block = np.where(out_block == 4903, 4442, out_block)
        out_block = np.where(out_block == 4966, 4445, out_block)
        out_block = np.where(out_block == 4963, 4458, out_block)
        out_block = np.where(out_block == 4964, 4458, out_block)
        out_block = np.where(out_block == 4970, 4464, out_block)
        out_block = np.where(out_block == 4470, 4471, out_block)
        out_block = np.where(out_block == 4962, 4471, out_block)
        out_block = np.where(out_block == 4968, 4471, out_block)
        out_block = np.where(out_block == 4969, 4471, out_block)
        out_block = np.where(out_block == 4987, 4471, out_block)
        out_block = np.where(out_block == 4988, 4471, out_block)
        out_block = np.where(out_block == 4989, 4471, out_block)
        out_block = np.where(out_block == 4990, 4471, out_block)
        out_block = np.where(out_block == 4991, 4471, out_block)
        out_block = np.where(out_block == 4992, 4471, out_block)
        out_block = np.where(out_block == 4424, 7663, out_block)
        out_block = np.where(out_block == 4965, 7733, out_block)
        out_block = np.where(out_block == 4447, 4947, out_block)

        # Correct sub-boreal types
        out_block = np.where((subboreal_block == 1) & ((out_block == 4479) | (out_block == 4481)),
                             4483, out_block)
        out_block = np.where((subboreal_block == 1) & (out_block == 10005),
                             4408, out_block)

        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)

        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)

# Delete intermediate datasets
os.remove(subboreal_intermediate)
os.remove(evt_intermediate)
