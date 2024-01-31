# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Parse foliar cover to types
# Author: Timm Nawrocki
# Last Updated: 2024-01-27
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
nodata = -32768

# Set round date
round_date = 'round_20240125'

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
area_input = os.path.join(project_folder, 'Data_Input/Landfire_AKVEG_Automated_Domain_30m_3338.tif')
abovedomain_input = os.path.join(intermediate_folder, 'ABoVE_Domain_30m_3338.tif')
landfire_input = os.path.join(intermediate_folder, 'LA16_EVT_200.tif')
biomes_input = os.path.join(intermediate_folder, 'AlaskaYukon_Biomes_30m_3338.tif')
zones_input = os.path.join(intermediate_folder, 'AlaskaYukon_VegetationZones_30m_3338.tif')
subboreal_input = os.path.join(intermediate_folder, 'Alaska_EcologicalSystems_Subboreal_30m_3338.tif')
correction_input = os.path.join(intermediate_folder, 'Correction_BlackMixedSpruce_30m_3338.tif')
elevation_input = os.path.join(intermediate_folder, 'Elevation_30m_3338.tif')
alnus_input = os.path.join(foliar_folder, 'alnus_30m_3338.tif')
betshr_input = os.path.join(foliar_folder, 'betshr_30m_3338.tif')
bettre_input = os.path.join(foliar_folder, 'bettre_30m_3338.tif')
contre_input = os.path.join(foliar_folder, 'contre_30m_3338.tif')
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
ndshrub_input = os.path.join(derived_folder, 'alder_birch_willow_30m_3338.tif')
eridwarf_input = os.path.join(derived_folder, 'ericaceous_dwarf_30m_3338.tif')
wetland_input = os.path.join(derived_folder, 'wetland_indicator_30m_3338.tif')
picwet_input = os.path.join(derived_folder, 'picmar_wet_indicator_30m_3338.tif')
herbac_input = os.path.join(derived_folder, 'herbaceous_30m_3338.tif')
vegetation_input = os.path.join(derived_folder, 'vegetation_30m_3338.tif')

# Define output file
parsed_output = os.path.join(output_folder, round_date, 'AKVEG_Parsed_30m_3338.tif')

