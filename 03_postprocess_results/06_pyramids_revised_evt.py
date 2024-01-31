# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Build pyramids for revised EVT
# Author: Timm Nawrocki
# Last Updated: 2024-01-30
# Usage: Must be executed in an ArcGIS Pro Python 3.9+ distribution.
# Description: "Build pyramids for revised EVT" builds pyramid using the "mode" setting.
# ---------------------------------------------------------------------------

# Import packages
import os
import time
from osgeo import gdal
from akutils import *

# Set version
version = 'v1.0_20240126'

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
output_folder = os.path.join(project_folder,
                             'Data_Output/data_package/data_package_' + version,
                             'Data_Output/final_rasters')

# Define input datasets
revised_input = os.path.join(output_folder, 'Landfire_EVT_Revised_30m_3338.tif')

# Build pyramids
print('Building pyramids...')
iteration_start = time.time()
revised_raster = gdal.Open(revised_input, 0)  # 0 = read-only, 1 = read-write.
gdal.SetConfigOption('COMPRESS_OVERVIEW', 'LZW')
gdal.SetConfigOption('BIGTIFF_OVERVIEW', 'IF_SAFER')
revised_raster.BuildOverviews('MODE', [2, 4, 8, 16, 32, 64, 128, 256], gdal.TermProgress_nocb)
del revised_raster  # close the dataset (Python object and pointers)
end_timing(iteration_start)
