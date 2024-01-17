# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Assign EVT
# Author: Timm Nawrocki
# Last Updated: 2024-01-17
# Usage: Execute in Python 3.9+.
# Description: "Assign EVT" combines the AKVEG parsed results into the Landfire Map
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
area_input = os.path.join(project_folder, 'Data_Input/Landfire_AKVEG_Automated_Domain_30m_3338.tif')
landfire_input = os.path.join(intermediate_folder, 'LA16_EVT_200.tif')
zones_input = os.path.join(intermediate_folder, 'AlaskaYukon_VegetationZones_30m_3338.tif')
biomes_input = os.path.join(intermediate_folder, 'AlaskaYukon_Biomes_30m_3338.tif')
subboreal_input = os.path.join(intermediate_folder, 'Alaska_EcologicalSystems_Subboreal_30m_3338.tif')
parsed_input = os.path.join(output_folder, round_date, 'akveg_parsed_30m_3338.tif')

# Define output files
evt_output = os.path.join(output_folder, round_date, 'AKVEG_Landfire_Combined_30m_3338.tif')

# Prepare input rasters
area_raster = rasterio.open(area_input)
landfire_raster = rasterio.open(landfire_input)
zones_raster = rasterio.open(zones_input)
biomes_raster = rasterio.open(biomes_input)
subboreal_raster = rasterio.open(subboreal_input)
parsed_raster = rasterio.open(parsed_input)

