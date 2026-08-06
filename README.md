# Disparity Assessment in the Distribution of Toxic Water Pollution

## Project Overview

This repository supports the analysis of industrial water pollution exposure for communities adjacent to the Mississippi River.

## Workflow

Scripts are intended to be run sequentially in the order shown below.

- [0_download_rsei_water_gm.py](0_download_rsei_water_gm.py): Download RSEI water geographic microdata
- [1_define_study_area.py](1_define_study_area.py): Select HUC-12 units within the study area
- [2_pop_preprocess_cbg.py](2_pop_preprocess_cbg.py): Preprocess demographic data at the Census Block Group level
- [3_pop_cbg_to_pixels.py](3_pop_cbg_to_pixels.py): Rasterize demographics to 30-m grids
- [4_pop_pixels_to_huc12.py](4_pop_pixels_to_huc12.py): Aggregate gridded demographics to HUC-12 subwatersheds
- [5_rsei_to_huc12.py](5_rsei_to_huc12.py): Aggregate RSEI flowline toxicity to HUC-12 subwatersheds
- [6_analysis.ipynb](6_analysis.ipynb): Statistical analysis and calculation of disparity metrics
- [7_source_tracing.ipynb](7_source_tracing.ipynb): Facility and chemical source attribution
- [notebooks-figures](notebooks-figures): Figure generation notebooks
- [utils](utils): Shared helper functions
- [environment.yml](environment.yml): Conda environment definition

## System Requirements

This workflow was executed on Linux-based HPC systems (University of Minnesota MSI). Required Python packages are listed in [environment.yml](environment.yml). For environment setup, run the following:
- `mamba env create -f environment.yml`
- `source activate ej`
- `ipython kernel install --user --name=ej`


## Data Release

- Study area boundary (county level): https://s3.msi.umn.edu/ejwater/results/aoi_county_boundaries.gpkg
- Study area boundary (HUC-12 subwatershed level): https://s3.msi.umn.edu/ejwater/results/aoi_huc12_boundaries.gpkg
- Disparity ratios for demographic groups (2008 to 2012): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2008_2012.csv
- Disparity ratios for demographic groups (2013 to 2017): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2013_2017.csv
- Disparity ratios for demographic groups (2018 to 2022): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2018_2022.csv
- Socioeconomic and demographic characteristics of HUC-12 subwatershed units: https://s3.msi.umn.edu/ejwater/results/huc12_demographics.csv
- Toxicity-weighted concentrations for HUC-12 subwatershed units: https://s3.msi.umn.edu/ejwater/results/huc12_rsei_toxconc_weighted.csv
- Descriptive statistics of toxic concentration exposure footprints: https://s3.msi.umn.edu/ejwater/results/toxconc_descriptive_stats.csv
- T-test statistics comparing impacted and non-impacted subwatersheds: https://s3.msi.umn.edu/ejwater/results/toxconc_ttest_stats.csv
- Chemicals contributing to toxic water pollution in the study area: https://s3.msi.umn.edu/ejwater/results/source_chemicals.csv
- Industrial facilities identified as pollution sources: https://s3.msi.umn.edu/ejwater/results/source_facilities.csv

## Input data sources
- U.S. Geological Survey (USGS) 2025 Watershed Boundary Dataset (WBD) - National, FileGDB (https://www.usgs.gov/national-hydrography/access-national-hydrography-products) 
- U.S. Environmental Protection Agency (EPA) 2022a Risk-Screening Environmental Indicators Geographic Microdata (RSEI-GM), Version 2.3.12, Universe Core01 (http://abt-rsei.s3-website-us-east-1.amazonaws.com/?prefix=microdata2022/water/) 
- U.S. Environmental Protection Agency (EPA) 2022b Risk-Screening Environmental Indicators (RSEI) Public Release Data tables, Version 2.3.12 (https://www.epa.gov/rsei/rsei-data-dictionary-facility-data)
- U.S. Environmental Protection Agency (EPA) 2010 Dasymetric Allocation of Population, Conterminous U.S., 2010 v.3, raster (https://www.epa.gov/enviroatlas/data-download)
- Schroeder J, Van Riper D, Manson S, Knowles K, Kugler T, Roberts F and Ruggles S 2025 IPUMS National Historical Geographic Information System: Version 20.0. 2022 American Community Survey: 5-Year Data: 2008-2012, 2013-2017, and 2018-2022, Block Groups & Larger Areas (doi: 10.18128/D050.V20.0)


