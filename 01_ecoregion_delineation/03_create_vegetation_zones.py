# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create vegetation zone raster
# Author: Timm Nawrocki
# Last Updated: 2023-12-12
# Usage: Execute in Python 3.9+.
# Description: "Create vegetation zone raster" combines vegetation zones and the spruce extent vector..
# ---------------------------------------------------------------------------

# Import packages
import os
import time
import numpy as np
import rasterio
from osgeo import gdal
from akutils import *

# Set nodata value
nodata = -32768

# Set root directory
drive = 'D:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Landfire_BpS/Data')
ecoregion_folder = os.path.join(project_folder, 'Data_Input/ecoregion_inputs')
zones_folder = os.path.join(ecoregion_folder, 'zones')
intermediate_folder = os.path.join(ecoregion_folder, 'intermediate')

# Define input files
area_input = os.path.join(ecoregion_folder, 'AlaskaYukon_MapDomain_50m_3338.tif')
tnp_input = os.path.join(zones_folder, 'TemperateNorthPacific_ModelArea_3338.shp')
spruce_input = os.path.join(zones_folder, 'AlaskaYukon_SpruceExtent_3338.shp')
zones_input = os.path.join(zones_folder, 'Alaska_VegetationZones_Initial.shp')

# Define intermediate files
tnp_intermediate = os.path.join(intermediate_folder, 'TemperateNorthPacific_ModelArea_50m_3338.tif')
spruce_intermediate = os.path.join(intermediate_folder, 'AlaskaYukon_SpruceExtent_50m_3338.tif')
zones_intermediate = os.path.join(intermediate_folder, 'Alaska_VegetationZones_Initial_50m_3338.tif')

# Define output files
zones_output = os.path.join(intermediate_folder, 'AlaskaYukon_VegetationZones_50m_3338.tif')

#### PROCESS RASTER CONVERSIONS

# Calculate area bounds
area_bounds = raster_bounds(area_input)

# Convert Temperate North Pacific region
if os.path.exists(tnp_intermediate) == 0:
    print('Converting Temperate North Pacific region to raster...')
    iteration_start = time.time()
    # Open the data source
    tnp_vector = gdal.OpenEx(tnp_input)
    # Rasterize the vector
    gdal.Rasterize(tnp_intermediate,
                   tnp_vector,
                   format='GTIFF',
                   outputType=gdal.GDT_Int16,
                   creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'],
                   noData=nodata,
                   initValues=nodata,
                   outputSRS='EPSG:3338',
                   outputBounds=area_bounds,
                   xRes=50,
                   yRes=50,
                   allTouched=True,
                   attribute='value')
    end_timing(iteration_start)

# Convert spruce extent to raster
if os.path.exists(spruce_intermediate) == 0:
    print('Converting spruce extent polygon to raster...')
    iteration_start = time.time()
    # Open the data source
    spruce_vector = gdal.OpenEx(spruce_input)
    # Rasterize the vector
    gdal.Rasterize(spruce_intermediate,
                   spruce_vector,
                   format='GTIFF',
                   outputType=gdal.GDT_Int16,
                   creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'],
                   noData=nodata,
                   initValues=nodata,
                   outputSRS='EPSG:3338',
                   outputBounds=area_bounds,
                   xRes=50,
                   yRes=50,
                   allTouched=True,
                   attribute='value')
    end_timing(iteration_start)

# Convert initial zones to raster
if os.path.exists(zones_intermediate) == 0:
    print('Converting initial zones to raster...')
    iteration_start = time.time()
    # Open the data source
    zones_vector = gdal.OpenEx(zones_input)
    # Rasterize the vector
    gdal.Rasterize(zones_intermediate,
                   zones_vector,
                   format='GTIFF',
                   outputType=gdal.GDT_Int16,
                   creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'],
                   noData=nodata,
                   initValues=nodata,
                   outputSRS='EPSG:3338',
                   outputBounds=area_bounds,
                   xRes=50,
                   yRes=50,
                   allTouched=True,
                   attribute='value')
    end_timing(iteration_start)

#### DELINEATE VEGETATION ZONES

# Combine data sources using blocked read/write
print('Delineating vegetation zones...')
iteration_start = time.time()
tnp_raster = rasterio.open(tnp_intermediate)
spruce_raster = rasterio.open(spruce_intermediate)
zones_raster = rasterio.open(zones_intermediate)
input_profile = zones_raster.profile.copy()
area_raster = rasterio.open(area_input)
with rasterio.open(zones_output, 'w', **input_profile, BIGTIFF='YES') as dst:
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
        tnp_block = tnp_raster.read(window=window,
                                    masked=False)
        spruce_block = spruce_raster.read(window=window,
                                          masked=False)
        zones_block = zones_raster.read(window=window,
                                        masked=False)
        # Create alternate values for initial zones
        zones_block = np.where(zones_block != nodata,
                               zones_block + 100,
                               nodata)
        # Set initial values
        raster_block = np.where((tnp_block == 1) & (zones_block == nodata),
                                1,
                                zones_block)
        # Set temperate-boreal
        raster_block = np.where(raster_block == 102,
                                2,
                                raster_block)
        # Set southern boreal
        raster_block = np.where(raster_block == 103,
                                3,
                                raster_block)
        # Set central boreal
        raster_block = np.where(raster_block == 104,
                                4,
                                raster_block)
        # Set northern boreal
        raster_block = np.where((spruce_block == 20) &
                                ((raster_block == 106) | (raster_block == 107)),
                                5,
                                raster_block)
        # Set northern Arctic
        raster_block = np.where((raster_block == 106) | (raster_block == 107),
                                12,
                                raster_block)
        # Set western boreal
        raster_block = np.where((spruce_block == 20) &
                                ((raster_block == 108) | (raster_block == 109)),
                                6,
                                raster_block)
        # Set western Arctic
        raster_block = np.where((raster_block == 108) | (raster_block == 109),
                                11,
                                raster_block)
        # Set southwest boreal
        raster_block = np.where((spruce_block == 20) &
                                ((raster_block == 119) | (raster_block == 122)),
                                7,
                                raster_block)
        # Set southwest Arctic transition
        raster_block = np.where(raster_block == 119,
                                10,
                                raster_block)
        # Set southwest maritime transition
        raster_block = np.where(raster_block == 122,
                                8,
                                raster_block)
        # Set maritime
        raster_block = np.where((raster_block == 112) | (raster_block == 113),
                                9,
                                raster_block)
        # Write results
        dst.write(raster_block,
                  window=window)
        # Report progress
        count, progress = raster_block_progress(100, len(window_list), count, progress)
end_timing(iteration_start)
