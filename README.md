# **Disparity assessment in the distribution of toxic water pollution**

## **Project overview**

The objective of this project is to explore industrial water pollution exposure among communities adjacent to the Mississippi River. It involves a range of activities, including processing spatial data on polluting facilities and impaired water bodies, gathering socioeconomic data for communities of interest, estimating potential disparities in exposure to pollution, and visualizing the results.

## **System requirements**
This workflow was successfully executed on the University of Minnesota's Minnesota Supercomputing Institute (MSI) High Performance Computing (HPC) systems. Required Python packages are listed in the `environment.yml` file.

## **Data release**
- Study area boundary (county level): https://s3.msi.umn.edu/ejwater/results/aoi_county_boundaries.gpkg
- Study area boundary (HUC-12 subwatershed units): https://s3.msi.umn.edu/ejwater/results/aoi_huc12_boundaries.gpkg
- Pollution exposure disparity ratios by demographic group (2008–2012): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2008_2012.csv
- Pollution exposure disparity ratios by demographic group (2013–2017): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2013_2017.csv
- Pollution exposure disparity ratios by demographic group (2018–2022): https://s3.msi.umn.edu/ejwater/results/disparity_ratios_2018_2022.csv
- Socioeconomic and demographic characteristics of HUC-12 subwatershed units: https://s3.msi.umn.edu/ejwater/results/huc12_demographics.csv
- Toxicity-weighted concentrations for HUC-12 subwatershed units: https://s3.msi.umn.edu/ejwater/results/huc12_rsei_toxconc_weighted.csv
- Descriptive statistics of toxic concentration exposure footprints: https://s3.msi.umn.edu/ejwater/results/toxconc_descriptive_stats.csv
- T-test statistics comparing impacted and non-impacted subwatersheds: https://s3.msi.umn.edu/ejwater/results/toxconc_ttest_stats.csv
- Chemicals contributing to toxic water pollution in the study area: https://s3.msi.umn.edu/ejwater/results/source_chemicals.csv
- Industrial facilities identified as pollution sources: https://s3.msi.umn.edu/ejwater/results/source_facilities.csv