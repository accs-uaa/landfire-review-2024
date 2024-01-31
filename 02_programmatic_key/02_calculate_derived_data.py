# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate derived data
# Author: Timm Nawrocki
# Last Updated: 2024-01-27
# Usage: Execute in Python 3.9+.
# Description: "Calculate derived data" calculates new metrics from the foliar cover maps.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
import numpy as np
import rasterio
from akutils import *

# Set no data value
nodata = -32768

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
foliar_folder = os.path.join(project_folder, 'Data_Input/akveg_foliar_30m')
intermediate_folder = os.path.join(project_folder, 'Data_Input/intermediate')
derived_folder = os.path.join(project_folder, 'Data_Input/akveg_derived_30m')

# Define input files
area_input = os.path.join(project_folder, 'Data_Input/Landfire_AKVEG_Automated_Domain_30m_3338.tif')
abovedomain_input = os.path.join(intermediate_folder, 'ABoVE_Domain_30m_3338.tif')
alnus_input = os.path.join(foliar_folder, 'alnus_30m_3338.tif')
betshr_input = os.path.join(foliar_folder, 'betshr_30m_3338.tif')
dectre_input = os.path.join(foliar_folder, 'dectre_30m_3338.tif')
empnig_input = os.path.join(foliar_folder, 'empnig_30m_3338.tif')
erivag_input = os.path.join(foliar_folder, 'erivag_30m_3338.tif')
picgla_input = os.path.join(foliar_folder, 'picgla_30m_3338.tif')
picmar_input = os.path.join(foliar_folder, 'picmar_30m_3338.tif')
rhoshr_input = os.path.join(foliar_folder, 'rhoshr_30m_3338.tif')
salshr_input = os.path.join(foliar_folder, 'salshr_30m_3338.tif')
sphagn_input = os.path.join(foliar_folder, 'sphagn_30m_3338.tif')
vacvit_input = os.path.join(foliar_folder, 'vacvit_30m_3338.tif')
wetsed_input = os.path.join(foliar_folder, 'wetsed_30m_3338.tif')
decshr_input = os.path.join(foliar_folder, 'decshr_30m_3338.tif')
evrshr_input = os.path.join(foliar_folder, 'evrshr_30m_3338.tif')
lichen_input = os.path.join(foliar_folder, 'lichen_30m_3338.tif')
gramin_input = os.path.join(foliar_folder, 'gramin_30m_3338.tif')
forb_input = os.path.join(foliar_folder, 'forb_30m_3338.tif')

# Define output files
picratio_output = os.path.join(derived_folder, 'picea_ratio_30m_3338.tif')
picsum_output = os.path.join(derived_folder, 'picea_sum_30m_3338.tif')
decratio_output = os.path.join(derived_folder, 'deciduous_ratio_30m_3338.tif')
ndshrub_output = os.path.join(derived_folder, 'alder_birch_willow_30m_3338.tif')
eridwarf_output = os.path.join(derived_folder, 'ericaceous_dwarf_30m_3338.tif')
wetland_output = os.path.join(derived_folder, 'wetland_indicator_30m_3338.tif')
picwet_output = os.path.join(derived_folder, 'picmar_wet_indicator_30m_3338.tif')
herbaceous_output = os.path.join(derived_folder, 'herbaceous_30m_3338.tif')
vegetation_output = os.path.join(derived_folder, 'vegetation_30m_3338.tif')

# Open area raster
area_raster = rasterio.open(area_input)

