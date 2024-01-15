# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Parse foliar cover to types
# Author: Timm Nawrocki
# Last Updated: 2024-01-14
# Usage: Execute in Python 3.9+.
# Description: "Parse foliar cover to types" implements a programmatic key to create discrete types.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
import numpy as np
import rasterio
from akutils import *

# Set no data
nodata = 255

# Set round date
round_date = 'round_20240114'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
foliar_folder = os.path.join(project_folder, 'Data_Input/akveg_foliar_30m')
derived_folder = os.path.join(project_folder, 'Data_Input/akveg_derived_30m')
intermediate_folder = os.path.join(project_folder, 'Data_Input/intermediate')
output_folder = os.path.join(project_folder, 'Data_Output/automated_checks')

# Define input files
area_input = os.path.join(project_folder, 'Data_Input/NorthAmericanBeringia_v1_30m.tif')
landfire_input = os.path.join(intermediate_folder, 'LA16_EVT_200.tif')
zones_input = os.path.join(intermediate_folder, 'AlaskaYukon_VegetationZones_30m_3338.tif')
alnus_input = os.path.join(foliar_folder, 'alnus_30m_3338.tif')
betshr_input = os.path.join(foliar_folder, 'betshr_30m_3338.tif')
bettre_input = os.path.join(foliar_folder, 'bettre_30m_3338.tif')
dectre_input = os.path.join(foliar_folder, 'dectre_30m_3338.tif')
dryas_input = os.path.join(foliar_folder, 'dryas_30m_3338.tif')
empnig_input = os.path.join(foliar_folder, 'empnig_30m_3338.tif')
erivag_input = os.path.join(foliar_folder, 'erivag_30m_3338.tif')
picgla_input = os.path.join(foliar_folder, 'picgla_30m_3338.tif')
picmar_input = os.path.join(foliar_folder, 'picmar_30m_3338.tif')
rhoshr_input = os.path.join(foliar_folder, 'rhoshr_30m_3338.tif')
salshr_input = os.path.join(foliar_folder, 'salshr_30m_3338.tif')
sphagn_input = os.path.join(foliar_folder, 'sphagn_30m_3338.tif')
vaculi_input = os.path.join(foliar_folder, 'vaculi_30m_3338.tif')
vacvit_input = os.path.join(foliar_folder, 'vacvit_30m_3338.tif')
wetsed_input = os.path.join(foliar_folder, 'wetsed_30m_3338.tif')
decshr_input = os.path.join(foliar_folder, 'decshr_30m_3338.tif')
evrshr_input = os.path.join(foliar_folder, 'evrshr_30m_3338.tif')
lichen_input = os.path.join(foliar_folder, 'lichen_30m_3338.tif')
gramin_input = os.path.join(foliar_folder, 'gramin_30m_3338.tif')
forb_input = os.path.join(foliar_folder, 'forb_30m_3338.tif')
picratio_input = os.path.join(derived_folder, 'picea_ratio_30m_3338.tif')
picsum_input = os.path.join(derived_folder, 'picea_sum_30m_3338.tif')
decratio_input = os.path.join(derived_folder, 'deciduous_ratio_30m_3338.tif')
ndshrub_input = os.path.join(derived_folder, 'ndshrub_30m_3338.tif')
eridwarf_input = os.path.join(derived_folder, 'ericaceous_dwarf_30m_3338.tif')
wetland_input = os.path.join(derived_folder, 'wetland_indicator_30m_3338.tif')
picwet_input = os.path.join(derived_folder, 'picmar_wet_indicator_30m_3338.tif')
vegetation_input = os.path.join(derived_folder, 'vegetation_30m_3338.tif')

# Define output file
parsed_output = os.path.join(output_folder, round_date, 'AKVEG_Parsed_30m_3338.tif')

# Prepare input rasters
print('Opening raster files...')
area_raster = rasterio.open(area_input)
landfire_raster = rasterio.open(landfire_input)
zones_raster = rasterio.open(zones_input)
alnus_raster = rasterio.open(alnus_input)
betshr_raster = rasterio.open(betshr_input)
bettre_raster = rasterio.open(bettre_input)
dectre_raster = rasterio.open(dectre_input)
dryas_raster = rasterio.open(dryas_input)
empnig_raster = rasterio.open(empnig_input)
erivag_raster = rasterio.open(erivag_input)
picgla_raster = rasterio.open(picgla_input)
picmar_raster = rasterio.open(picmar_input)
rhoshr_raster = rasterio.open(rhoshr_input)
salshr_raster = rasterio.open(salshr_input)
sphagn_raster = rasterio.open(sphagn_input)
vaculi_raster = rasterio.open(vaculi_input)
vacvit_raster = rasterio.open(vacvit_input)
wetsed_raster = rasterio.open(wetsed_input)
decshr_raster = rasterio.open(decshr_input)
evrshr_raster = rasterio.open(evrshr_input)
forb_raster = rasterio.open(forb_input)
gramin_raster = rasterio.open(gramin_input)
lichen_raster = rasterio.open(lichen_input)
picratio_raster = rasterio.open(picratio_input)
picsum_raster = rasterio.open(picsum_input)
decratio_raster = rasterio.open(decratio_input)
ndshrub_raster = rasterio.open(ndshrub_input)
eridwarf_raster = rasterio.open(eridwarf_input)
wetland_raster = rasterio.open(wetland_input)
picwet_raster = rasterio.open(picwet_input)
vegetation_raster = rasterio.open(vegetation_input)

