# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Assign EVT
# Author: Timm Nawrocki
# Last Updated: 2024-01-14
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
parsed_input = os.path.join(output_folder, round_date, 'akveg_parsed_30m_3338.tif')

# Define output files
landfire_output = os.path.join(output_folder, round_date, 'akveg_landfire_combined_30m_3338.tif')

# Prepare input rasters
print('Opening raster files...')
area_raster = rasterio.open(area_input)
landfire_raster = rasterio.open(landfire_input)
zones_raster = rasterio.open(zones_input)
parsed_raster = rasterio.open(parsed_input)

# Parse foliar cover
print(f'Parsing foliar cover to types...')
iteration_start = time.time()
input_profile = landfire_raster.profile.copy()
with rasterio.open(landfire_output, 'w', **input_profile, BIGTIFF='YES') as dst:
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
        lf_block = landfire_raster.read(window=window, masked=False)
        in_block = parsed_raster.read(window=window, masked=False)

        # Set base value
        out_block = np.where(area_block == 1, 1, nodata)

        #### SPRUCE WOODLAND AND FOREST TYPES

        # 4474. Western North American Boreal Spruce-Lichen Woodland
        out_block = np.where((lf_block == 4474) & (in_block == 1),
                             4474, out_block)
        # 4475. Western North American Boreal Treeline White Spruce Woodland
        out_block = np.where((lf_block == 4475) & (in_block == 2),
                             4475, out_block)
        # 4410. Alaska Sub-boreal White-Lutz Spruce Forest and Woodland
        out_block == np.where((lf_block == 4410) & ((in_block == 2) | (in_block == 8)),
                              4410, out_block)
        # 4479. Western North American Boreal Treeline White Spruce-Hardwood Woodland
        out_block == np.where(((lf_block == 4478) | (lf_block == 4479)) & (in_block == 3),
                              4479, out_block)
        # 4483. Alaska Sub-boreal White-Lutz Spruce-Hardwood Forest and Woodland
        out_block == np.where(((lf_block == 4482) | (lf_block == 4483))
                              & ((in_block == 3) | (in_block == 1)),
                              4483, out_block)
        # 4467. Western North American Boreal Mesic-Wet Black Spruce Forest and Woodland
        out_block == np.where((lf_block == 4467) & ((in_block == 4) | (in_block == 9)),
                              4467, out_block)
        # 4484. Western North American Boreal Mesic-Wet Black Spruce-Hardwood Forest and Woodland
        out_block = np.where((lf_block == 4484) & ((in_block == 5) | (in_block == 12)),
                             4484, out_block)
        # 4466. Western North American Boreal Mesic White Spruce Forest
        out_block = np.where(((lf_block == 4466) | (lf_block == 4462) | (lf_block == 4468) | (lf_block == 4469))
                             & (in_block == 8),
                             4466, out_block)
        # 4480. Western North American Boreal Mesic White Spruce-Hardwood Forest
        out_block = np.where(((lf_block == 4480) | (lf_block == 4481)) & (in_block == 11),
                             4481, out_block)
        # 4476. Western North American Boreal Wet Black Spruce-Tussock Woodland
        out_block == np.where((lf_block == 4476) & (in_block == 14),
                              4476, out_block)
        # 4456. Western North American Boreal Black Spruce Bog and Dwarf-Tree Peatland
        out_block == np.where(((lf_block == 4456) | (lf_block == 4457)) & (in_block == 15),
                              4456, out_block)

        #### DECIDUOUS FOREST TYPES
        # 4463. Western North American Boreal Mesic Birch-Aspen Forest
        out_block = np.where(((lf_block == 4463) | (lf_block == 4402) | (lf_block == 4403)
                              | ((lf_block >= 4485) & (lf_block <= 4492))) & (in_block == 16),
                             4463, out_block)

        #### BIRCH-WILLOW-ALDER
        # 4404. Alaska Arctic Mesic Alder Shrubland
        out_block = np.where((lf_block == 4404) & ((in_block == 17) | (in_block == 20)),
                            4404, out_block)

        # 4408. Alaska Sub-boreal Mesic Subalpine Alder Shrubland
        out_block = np.where((lf_block == 4408) & ((in_block == 17) | (in_block == 20)),
                             4408, out_block)

        # 4425. Alaskan Pacific-Aleutian Alder-Salmonberry-Copperbush Shrubland
        out_block = np.where((lf_block == 4425) & ((in_block == 17) | (in_block == 20)),
                             4425, out_block)

        # 10005. Western North American Boreal Alder Shrubland


        # 4431. Aleutian Mesic-Wet Willow Shrubland
        out_block = np.where((lf_block == 4431) & ((in_block == 22) | (in_block == 23) | (in_block == 26)),
                             4431, out_block)

        # 4442. North American Arctic Mesic-Wet Low Willow Shrubland
        out_block = np.where(((lf_block == 4442) | (lf_block == 4441))
                             & ((in_block == 22) | (in_block == 23) | (in_block == 26)),
                             4442, out_block)

        # 4444. North American Arctic Scrub Birch-Ericaceous Shrubland
        out_block = np.where((lf_block == 4444) & (in_block == 27),
                             4444, out_block)

        # 4465. Western North American Boreal Mesic Scrub Birch-Willow Shrubland
        out_block = np.where((lf_block == 4465) & ((in_block == 22) | (in_block == 25) | (in_block == 27)),
                             4465, out_block)

        # 4471. Western North American Boreal Shrub Swamp
        out_block = np.where((lf_block == 4471) & ((in_block == 21) | (in_block == 23) | (in_block == 26)),
                             4471, out_block)

        # 4472. Western North American Boreal Shrub-Sedge Bog & Acidic Fen
        out_block = np.where(((lf_block == 4472) | (lf_block == 4473)) & (in_block == 24),
                             4472, out_block)

        # 7663. North Pacific Shrub Swamp
        out_block = np.where((lf_block == 7663) | ((in_block == 21) | (in_block == 23) | (in_block == 26)),
                             7663, out_block)


        #### SEDGE (-SHRUB) TYPES

        # 4427. Alaskan Pacific-Aleutian Fen and Wet Meadow
        out_block = np.where((lf_block == 4427) & (in_block == 28),
                             4427, out_block)

        # 4438. North American Arctic Freshwater Marsh
        out_block = np.where((lf_block == 4438) & (in_block == 28),
                             4438, out_block)

        # 4446. North American Arctic Wet Sedge Tundra and Polygonal Ground
        out_block = np.where((lf_block == 4446) & (in_block == 28),
                             4446, out_block)

        # 4448. North American Arctic-Subarctic Shrub-Tussock Tundra
        out_block = np.where(((lf_block == 4448) | (lf_block == 4443)) & (in_block == 18),
                             4448, out_block)

        # 4450. North American Arctic-Subarctic Tussock Tundra
        out_block = np.where(((lf_block == 4450) | (lf_block == 4943)) & (in_block == 4943),
                             4450, out_block)


        #### DWARF SHRUB TYPES
        # 4401. Alaska Arctic Coastal Sedge-Dwarf-Shrubland
        out_block = np.where((lf_block == 4401) & (in_block == 33),
                             4401, out_block)

        # 4405. Alaska Arctic Permafrost Plateau Dwarf-Shrub Lichen Tundra
        out_block = np.where((lf_block == 4405) & (in_block == 32),
                             4405, out_block)

        # 4411. Alaskan Pacific Acidic Shrub Peatland
        out_block = np.where((lf_block == 4411) & (in_block == 30),
                             4411, out_block)

        # 4429. Aleutian Ericaceous Dwarf-shrubland Heath and Fell-field
        out_block = np.where((lf_block == 4429) & (in_block == 33),
                             4429, out_block)

        # 4435. North American Arctic Dryas Tundra




        # Set no data values from area raster to no data
        out_block = np.where(area_block != 1, nodata, out_block)
        # Write results
        dst.write(out_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
