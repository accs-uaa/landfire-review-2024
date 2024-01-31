# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Assess pixel change
# Author: Timm Nawrocki
# Last Updated: 2024-01-30
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Assess pixel change" combines the EVT that resulted from the automated checks with the original Landfire 2016 EVT.
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

# Set version
version = 'v1.0_20240126'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
landfire_folder = os.path.join(project_folder, 'Data_Input/landfire_evt')
intermediate_folder = os.path.join(project_folder, 'Data_Input/intermediate')
output_folder = os.path.join(project_folder,
                             'Data_Output/data_package/data_package_' + version,
                             'Data_Output/final_rasters')

# Define input datasets
area_input = os.path.join(project_folder, 'Data_Input/Landfire_Domain_30m_3338.tif')
checkdomain_input = os.path.join(intermediate_folder, 'Landfire_AKVEG_Automated_FullZone_30m_3338.tif')
landfire_input = os.path.join(landfire_folder, 'LA16_EVT_200.tif')
revised_input = os.path.join(output_folder, 'Landfire_EVT_Revised_30m_3338.tif')

# Define output datasets
status_output = os.path.join(output_folder, 'Landfire_EVT_Status_30m_3338.tif')

# Calculate area bounds
area_bounds = raster_bounds(area_input)

# Prepare input rasters
area_raster = rasterio.open(area_input)
check_raster = rasterio.open(checkdomain_input)
landfire_raster = rasterio.open(landfire_input)
revised_raster = rasterio.open(revised_input)

# Assessing change status
print('Assessing change status...')
iteration_start = time.time()
input_profile = landfire_raster.profile.copy()
input_profile.update(nodata=nodata)
with rasterio.open(status_output, 'w', **input_profile, BIGTIFF='YES') as dst:
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
        check_block = check_raster.read(window=window, masked=False)
        lf_block = landfire_raster.read(window=window, masked=False)
        evt_block = revised_raster.read(window=window, masked=False)

        # Set base value
        out_block = np.where(area_block == 1, 1, nodata)

        # Assess where manual review required
        out_block = np.where(check_block != 1, 5, out_block)

        # Assess where original and revised do not match
        out_block = np.where((out_block == 1) & (lf_block != evt_block), 2, out_block)

        # Assess where change is related to classification system update
        out_block = np.where((lf_block == 4457) & (evt_block == 4456), 3, out_block)
        out_block = np.where((lf_block == 4484) & (evt_block == 4467), 3, out_block)
        out_block = np.where((lf_block == 4475) & (evt_block == 4479), 3, out_block)
        out_block = np.where((lf_block == 4478) & (evt_block == 4479), 3, out_block)
        out_block = np.where((lf_block == 4466) & (evt_block == 4481), 3, out_block)
        out_block = np.where((lf_block == 4480) & (evt_block == 4481), 3, out_block)
        out_block = np.where((lf_block == 4410) & (evt_block == 4483), 3, out_block)
        out_block = np.where((lf_block == 4482) & (evt_block == 4483), 3, out_block)
        out_block = np.where((lf_block == 4441) & (evt_block == 4442), 3, out_block)
        out_block = np.where((lf_block == 4473) & (evt_block == 4472), 3, out_block)
        out_block = np.where((lf_block == 4937) & (evt_block == 4437), 3, out_block)
        out_block = np.where((lf_block == 4443) & (evt_block == 4448), 3, out_block)
        out_block = np.where((lf_block == 4943) & (evt_block == 4450), 3, out_block)
        out_block = np.where((lf_block == 4973) & (evt_block == 4477), 3, out_block)
        out_block = np.where((lf_block == 4411) & (evt_block == 4911), 3, out_block)
        out_block = np.where((lf_block == 4455) & (evt_block == 4458), 3, out_block)
        out_block = np.where((lf_block == 7734) & (evt_block == 7733), 3, out_block)
        out_block = np.where((lf_block == 4447) & (evt_block == 4947), 3, out_block)

        # Assess where change is related to removal of floodplains
        out_block = np.where((lf_block == 4413) & (evt_block == 4423), 4, out_block)
        out_block = np.where((lf_block == 4913) & (evt_block == 4423), 4, out_block)
        out_block = np.where((lf_block == 4414) & (evt_block == 4425), 4, out_block)
        out_block = np.where((lf_block == 4985) & (evt_block == 4425), 4, out_block)
        out_block = np.where((lf_block == 4986) & (evt_block == 4425), 4, out_block)
        out_block = np.where((lf_block == 4902) & (evt_block == 4442), 4, out_block)
        out_block = np.where((lf_block == 4903) & (evt_block == 4442), 4, out_block)
        out_block = np.where((lf_block == 4966) & (evt_block == 4445), 4, out_block)
        out_block = np.where((lf_block == 4963) & (evt_block == 4458), 4, out_block)
        out_block = np.where((lf_block == 4964) & (evt_block == 4458), 4, out_block)
        out_block = np.where((lf_block == 4402) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4403) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4485) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4486) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4487) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4488) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4489) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4490) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4491) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4492) & (evt_block == 4463), 4, out_block)
        out_block = np.where((lf_block == 4970) & (evt_block == 4464), 4, out_block)
        out_block = np.where((lf_block == 4470) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4962) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4968) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4969) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4987) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4988) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4989) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4990) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4991) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4992) & (evt_block == 4471), 4, out_block)
        out_block = np.where((lf_block == 4462) & (evt_block == 4481), 4, out_block)
        out_block = np.where((lf_block == 4468) & (evt_block == 4481), 4, out_block)
        out_block = np.where((lf_block == 4469) & (evt_block == 4481), 4, out_block)
        out_block = np.where((lf_block == 4424) & (evt_block == 7663), 4, out_block)
        out_block = np.where((lf_block == 4965) & (evt_block == 7733), 4, out_block)

        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)

        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