# Calculate Picea ratio
if os.path.exists(picratio_output) == 0:
    print(f'Calculating Picea ratio...')
    iteration_start = time.time()
    picgla_raster = rasterio.open(picgla_input)
    picmar_raster = rasterio.open(picmar_input)
    input_profile = picgla_raster.profile.copy()
    with rasterio.open(picratio_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            picgla_block = picgla_raster.read(window=window, masked=False)
            picmar_block = picmar_raster.read(window=window, masked=False)
            # Calculate Picea ratio
            raster_block = (picgla_block / (picgla_block + picmar_block + 0.01)) * 100
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate Picea sum
if os.path.exists(picsum_output) == 0:
    print(f'Calculating Picea sum...')
    iteration_start = time.time()
    picgla_raster = rasterio.open(picgla_input)
    picmar_raster = rasterio.open(picmar_input)
    input_profile = picgla_raster.profile.copy()
    with rasterio.open(picsum_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            picgla_block = picgla_raster.read(window=window, masked=False)
            picmar_block = picmar_raster.read(window=window, masked=False)
            # Calculate Picea ratio
            raster_block = picgla_block + picmar_block
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate deciduous ratio
if os.path.exists(decratio_output) == 0:
    print(f'Calculating deciduous ratio...')
    iteration_start = time.time()
    picgla_raster = rasterio.open(picgla_input)
    picmar_raster = rasterio.open(picmar_input)
    dectre_raster = rasterio.open(dectre_input)
    input_profile = picgla_raster.profile.copy()
    with rasterio.open(decratio_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            picgla_block = picgla_raster.read(window=window, masked=False)
            picmar_block = picmar_raster.read(window=window, masked=False)
            dectre_block = dectre_raster.read(window=window, masked=False)
            # Calculate Picea ratio
            raster_block = (dectre_block / (picgla_block + picmar_block + dectre_block + 0.01)) * 100
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate non-dwarf shrub output
if os.path.exists(ndshrub_output) == 0:
    print(f'Calculating non-dwarf shrub sum...')
    iteration_start = time.time()
    alnus_raster = rasterio.open(alnus_input)
    betshr_raster = rasterio.open(betshr_input)
    salshr_raster = rasterio.open(salshr_input)
    input_profile = alnus_raster.profile.copy()
    with rasterio.open(ndshrub_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            alnus_block = alnus_raster.read(window=window, masked=False)
            salshr_block = salshr_raster.read(window=window, masked=False)
            betshr_block = betshr_raster.read(window=window, masked=False)
            # Calculate ndshrub sum
            raster_block = alnus_block + salshr_block + betshr_block
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate ericaceous dwarf shrub output
if os.path.exists(eridwarf_output) == 0:
    print(f'Calculating ericaceous dwarf shrub sum...')
    iteration_start = time.time()
    empnig_raster = rasterio.open(empnig_input)
    rhoshr_raster = rasterio.open(rhoshr_input)
    vacvit_raster = rasterio.open(vacvit_input)
    input_profile = empnig_raster.profile.copy()
    with rasterio.open(eridwarf_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            empnig_block = empnig_raster.read(window=window, masked=False)
            rhoshr_block = rhoshr_raster.read(window=window, masked=False)
            vacvit_block = vacvit_raster.read(window=window, masked=False)
            # Calculate ericaceous dwarf shrub sum
            raster_block = empnig_block + rhoshr_block + vacvit_block
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate wetland indicator
if os.path.exists(wetland_output) == 0:
    print(f'Calculating wetland indicator...')
    iteration_start = time.time()
    wetsed_raster = rasterio.open(wetsed_input)
    sphagn_raster = rasterio.open(sphagn_input)
    input_profile = wetsed_raster.profile.copy()
    with rasterio.open(wetland_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            sphagn_block = sphagn_raster.read(window=window, masked=False)
            wetsed_block = wetsed_raster.read(window=window, masked=False)
            # Calculate wetland indicator
            raster_block = sphagn_block + wetsed_block
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate Picea mariana wet indicator
if os.path.exists(picwet_output) == 0:
    print(f'Calculating Picea mariana wet indicator...')
    iteration_start = time.time()
    erivag_raster = rasterio.open(erivag_input)
    sphagn_raster = rasterio.open(sphagn_input)
    wetsed_raster = rasterio.open(wetsed_input)
    input_profile = wetsed_raster.profile.copy()
    with rasterio.open(picwet_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            sphagn_block = sphagn_raster.read(window=window, masked=False)
            wetsed_block = wetsed_raster.read(window=window, masked=False)
            erivag_block = erivag_raster.read(window=window, masked=False)
            # Calculate Picea mariana wet indicator
            raster_block = erivag_block + sphagn_block + wetsed_block
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate herbaceous output
if os.path.exists(herbaceous_output) == 0:
    print(f'Calculating herbaceous output...')
    iteration_start = time.time()
    above_raster = rasterio.open(abovedomain_input)
    forb_raster = rasterio.open(forb_input)
    gramin_raster = rasterio.open(gramin_input)
    erivag_raster = rasterio.open(erivag_input)
    wetsed_raster = rasterio.open(wetsed_input)
    input_profile = wetsed_raster.profile.copy()
    with rasterio.open(herbaceous_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            above_block = above_raster.read(window=window, masked=False)
            forb_block = forb_raster.read(window=window, masked=False)
            gramin_block = gramin_raster.read(window=window, masked=False)
            erivag_block = erivag_raster.read(window=window, masked=False)
            wetsed_block = wetsed_raster.read(window=window, masked=False)
            # Correct ABoVE domain
            forb_block = np.where(above_block != 1, 0, forb_block)
            gramin_block = np.where(above_block != 1, 0, gramin_block)
            # Calculate herbaceous cover
            raster_block = (forb_block + gramin_block) - (erivag_block + wetsed_block)
            # Set no data values from area raster to no data
            raster_block = np.where(raster_block < 0, 0, raster_block)
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)

# Calculate vegetation output
if os.path.exists(vegetation_output) == 0:
    print(f'Calculating vegetation sum...')
    iteration_start = time.time()
    above_raster = rasterio.open(abovedomain_input)
    dectre_raster = rasterio.open(dectre_input)
    decshr_raster = rasterio.open(decshr_input)
    evrshr_raster = rasterio.open(evrshr_input)
    forb_raster = rasterio.open(forb_input)
    gramin_raster = rasterio.open(gramin_input)
    picgla_raster = rasterio.open(picgla_input)
    picmar_raster = rasterio.open(picmar_input)
    sphagn_raster = rasterio.open(sphagn_input)
    input_profile = picgla_raster.profile.copy()
    with rasterio.open(vegetation_output, 'w', **input_profile, BIGTIFF='YES') as dst:
        # Find number of raster blocks
        window_list = []
        for block_index, window in area_raster.block_windows(1):
            window_list.append(window)
        # Iterate processing through raster blocks
        count = 1
        progress = 0
        for block_index, window in area_raster.block_windows(1):
            area_block = area_raster.read(window=window, masked=False)
            above_block = above_raster.read(window=window, masked=False)
            dectre_block = dectre_raster.read(window=window, masked=False)
            decshr_block = decshr_raster.read(window=window, masked=False)
            evrshr_block = evrshr_raster.read(window=window, masked=False)
            forb_block = forb_raster.read(window=window, masked=False)
            gramin_block = gramin_raster.read(window=window, masked=False)
            picgla_block = picgla_raster.read(window=window, masked=False)
            picmar_block = picmar_raster.read(window=window, masked=False)
            sphagn_block = sphagn_raster.read(window=window, masked=False)
            # Correct ABoVE domain
            decshr_block = np.where(above_block != 1, 0, decshr_block)
            evrshr_block = np.where(above_block != 1, 0, evrshr_block)
            forb_block = np.where(above_block != 1, 0, forb_block)
            gramin_block = np.where(above_block != 1, 0, gramin_block)
            # Calculate vegetation sum
            raster_block = dectre_block + decshr_block + evrshr_block + forb_block + gramin_block + picgla_block + picmar_block + sphagn_block
            raster_block = np.where(raster_block > 254, 254, raster_block)
            # Set no data values from area raster to no data
            raster_block = np.where(area_block != 1, nodata, raster_block)
            # Write results
            dst.write(raster_block, window=window)
            # Report progress
            count, progress = raster_block_progress(10, len(window_list), count, progress)
    end_timing(iteration_start)