# Prepare input rasters
area_raster = rasterio.open(area_input)
above_raster = rasterio.open(abovedomain_input)
landfire_raster = rasterio.open(landfire_input)
biomes_raster = rasterio.open(biomes_input)
zones_raster = rasterio.open(zones_input)
subboreal_raster = rasterio.open(subboreal_input)
correction_raster = rasterio.open(correction_input)
elevation_raster = rasterio.open(elevation_input)
alnus_raster = rasterio.open(alnus_input)
betshr_raster = rasterio.open(betshr_input)
bettre_raster = rasterio.open(bettre_input)
contre_raster = rasterio.open(contre_input)
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
herbac_raster = rasterio.open(herbac_input)
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
        above_block = above_raster.read(window=window, masked=False)
        biomes_block = biomes_raster.read(window=window, masked=False)
        zones_block = zones_raster.read(window=window, masked=False)
        subboreal_block = subboreal_raster.read(window=window, masked=False)
        correction_block = correction_raster.read(window=window, masked=False)
        elevation_block = elevation_raster.read(window=window, masked=False)
        alnus_block = alnus_raster.read(window=window, masked=False)
        betshr_block = betshr_raster.read(window=window, masked=False)
        bettre_block = bettre_raster.read(window=window, masked=False)
        contre_block = contre_raster.read(window=window, masked=False)
        dectre_block = dectre_raster.read(window=window, masked=False)
        dryas_block = dryas_raster.read(window=window, masked=False)
        erivag_block = erivag_raster.read(window=window, masked=False)
        picmar_block = picmar_raster.read(window=window, masked=False)
        salshr_block = salshr_raster.read(window=window, masked=False)
        sphagn_block = sphagn_raster.read(window=window, masked=False)
        wetsed_block = wetsed_raster.read(window=window, masked=False)
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
        herbac_block = herbac_raster.read(window=window, masked=False)
        vegetation_block = vegetation_raster.read(window=window, masked=False)

        #### BEGIN PROGRAMMATIC KEY

        # Set base value
        out_block = np.where(area_block == 1, 253, nodata)

        #### 1. MAJOR BREAKS

        # 1.17 Mesic Alder (field value >= 50)
        out_block = np.where((out_block == 253) & (alnus_block >= 36),
                             17, out_block)
        # 1.254 Coniferous trees dominant (field value >= 5 / 5)
        out_block = np.where((out_block == 253) & (picsum_block >= 8)
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 3)),
                             254, out_block)
        out_block = np.where((out_block == 253)
                             & ((contre_block >= 7) & (picsum_block >= 1))
                             & ((zones_block == 5) | (zones_block == 7)),
                             254, out_block)
        # 1.16 Deciduous trees dominant
        out_block = np.where((out_block == 253) & (dectre_block >= 24) & (decratio_block >= 55),
                             16, out_block)  # field value >= 30
        out_block = np.where((out_block == 253) & (dectre_block >= 17) & (decratio_block >= 70)
                             & (dectre_block >= (ndshrub_block * 0.5)),
                             16, out_block)  # field value >= 15
        out_block = np.where((out_block == 254) & (dectre_block >= 17) & (decratio_block >= 70),
                             16, out_block)  # field value >= 15
        # 1.32 Lichens are dominant or co-dominant
        out_block = np.where((out_block == 253) & (lichen_block >= 16) & (erivag_block < 19),
                             32, out_block)  # field value >= 20 / 20
        out_block = np.where((out_block == 253) & (lichen_block >= 27),
                             32, out_block)  # field value >= 40

        #### 2. SPRUCE WOODLAND

        # 2.1 Spruce-lichen woodland
        out_block = np.where((out_block == 254) & ((contre_block < 35) | (picsum_block < 27)) & (lichen_block >= 15),
                             1, out_block)  # field value < 40 / < 40 / >= 20
        out_block = np.where((out_block == 254) & ((contre_block < 35) | (picsum_block < 27)) & (lichen_block >= 8)
                             & ((zones_block == 5) | (zones_block == 7)),
                             1, out_block)  # field value < 40 / < 40 / >= 5

        # 2.2 White spruce woodland (field value < 15 / 20)
        out_block = np.where((out_block == 254) & (picratio_block >= 60)
                             & ((contre_block < 15) | (picsum_block < 16)),
                             2, out_block)

        # 2.3 White spruce-hardwood woodland (field value >= 5 & < 15)
        out_block = np.where((out_block == 2) & ((dectre_block >= 12) & (dectre_block < 17)),
                             3, out_block)

        # 2.4 Black spruce woodland (field value < 15 / 20)
        out_block = np.where((out_block == 254) & (picratio_block <= 40)
                             & ((contre_block < 15) | (picsum_block < 16)),
                             4, out_block)

        # 2.5 Black spruce-hardwood woodland (field value >= 5 & < 15)
        out_block = np.where((out_block == 4) & ((dectre_block >= 12) & (dectre_block < 17)),
                             5, out_block)

        # 2.6 Mixed spruce woodland (field value < 15 / 20)
        out_block = np.where((out_block == 254) & (picratio_block > 40)
                             & ((contre_block < 15) | (picsum_block < 16)),
                             6, out_block)

        # 2.7 Mixed spruce-hardwood woodland (field value >= 5 & < 15)
        out_block = np.where((out_block == 6) & ((dectre_block >= 12) & (dectre_block < 17)),
                             7, out_block)

        #### 3. SPRUCE FOREST TYPES

        # 3.8 White spruce is dominant
        out_block = np.where((out_block == 254) & (picratio_block >= 60),
                             8, out_block)

        # 3.9a Black spruce is dominant
        out_block = np.where((out_block == 254) & (picratio_block <= 40),
                             9, out_block)

        # 3.10 Mixed spruce
        out_block = np.where((out_block == 254) & (picratio_block > 40),
                             10, out_block)

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

        # Correction: narrow the black and mixed spruce woodland types
        out_block = np.where(((out_block == 4) | (out_block == 5)) & (contre_block < 10),
                             253, out_block)
        out_block = np.where(((out_block == 6) | (out_block == 7)) & (contre_block < 10),
                             253, out_block)

        #### 5. BLACK SPRUCE WET TYPES
        # 5.14 Black spruce-tussock woodland
        out_block = np.where(((out_block == 4) | (out_block == 6) | (out_block == 9) | (out_block == 10))
                             & (erivag_block >= 23),
                             14, out_block)  # field value >= 30
        out_block = np.where(((out_block == 4) | (out_block == 6) | (out_block == 9) | (out_block == 10))
                             & (erivag_block >= 16) & (ndshrub_block < 35),
                             14, out_block)  # field value >= 15 / 35

        # 5.15 Black spruce peatland (field value >= 8 / < 60)
        out_block = np.where(((out_block == 4) | (out_block == 6) | (out_block == 9) | (out_block == 10))
                             & (picwet_block >= 8) & (salshr_block < 34),
                             15, out_block)

        # Correction: black spruce wet types are coniferous (black spruce) forest (field value >= 40 / 40)
        out_block = np.where(((out_block == 14) | (out_block == 15)) & ((contre_block >= 35) | (picsum_block >= 27)),
                             9, out_block)

        # Correction: correct black-mixed spruce beyond black spruce range
        out_block = np.where(((out_block == 4) | (out_block == 6)) & (correction_block == 1),
                             2, out_block)
        out_block = np.where(((out_block == 5) | (out_block == 7)) & (correction_block == 1),
                             3, out_block)
        out_block = np.where(((out_block == 9) | (out_block == 10)) & (correction_block == 1),
                             8, out_block)
        out_block = np.where(((out_block == 12) | (out_block == 13)) & (correction_block == 1),
                             11, out_block)
        out_block = np.where(((out_block == 14) | (out_block == 15)) & (correction_block == 1),
                             2, out_block)

        # Correction: correct black spruce tussock in Cook Inlet and Kenai Peninsula
        out_block = np.where((out_block == 14) & (subboreal_block == 1) & ((zones_block == 2) | (zones_block == 3)),
                             15, out_block)

        # Correction: correct white spruce in Cook Inlet Wetlands
        out_block = np.where(((out_block == 2) | (out_block == 3) | (out_block == 8) | (out_block == 11))
                             & (wetland_block >= 10)
                             & (subboreal_block == 1) & (zones_block == 3),
                             253, out_block)

        #### 6. TUSSOCK TUNDRA TYPES

        # 6.19 Low shrub-tussock tundra
        out_block = np.where((out_block == 253) & (erivag_block >= 23),
                             19, out_block)
        out_block = np.where((out_block == 253) & (erivag_block >= 16) & (ndshrub_block < 35),
                             19, out_block)  # field value >= 15 / < 35
        out_block = np.where((out_block == 253) & (erivag_block >= 10) & (ndshrub_block < 40)
                             & ((zones_block == 7) | (zones_block == 8) | (zones_block >= 10)),
                             19, out_block)  # field value >= 8 / < 40

        # 6.20 Dwarf shrub-tussock tundra (field value < 5)
        out_block = np.where((out_block == 19) & (ndshrub_block < 8),
                             20, out_block)

        #### 7. ALDER TYPES
        # 7.17 Mesic alder (field value >= 20)
        out_block = np.where((out_block == 253) & (alnus_block >= 18),
                             17, out_block)

        # 7.18 Wet alder (field value >= 20)
        out_block = np.where((out_block == 17) & (wetland_block >= 20),
                             18, out_block)

        # 7.21 Alder and willow are co-dominant (field value >= 15 / 15)
        out_block = np.where(((out_block == 253) | (out_block == 17) | (out_block == 18))
                             & (alnus_block >= 14) & (salshr_block >= 13),
                             21, out_block)

        # 7.22 Alder and willow wet (field value >= 20)
        out_block = np.where((out_block == 21) & (wetland_block >= 20),
                             22, out_block)

        #### 8. WILLOW AND BIRCH TYPES

        # 8.23 Mesic willow (field value >= 25)
        out_block = np.where((out_block == 253) & (salshr_block >= 18),
                             23, out_block)

        # 8.24 Wet willow (field value >= 20)
        out_block = np.where((out_block == 23) & (wetland_block >= 20),
                             24, out_block)

        # 8.26 Mesic birch-willow shrub
        out_block = np.where((out_block == 23) & (betshr_block >= 16),
                             26, out_block)  # field value >= 15
        out_block = np.where((out_block == 253) & (betshr_block >= 16) & (salshr_block >= 15),
                             26, out_block)  # field value >= 15 / 15

        # 8.27 Wet birch-willow shrub
        out_block = np.where((out_block == 24) & (betshr_block >= 16),
                             27, out_block)  # field value >= 15
        out_block = np.where((out_block == 26) & (wetland_block >= 20),
                             27, out_block) # field value >= 20

        # 8.25 Wet shrub-sphagnum
        out_block = np.where(((out_block == 24) | (out_block == 27)) & (sphagn_block >= 15),
                             25, out_block)  # field value >= 15
        out_block = np.where((out_block == 19) & (sphagn_block >= 44) & (erivag_block < 23)
                             & ((zones_block == 12)),
                             25, out_block)  # field value >= 70
        out_block = np.where((out_block == 19) & (sphagn_block >= 29)
                             & (zones_block != 12),
                             25, out_block)  # field value >= 40

        # 8.28 Mesic birch shrub (field value >= 15)
        out_block = np.where((out_block == 253) & (betshr_block >= 15),
                             28, out_block)

        # Correction: correct tussock tundra in Cook Inlet and Kenai Peninsula
        out_block = np.where(((out_block == 19) | (out_block == 20))
                             & (subboreal_block == 1) & ((zones_block == 2) | (zones_block == 3)),
                             25, out_block)

        #### 9. WET SEDGE AND PEATLAND TYPES

        # 9.29 Wetland sedge meadow (field value >= 15)
        out_block = np.where((out_block == 253) & (wetsed_block >= 18),
                             29, out_block)

        # 9.30 Peatland
        out_block = np.where((out_block == 29) & (sphagn_block >= 20),
                             30, out_block)  # field value >= 20
        out_block = np.where((out_block == 253) & (sphagn_block >= 15),
                             30, out_block)  # field value >= 15
        out_block = np.where((out_block == 20) & (sphagn_block >= 44) & (erivag_block < 23)
                             & (zones_block == 12),
                             30, out_block)  # field value >= 70
        out_block = np.where((out_block == 20) & (sphagn_block >= 29)
                             & (zones_block != 12),
                             30, out_block)  # field value >= 40

        # 9.31 Dwarf shrub-sphagnum (field value >= 20 / 15)
        out_block = np.where((out_block == 30)
                             & ((evrshr_block >= 17) | (eridwarf_block >= 15)),
                             31, out_block)

        #### 10. DWARF SHRUB TYPES

        # 10.33 Dwarf shrub-lichen (field value >= 20 / 15 / 15)
        out_block = np.where((out_block == 32)
                             & ((evrshr_block >= 15) | (dryas_block >= 12) | (eridwarf_block >= 15)),
                             33, out_block)

        # 10.34 Ericaceous (dryas) dwarf shrub (field value >= 15 / < 30)
        out_block = np.where((out_block == 253) & (eridwarf_block >= 15) & (dryas_block < 20),
                             34, out_block)

        # 10.35 Dryas dwarf shrub (field value >= 15)
        out_block = np.where((out_block == 253) & (dryas_block >= 12),
                             35, out_block)

        # Correction: ericaceous shrubs in wet areas should be dwarf-shrub peatlands
        out_block = np.where((out_block == 34) & (wetland_block >= 10) & (zones_block != 12),
                             31, out_block)

        # Correction: ericaceous shrubs do not relate to EVT below subalpine in Kenai Peninsula and Cook Inlet
        out_block = np.where((out_block == 34) &
                             (elevation_block < 500)
                             & ((zones_block == 2) | (zones_block == 3)) & (subboreal_block ==1),
                             253, out_block)

        # Correction: ericaceous shrubs do not relate to EVT below subalpine in boreal
        out_block = np.where((out_block == 34)
                             & (elevation_block < 900)
                             & (biomes_block == 3), 253, out_block)

        #### 11. HERBACEOUS

        # 11.36 Herbaceous mix
        out_block = np.where((herbac_block >= 40)
                             & (alnus_block < 10) & (salshr_block < 15) & (dectre_block < 15) & (contre_block < 8)
                             & (subboreal_block == 1),
                             36, out_block) # Lowland Kenai Peninsula meadows
        out_block = np.where((herbac_block >= 25)
                             & (alnus_block < 10) & (salshr_block < 15) & (dectre_block < 15) & (contre_block < 8)
                             & (elevation_block >= 1200)
                             & (biomes_block == 3),
                             36, out_block) # Talkeetna, Wrangell, and Alaska Range alpine
        out_block = np.where((herbac_block >= 25)
                             & (alnus_block < 10) & (salshr_block < 15) & (dectre_block < 15) & (contre_block < 8)
                             & (elevation_block >= 800)
                             & (subboreal_block == 1), # Subboreal mountain alpine
                             36, out_block)  # Talkeetna, Wrangell, and Alaska Range alpine
        out_block = np.where((out_block == 253) & (herbac_block >= 25),
                             36, out_block)  # field value >= 25
        # 9.29 Wetland sedge meadow (field value >= 5)
        out_block = np.where((out_block == 253) & (wetsed_block >= 11),
                             29, out_block)

        #### 12. SPARSE OR BARREN

        # 12.37 Sparse vegetation
        out_block = np.where((out_block == 253) & (vegetation_block < 25) & (above_block == 1),
                             37, out_block)

        # 12.38 Barren
        out_block = np.where((out_block == 37) & (vegetation_block <= 10) & (above_block == 1),
                             38, out_block)

        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)
        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