# Parse foliar cover
print(f'Parsing foliar cover to types...')
iteration_start = time.time()
input_profile = picgla_raster.profile.copy()
with rasterio.open(parsed_output, 'w', **input_profile, BIGTIFF='YES') as dst:
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
        zones_block = zones_raster.read(window=window, masked=False)
        alnus_block = alnus_raster.read(window=window, masked=False)
        betshr_block = betshr_raster.read(window=window, masked=False)
        bettre_block = bettre_raster.read(window=window, masked=False)
        dectre_block = dectre_raster.read(window=window, masked=False)
        dryas_block = dryas_raster.read(window=window, masked=False)
        # empnig_block = empnig_raster.read(window=window, masked=False)
        erivag_block = erivag_raster.read(window=window, masked=False)
        # picgla_block = picgla_raster.read(window=window, masked=False)
        # picmar_block = picmar_raster.read(window=window, masked=False)
        # rhoshr_block = rhoshr_raster.read(window=window, masked=False)
        salshr_block = salshr_raster.read(window=window, masked=False)
        sphagn_block = sphagn_raster.read(window=window, masked=False)
        # vaculi_block = vaculi_raster.read(window=window, masked=False)
        # vacvit_block = vacvit_raster.read(window=window, masked=False)
        wetsed_block = wetsed_raster.read(window=window, masked=False)
        # decshr_block = decshr_raster.read(window=window, masked=False)
        evrshr_block = evrshr_raster.read(window=window, masked=False)
        forb_block = forb_raster.read(window=window, masked=False)
        gramin_block = gramin_raster.read(window=window, masked=False)
        lichen_block = lichen_raster.read(window=window, masked=False)
        picratio_block = picratio_raster.read(window=window, masked=False)
        picsum_block = picsum_raster.read(window=window, masked=False)
        decratio_block = decratio_raster.read(window=window, masked=False)
        ndshrub_block = ndshrub_raster.read(window=window, masked=False)
        eridwarf_block = eridwarf_raster.read(window=window, masked=False)
        wetland_block = wetland_raster.read(window=window, masked=False)
        picwet_block = picwet_raster.read(window=window, masked=False)
        vegetation_block = vegetation_raster.read(window=window, masked=False)

        #### BEGIN PROGRAMMATIC KEY

        # Set base value
        out_block = np.where(area_block == 1, 253, nodata)
        # Set no data to zero
        evrshr_block = np.where(evrshr_block == 255, 0, evrshr_block)
        lichen_block = np.where(lichen_block == 255, 0, lichen_block)

        #### 1. MAJOR BREAKS

        # 1.17 Alder
        out_block = np.where((out_block == 253) & (alnus_block >= 30),
                             17, out_block)
        # 1.254 Coniferous trees dominant
        out_block = np.where(((zones_block >= 2) & (zones_block <= 7)) & (out_block == 253)
                             & (picsum_block >= 5),
                             254, out_block)
        # 1.16 Deciduous trees dominant
        out_block = np.where((out_block == 253) & (dectre_block >= 20),
                             16, out_block)
        # 1.31 Lichens are dominant or co-dominant
        out_block = np.where((out_block == 253) & (lichen_block >= 15) & (erivag_block < 20),
                             31, out_block)

        #### 2. SPRUCE WOODLAND

        # 2.1 Spruce-lichen woodland
        out_block = np.where((out_block == 254) & (picsum_block < 15) & (lichen_block >= 15),
                             1, out_block)

        # 2.2 White spruce woodland
        out_block = np.where((out_block == 254) & (picsum_block < 15) & (picratio_block >= 70),
                             2, out_block)

        # 2.3 White spruce-hardwood woodland
        out_block = np.where((out_block == 2) & (dectre_block >= 8),
                             3, out_block)

        # 2.4 Black spruce woodland
        out_block = np.where((out_block == 254) & (picsum_block < 15) & (picratio_block <= 30),
                             4, out_block)

        # 2.5 Black spruce-hardwood woodland
        out_block = np.where((out_block == 4) & (dectre_block >= 8),
                             5, out_block)

        # 2.6 Mixed spruce woodland
        out_block = np.where((out_block == 254) & (picsum_block < 15) & (picratio_block > 30),
                             6, out_block)

        # 2.7 Mixed spruce-hardwood woodland
        out_block = np.where((out_block == 6) & (dectre_block >= 8),
                             7, out_block)

        #### 3. SPRUCE FOREST TYPES

        # 3.8 White spruce is dominant
        out_block = np.where((out_block == 254) & (picratio_block >= 70),
                             8, out_block)

        # 3.9a Black spruce is dominant
        out_block = np.where((out_block == 254) & (picratio_block <= 30),
                             9, out_block)

        # 3.10 Mixed spruce
        out_block = np.where((out_block == 254) & (picratio_block > 30),
                             10, out_block)

        # 3.9b Mixed spruce predicted but black spruce dominance is likely because of indicator species
        out_block = np.where((out_block == 10) & (picwet_block >= 15),
                             9, out_block)

        #### 4. MIXED SPRUCE-DECIDUOUS TYPES
        # 4.11 Deciduous trees are co-dominant with white spruce
        out_block = np.where((out_block == 8) & (decratio_block >= 40),
                             11, out_block)

        # 4.12 Deciduous trees are co-dominant with black spruce
        out_block = np.where((out_block == 9) & (decratio_block >= 40),
                             12, out_block)

        # 4.13 Deciduous trees are co-dominant with mixed spruce
        out_block = np.where((out_block == 10) & (decratio_block >= 40),
                             13, out_block)

        #### 5. BLACK SPRUCE WET TYPES
        # 5.14 Black spruce-tussock woodland
        out_block = np.where(((out_block == 9) | (out_block == 12)) & (erivag_block >= 20),
                             14, out_block)

        # 5.15 Black spruce peatland
        out_block = np.where(((out_block == 9) | (out_block == 12)) & (picwet_block >= 15),
                             15, out_block)

        #### 6. TUSSOCK TUNDRA TYPES

        # 6.18 Low shrub-tussock tundra
        out_block = np.where((out_block == 253) & (erivag_block >= 8) & (ndshrub_block < 25),
                             18, out_block)

        # 6.19 Dwarf shrub-tussock tundra
        out_block = np.where((out_block == 18) & (ndshrub_block < 8),
                             19, out_block)

        #### 7. ALDER TYPES
        # 7.17 Alder is dominant
        out_block = np.where((out_block == 253) & (alnus_block >= 18),
                             17, out_block)

        # 7.20 Alder and willow are co-dominant
        out_block = np.where(((out_block == 253) | (out_block == 17))
                             & (alnus_block >= 15) & (salshr_block >= 15),
                             20, out_block)

        # 7.21 Alder and willow wet
        out_block = np.where((out_block == 20) & (wetland_block >= 15),
                             21, out_block)

        #### 8. WILLOW AND BIRCH TYPES

        # 8.22 Mesic willow
        out_block = np.where((out_block == 253) & (salshr_block >= 18),
                             22, out_block)

        # 8.23 Wet willow
        out_block = np.where((out_block == 22) & (wetland_block >= 15),
                             23, out_block)

        # 8.24 Wet shrub-sedge
        out_block = np.where((out_block == 23) & (wetsed_block >= 30),
                             24, out_block)

        # 8.25 Mesic birch-willow shrub
        out_block = np.where((out_block == 22) & (betshr_block >= 15),
                             25, out_block)
        out_block = np.where((out_block == 253) & (betshr_block >= 15) & (salshr_block >= 15),
                             25, out_block)

        # 8.26 Wet birch-willow shrub
        out_block = np.where((out_block == 23) & (betshr_block >= 15),
                             26, out_block)
        out_block = np.where((out_block == 25) & (wetland_block >= 15),
                             26, out_block)

        # 8.27 Mesic birch shrub
        out_block = np.where((out_block == 253) & (betshr_block >= 18),
                             27, out_block)

        #### 9. WET SEDGE AND PEATLAND TYPES

        # 9.28 Wetland sedge meadow
        out_block = np.where((out_block == 253) & (wetsed_block >= 15),
                             28, out_block)

        # 9.29 Peatland
        out_block = np.where((out_block == 28) & (sphagn_block >= 20),
                             29, out_block)
        out_block = np.where((out_block == 253) & (sphagn_block >= 15),
                             29, out_block)

        # 9.30 Dwarf shrub-sphagnum
        out_block = np.where((out_block == 29)
                             & ((evrshr_block >= 15) | (dryas_block >= 12) | (eridwarf_block >= 12)),
                             30, out_block)

        #### 10. DWARF SHRUB TYPES

        # 10.32 Dwarf shrub-lichen
        out_block = np.where((out_block == 31)
                             & ((evrshr_block >= 15) | (dryas_block >= 12) | (eridwarf_block >= 12)),
                             32, out_block)

        # 10.33 Ericaceous (dryas) dwarf shrub
        out_block = np.where((out_block == 253) & (eridwarf_block >= 12) & (dryas_block < 30),
                             33, out_block)

        # 10.34 Dryas dwarf shrub
        out_block = np.where((out_block == 253) & (dryas_block >= 12),
                             34, out_block)

        #### 11. HERBACEOUS

        # 11.35 Herbaceous mix
        out_block = np.where((out_block == 253) & (forb_block + gramin_block >= 20)
                             & ((forb_block != 255) & (gramin_block != 255)),
                             35, out_block)

        #### 12. SPARSE OR BARREN

        # 12.36 Sparse vegetation
        out_block = np.where((out_block == 253) & (vegetation_block - lichen_block < 25)
                             & ((forb_block != 255) & (gramin_block != 255)),
                             36, out_block)

        # 12.37 Barren
        out_block = np.where((out_block == 36) & (vegetation_block <= 10),
                             37, out_block)

        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)
        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
