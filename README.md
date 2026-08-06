# Disparity Assessment in the Distribution of Toxic Water Pollution

## Project Overview

This repository supports the analysis of industrial water pollution exposure for communities adjacent to the Mississippi River.

## Execution

Scripts are intended to be run sequentially in the order shown below.

- [0_download_rsei_water_gm.py](0_download_rsei_water_gm.py): Download RSEI water microdata
- [1_define_study_area.py](1_define_study_area.py): Select HUC-12 units within the study area
- [2_pop_preprocess_cbg.py](2_pop_preprocess_cbg.py): Preprocess demographic data at census block group level
- [3_pop_cbg_to_pixels.py](3_pop_cbg_to_pixels.py): Rasterize demographics to 30-m grid
- [4_pop_pixels_to_huc12.py](4_pop_pixels_to_huc12.py): Aggregate gridded demographics to HUC-12 subwatershed
- [5_rsei_to_huc12.py](5_rsei_to_huc12.py): Aggregate RSEI flowline toxicity to HUC-12 subwatersheds
- [6_analysis.ipynb](6_analysis.ipynb): Statistical analysis and calculation of disparity metrics
- [7_source_tracing.ipynb](7_source_tracing.ipynb): Facility and chemical source attribution
- [notebooks-figures](notebooks-figures): Figure generation notebooks
- [utils](utils): Shared helper functions
- [environment.yml](environment.yml): Conda environment definition

## System Requirements

This workflow was executed on Linux-based HPC systems (University of Minnesota MSI). Required Python packages are listed in [environment.yml](environment.yml).

## Data Release

1. Study area boundary (county level): https://s3.msi.umn.edu/ejwater/results/aoi_county_boundaries.gpkg
2. Study area boundary (HUC-12 subwatershed units): https://s3.msi.umn.edu/ejwater/results/aoi_huc12_boundaries.gpkg
3. Disparity ratios by demographic group (2008 to 2012): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2008_2012.csv
4. Disparity ratios by demographic group (2013 to 2017): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2013_2017.csv
5. Disparity ratios by demographic group (2018 to 2022): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2018_2022.csv
6. Socioeconomic and demographic characteristics of HUC-12 subwatershed units: https://s3.msi.umn.edu/ejwater/results/huc12_demographics.csv
7. Toxicity-weighted concentrations for HUC-12 subwatershed units: https://s3.msi.umn.edu/ejwater/results/huc12_rsei_toxconc_weighted.csv
8. Descriptive statistics of toxic concentration exposure footprints: https://s3.msi.umn.edu/ejwater/results/toxconc_descriptive_stats.csv
9. T-test statistics comparing impacted and non-impacted subwatersheds: https://s3.msi.umn.edu/ejwater/results/toxconc_ttest_stats.csv
10. Chemicals contributing to toxic water pollution in the study area: https://s3.msi.umn.edu/ejwater/results/source_chemicals.csv
11. Industrial facilities identified as pollution sources: https://s3.msi.umn.edu/ejwater/results/source_facilities.csv