# Parse EVT
print(f'Parsing evt...')
iteration_start = time.time()
input_profile = landfire_raster.profile.copy()
input_profile.update(nodata=nodata)
with rasterio.open(evt_output, 'w', **input_profile, BIGTIFF='YES') as dst:
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
        biomes_block = biomes_raster.read(window=window, masked=False)
        subboreal_block = subboreal_raster.read(window=window, masked=False)
        lf_block = landfire_raster.read(window=window, masked=False)
        in_block = parsed_raster.read(window=window, masked=False)

        # Set base value
        out_block = np.where(area_block == 1, 1, nodata)

        #### SPRUCE WOODLAND AND FOREST TYPES

        # 4483. Alaska Sub-boreal White-Lutz Spruce Forest and Woodland
        out_block = np.where(((lf_block == 4410) | (lf_block == 4482) | (lf_block == 4483))
                             & ((in_block == 2) | (in_block == 3) | (in_block == 8) | (in_block == 11))
                             & (subboreal_block == 1),
                             4483, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 2) | (in_block == 3) | (in_block == 8) | (in_block == 11))
                             & (subboreal_block == 1),
                             4483, out_block)

        # 4456. Western North American Boreal Black Spruce Bog and Dwarf-Tree Peatland
        out_block = np.where(((lf_block == 4456) | (lf_block == 4457))
                             & (in_block == 15)
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4456, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 15)
                             & (biomes_block == 3),
                             4456, out_block)

        # 4467. Western North American Boreal Mesic-Wet Black Spruce Forest and Woodland
        out_block = np.where(((lf_block == 4467) | (lf_block == 4484))
                             & ((in_block == 4) | (in_block == 5) | (in_block == 9) | (in_block == 12))
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4467, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 4) | (in_block == 5) | (in_block == 9) | (in_block == 12))
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4467, out_block)

        # 4474. Western North American Boreal Spruce-Lichen Woodland
        out_block = np.where((lf_block == 4474)
                             & (in_block == 1)
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4474, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 1)
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4474, out_block)

        # 4476. Western North American Boreal Wet Black Spruce-Tussock Woodland
        out_block = np.where((lf_block == 4476)
                             & (in_block == 14)
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4476, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 14)
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4476, out_block)

        # 4479. Western North American Boreal Treeline White Spruce-Hardwood Woodland
        out_block = np.where(((lf_block == 4475) | (lf_block == 4478) | (lf_block == 4479))
                             & ((in_block == 2) | (in_block == 3))
                             & ((biomes_block == 2) | (biomes_block == 3)) & (subboreal_block != 1),
                             4479, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 2) | (in_block == 3))
                             & ((biomes_block == 2) | (biomes_block == 3)) & (subboreal_block != 1),
                             4479, out_block)

        # 4481. Western North American Boreal Mesic White Spruce-Hardwood Forest
        out_block = np.where(((lf_block == 4462) | (lf_block == 4466) | (lf_block == 4468) | (lf_block == 4469)
                              | (lf_block == 4480) | (lf_block == 4481))
                             & ((in_block == 8) | (in_block == 11))
                             & ((biomes_block == 2) | (biomes_block == 3)) & (subboreal_block != 1),
                             4481, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 8) | (in_block == 11))
                             & ((biomes_block == 2) | (biomes_block == 3)) & (subboreal_block != 1),
                             4481, out_block)

        # 10004. Western North American Boreal Mixed Spruce-Hardwood Forest & Woodland
        out_block = np.where((out_block == 1)
                             & ((in_block == 6) | (in_block == 7) | (in_block == 10) | (in_block == 13))
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             10004, out_block)


        #### DECIDUOUS FOREST TYPES

        # 4463. Western North American Boreal Mesic Birch-Aspen Forest
        out_block = np.where(((lf_block == 4463) | (lf_block == 4402) | (lf_block == 4403)
                              | ((lf_block >= 4485) & (lf_block <= 4492)))
                             & (in_block == 16),
                             4463, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 16),
                             4463, out_block)


        #### BIRCH-WILLOW-ALDER

        # 4404. Alaska Arctic Mesic Alder Shrubland
        out_block = np.where((lf_block == 4404)
                             & ((in_block == 17) | (in_block == 21))
                             & ((biomes_block == 6) | (biomes_block == 7)),
                            4404, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 17) | (in_block == 21))
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4404, out_block)

        # 4408. Alaska Sub-boreal Mesic Subalpine Alder Shrubland
        out_block = np.where((lf_block == 4408)
                             & ((in_block == 17) | (in_block == 21))
                             & (subboreal_block == 1),
                             4408, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 17) | (in_block == 21))
                             & (subboreal_block == 1),
                             4408, out_block)

        # 4425. Alaskan Pacific-Aleutian Alder-Salmonberry-Copperbush Shrubland
        out_block = np.where((lf_block == 4425)
                             & ((in_block == 17) | (in_block == 21))
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 4) | (biomes_block == 5)),
                             4425, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 17) | (in_block == 21))
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 4) | (biomes_block == 5)),
                             4425, out_block)

        # 10005. Western North American Boreal Mesic Alder Shrubland
        out_block = np.where((out_block == 1)
                             & ((in_block == 17) | (in_block == 21))
                             & (biomes_block == 3) & (subboreal_block != 1),
                             10005, out_block)

        # 4431. Aleutian Mesic-Wet Willow Shrubland
        out_block = np.where((lf_block == 4431)
                             & ((in_block == 23) | (in_block == 24) | (in_block == 25) | (in_block == 26) | (in_block == 27))
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4431, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 23) | (in_block == 24) | (in_block == 25) | (in_block == 26) | (in_block == 27))
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4431, out_block)

        # 4442. North American Arctic Mesic-Wet Low Willow Shrubland
        out_block = np.where(((lf_block == 4442) | (lf_block == 4441))
                             & ((in_block == 23) | (in_block == 24) | (in_block == 25) | (in_block == 27))
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4442, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 23) | (in_block == 24) | (in_block == 25) | (in_block == 27))
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4442, out_block)

        # 4444. North American Arctic Scrub Birch-Ericaceous Shrubland
        out_block = np.where((lf_block == 4444)
                             & (in_block == 28)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4444, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 28)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4444, out_block)

        # 4465. Western North American Boreal Mesic Scrub Birch-Willow Shrubland
        out_block = np.where((lf_block == 4465)
                             & ((in_block == 23) | (in_block == 26) | (in_block == 28))
                             & (biomes_block == 3),
                             4465, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 23) | (in_block == 26) | (in_block == 28))
                             & (biomes_block == 3),
                             4465, out_block)

        # 4471. Western North American Boreal Shrub Swamp
        out_block = np.where((lf_block == 4471)
                             & ((in_block == 18) | (in_block == 22) | (in_block == 24) | (in_block == 27))
                             & (biomes_block == 3),
                             4471, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 18) | (in_block == 22) | (in_block == 24) | (in_block == 27))
                             & (biomes_block == 3),
                             4471, out_block)

        # 4472. Western North American Boreal Shrub-Sedge Bog & Acidic Fen
        out_block = np.where(((lf_block == 4472) | (lf_block == 4473))
                             & ((in_block == 25) | (in_block == 30))
                             & (biomes_block == 3),
                             4472, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 25) | (in_block == 30))
                             & (biomes_block == 3),
                             4472, out_block)

        # 7663. North Pacific Shrub Swamp
        out_block = np.where((lf_block == 7663)
                             & ((in_block == 18) | (in_block == 22) | (in_block == 24) | (in_block == 25) | (in_block == 27)
                                & (biomes_block == 1) | (biomes_block == 2)),
                             7663, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 18) | (in_block == 22) | (in_block == 24) | (in_block == 25) | (in_block == 27)
                                & (biomes_block == 1) | (biomes_block == 2)),
                             7663, out_block)


        #### SEDGE (-SHRUB) TYPES

        # 4911. Alaskan Pacific Acidic Sedge Peatland
        out_block = np.where(((lf_block == 4911) | (lf_block == 4411))
                             & ((in_block == 29) | (in_block == 30) | (in_block == 31))
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 4) | (biomes_block == 5)),
                             4911, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 30) | (in_block == 31))
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 4) | (biomes_block == 5)),
                             4911, out_block)

        # 4427. Alaskan Pacific-Aleutian Fen and Wet Meadow
        out_block = np.where((lf_block == 4427)
                             & (in_block == 29)
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 4) | (biomes_block == 5)),
                             4427, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 29)
                             & ((biomes_block == 1) | (biomes_block == 2) | (biomes_block == 4) | (biomes_block == 5)),
                             4427, out_block)

        # 4438. North American Arctic Freshwater Marsh
        out_block = np.where((lf_block == 4438)
                             & ((in_block == 29) | (in_block == 37))
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4438, out_block)

        # 4446. North American Arctic Wet Sedge Tundra and Polygonal Ground
        out_block = np.where((lf_block == 4446)
                             & (in_block == 29)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4446, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 29)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4446, out_block)

        # 4448. North American Arctic-Subarctic Shrub-Tussock Tundra
        out_block = np.where(((lf_block == 4448) | (lf_block == 4443))
                             & (in_block == 19)
                             & ((biomes_block == 3) | (biomes_block == 4) | (biomes_block == 6) | (biomes_block == 7)),
                             4448, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 19)
                             & ((biomes_block == 3) | (biomes_block == 4) | (biomes_block == 6) | (biomes_block == 7)),
                             4448, out_block)

        # 4450. North American Arctic-Subarctic Tussock Tundra
        out_block = np.where(((lf_block == 4450) | (lf_block == 4943))
                             & (in_block == 20)
                             & ((biomes_block == 3) | (biomes_block == 4) | (biomes_block == 6) | (biomes_block == 7)),
                             4450, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 20)
                             & ((biomes_block == 3) | (biomes_block == 4) | (biomes_block == 6) | (biomes_block == 7)),
                             4450, out_block)

        # 4461. Western North American Boreal Freshwater Emergent Marsh
        out_block = np.where((lf_block == 4461)
                             & ((in_block == 29) | (in_block == 37))
                             & (biomes_block == 3),
                             4461, out_block)

        # 4477. Western North American Boreal Wet Meadow
        out_block = np.where(((lf_block == 4477) | (in_block == 4973))
                             & (in_block == 29)
                             & (biomes_block == 3),
                             4477, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 29)
                             & (biomes_block == 3),
                             4477, out_block)

        # 4437. North American Arctic Dwarf-shrub-Wet Sedge-Sphagnum Peatland
        out_block = np.where(((lf_block == 4437) | (lf_block == 4937))
                             & ((in_block == 30) | (in_block == 31))
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4437, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 31)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4437, out_block)


        #### DWARF SHRUB TYPES

        # 4401. Alaska Arctic Coastal Sedge-Dwarf-Shrubland (Retain Original)
        out_block = np.where((lf_block == 4401),
                             4401, out_block)

        # 4405. Alaska Arctic Permafrost Plateau Dwarf-Shrub Lichen Tundra
        out_block = np.where((lf_block == 4405)
                             & ((in_block == 19) | (in_block == 20) | (in_block == 33))
                             & ((zones_block == 6) | (zones_block == 10) | (zones_block == 11)),
                             4405, out_block)

        # 4429. Aleutian Ericaceous Dwarf-shrubland Heath and Fell-field
        out_block = np.where((lf_block == 4429)
                             & (in_block == 34)
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4429, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 34)
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4429, out_block)

        # 4435. North American Arctic Dryas Tundra
        out_block = np.where((lf_block == 4435)
                             & (in_block == 35)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4435, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 35)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4435, out_block)

        # 4436. North American Arctic Dwarf-Shrub Lichen Tundra
        out_block = np.where((lf_block == 4436)
                             & (in_block == 33)
                             & ((biomes_block != 1) & (biomes_block != 2)),
                             4436, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 33)
                             & ((biomes_block != 1) & (biomes_block != 2)),
                             4436, out_block)

        # 4435. Western North American Boreal Alpine Dwarf-shrubland
        out_block = np.where((lf_block == 4435)
                             & ((in_block == 34) | (in_block == 35))
                             & (biomes_block == 3),
                             4435, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 34) | (in_block == 35))
                             & (biomes_block == 3),
                             4435, out_block)

        #### HERBACEOUS TYPES

        # 4407. Alaska Sub-boreal and Maritime Alpine Mesic Herbaceous Meadow
        out_block = np.where((lf_block == 4407)
                             & (in_block == 36)
                             & ((biomes_block == 1) | (biomes_block == 2) | (subboreal_block == 1)),
                             4407, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 36)
                             & ((biomes_block == 1) | (biomes_block == 2) | (subboreal_block == 1)),
                             4407, out_block)

        # 4430. Aleutian Mesic Herbaceous Meadow
        out_block = np.where((lf_block == 4430)
                             & (in_block == 36)
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4430, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 36)
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4430, out_block)

        # 4440. North American Arctic Mesic Herbaceous Meadow
        out_block = np.where((lf_block == 4440)
                             & (in_block == 36)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4440, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 36)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4440, out_block)

        # 4454. Western North American Boreal Alpine Mesic Herbaceous Meadow (Retain Original)
        out_block = np.where((lf_block == 4454)
                             & ((in_block != 32) & (in_block != 33))
                             & (biomes_block == 3),
                             4454, out_block)

        # 4460. Western North American Boreal Dry Grassland (Retain Original)
        out_block = np.where((lf_block == 4460)
                             & (biomes_block == 3),
                             4460, out_block)

        # 4464. Western North American Boreal Mesic Bluejoint-Forb Meadow
        out_block = np.where((lf_block == 4464)
                             & (in_block == 36)
                             & ((biomes_block == 2) | (biomes_block == 3)),
                             4464, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 36)
                             & (biomes_block == 3),
                             4464, out_block)


        #### RETAIN ORIGINAL

        # Retain original classification
        out_block = np.where((lf_block == 4406)
                             | (lf_block == 4409)
                             | (lf_block == 4412)
                             | (lf_block == 4415)
                             | (lf_block == 4416)
                             | (lf_block == 4417)
                             | (lf_block == 4418)
                             | (lf_block == 4419)
                             | (lf_block == 4420)
                             | (lf_block == 4421)
                             | (lf_block == 4422)
                             | (lf_block == 4423)
                             | (lf_block == 4426)
                             | (lf_block == 4428)
                             | (lf_block == 4447)
                             | (lf_block == 4449)
                             | (lf_block == 4459)
                             | (lf_block == 4947)
                             | (lf_block == 7178)
                             | (lf_block == 7191)
                             | (lf_block == 7192)
                             | (lf_block == 7193)
                             | (lf_block == 7195)
                             | (lf_block == 7196)
                             | (lf_block == 7197)
                             | (lf_block == 7198)
                             | (lf_block == 7199)
                             | (lf_block == 7292)
                             | (lf_block == 7295)
                             | (lf_block == 7296)
                             | (lf_block == 7297)
                             | (lf_block == 7298)
                             | (lf_block == 7299)
                             | (lf_block == 7300)
                             | (lf_block == 7662)
                             | (lf_block == 7668)
                             | (lf_block == 7669)
                             | (lf_block == 7735)
                             | (lf_block == 7754)
                             | (lf_block == 7755),
                             lf_block, out_block)


        #### SPARSE OR BARREN

        # 4432. Aleutian Volcanic Rock and Talus
        out_block = np.where((lf_block == 4432)
                             & ((in_block == 37) | (in_block == 38))
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4432, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 37) | (in_block == 38))
                             & ((biomes_block == 4) | (biomes_block == 5)),
                             4432, out_block)

        # 4434. North American Arctic Bedrock and Talus
        out_block = np.where((lf_block == 4434)
                             & (in_block == 38)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4434, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 38)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4434, out_block)

        # 4439. North American Arctic Lichen Tundra
        out_block = np.where((lf_block == 4439)
                             & (in_block == 32)
                             & ((biomes_block != 1) & (biomes_block != 2)),
                             4439, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 32)
                             & ((biomes_block != 1) & (biomes_block != 2)),
                             4439, out_block)

        # 4445. North American Arctic Sparse Tundra
        out_block = np.where((lf_block == 4445)
                             & (in_block == 37)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4445, out_block)
        out_block = np.where((out_block == 1)
                             & (in_block == 37)
                             & ((biomes_block == 6) | (biomes_block == 7)),
                             4445, out_block)

        # 4458. Western North American Boreal Cliff Scree and Rock
        out_block = np.where(((lf_block == 4458) | (lf_block == 4455))
                             & ((in_block == 37) | (in_block == 38))
                             & (biomes_block == 3),
                             4458, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 37) | (in_block == 38))
                             & (biomes_block == 3),
                             4458, out_block)

        # 7733. North Pacific Montane Massive Bedrock, Cliff, and Talus
        out_block = np.where(((lf_block == 7733) | (lf_block == 7734))
                             & ((in_block == 37) | (in_block == 38))
                             & ((biomes_block == 1) | (biomes_block == 2)),
                             7733, out_block)
        out_block = np.where((out_block == 1)
                             & ((in_block == 37) | (in_block == 38))
                             & ((biomes_block == 1) | (biomes_block == 2)),
                             7733, out_block)


        #### CORRECTIONS

        # 4447 TO 4947
        out_block = np.where(out_block == 4447,
                             4947, out_block)

        # Southern boreal tussock tundra to sedge-shrub
        out_block = np.where(((out_block == 4448) | (out_block == 4450))
                             & (zones_block == 3),
                             4472, out_block)

        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)


        #### EXPORT

        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
