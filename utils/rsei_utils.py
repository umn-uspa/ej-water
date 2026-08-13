"""Utilities for loading and aggregating RSEI data products."""

import pandas as pd
import geopandas as gpd
from utils.config import root_dir


def load_tabular_water_microdata(site="Onsite", universe="core01"):
    """Load zipped RSEI tabular water microdata for a release site and universe."""
    # these files are large, takes a minute to open
    return pd.read_csv(
        root_dir + f"data_input/rsei/NHDMicroResults_conc_agg{site}{universe}.zip",
        compression="zip",
    )


def load_rsei_flowlines(
    site="Onsite", year=2022, selection_aoi=None, universe="core01"
):
    """Load annual RSEI flowlines and optionally filter by area of interest."""
    # read a shapefile
    rsei_flowlines = gpd.read_file(
        f"zip://{root_dir}/data_input/rsei/NHDMicroResults_{site}{universe}_{year}.zip/NHDMicroResults_{site}{universe}_{year}.shp"
    )
    # select by area of interest if provided
    if selection_aoi is not None:
        # selection_aoi = selection_aoi.dissolve()
        rsei_flowlines = rsei_flowlines.sjoin(
            selection_aoi.to_crs(rsei_flowlines.crs), predicate="intersects"
        )[rsei_flowlines.columns]
        rsei_flowlines = rsei_flowlines.drop_duplicates(subset=["COMID", "REACHCODE"])
    # apply formatting to correctly interpret numerical columns
    rsei_flowlines["TOXCONC"] = rsei_flowlines["TOXCONC"].astype(float)
    rsei_flowlines["REACHCODE"] = rsei_flowlines["REACHCODE"].astype(int)
    return rsei_flowlines


def load_facility_data():
    """Load RSEI public-release facility, submission, NAICS, and chemical tables."""
    # rsei facility-level data
    releases_filepath = (
        root_dir
        + "data_input/rsei/RSEIv2312_Public_Release_Data/releases_data_rsei_v2312.csv"
    )
    releases = pd.read_csv(releases_filepath, low_memory=False)
    submissions_filepath = (
        root_dir
        + "data_input/rsei/RSEIv2312_Public_Release_Data/submissions_data_rsei_v2312.csv"
    )
    submissions = pd.read_csv(submissions_filepath, low_memory=False)
    facilities_filepath = (
        root_dir
        + "data_input/rsei/RSEIv2312_Public_Release_Data/facility_data_rsei_v2312.csv"
    )
    facilities = pd.read_csv(facilities_filepath, low_memory=False)
    naics_filepath = (
        root_dir
        + "data_input/rsei/RSEIv2312_Public_Release_Data/naics_data_rsei_v2312.csv"
    )
    naics = pd.read_csv(naics_filepath, low_memory=False)
    chemical_filepath = (
        root_dir
        + "data_input/rsei/RSEIv2312_Public_Release_Data/chemical_data_rsei_v2312.csv"
    )
    chemical = pd.read_csv(chemical_filepath, low_memory=False)
    return releases, submissions, facilities, naics, chemical


def aggregate_RSEI(years, selection_aoi=None, universe="core01", study_period_length=5):
    """Aggregate on-site and off-site flowline toxicity across study years."""
    rsei_list = []
    for year in years:
        # open rsei geographic microdata - flowlines
        rsei_onsite = load_rsei_flowlines(
            site="Onsite", year=year, selection_aoi=selection_aoi, universe=universe
        )
        rsei_offsite = load_rsei_flowlines(
            site="Offsite", year=year, selection_aoi=selection_aoi, universe=universe
        )
        # format TOXCONC field from string to numeric (float)
        cols = ["COMID", "REACHCODE", "TOXCONC", "geometry"]
        rsei_all_releases = pd.concat([rsei_onsite[cols], rsei_offsite[cols]])
        # sum up On- and Off- site discharges
        rsei_combined = rsei_all_releases.dissolve(
            ["COMID", "REACHCODE"], aggfunc="sum"
        ).reset_index()
        rsei_list.append(rsei_combined)
    # average over the 5-year study period
    rsei_all_years = pd.concat(rsei_list)
    rsei_aggregated = rsei_all_years.dissolve(
        ["COMID", "REACHCODE"], aggfunc="sum"
    ).reset_index()
    rsei_aggregated["TOXCONC"] = rsei_aggregated["TOXCONC"] / study_period_length
    return rsei_aggregated


def get_source_facilities(
    site, tabular_gm, aoi=None, universe="core01", years=range(2008, 2023)
):
    """Return ranked facilities contributing to selected flowline toxicity."""
    releases, submissions, facilities, naics, _ = load_facility_data()
    all_contributing_facs = []
    fac_columns = [
        "FacilityID",
        "FacilityName",
        "Latitude",
        "Longitude",
        "NAICS1",
        "Street",
        "City",
        "County",
        "State",
        "ZIPCode",
    ]
    ind_columns = ["2022NAICSCode", "TRIIndustrySector", "LongName"]
    for year in years:
        # read flowlines
        flowlines = load_rsei_flowlines(
            site=site, year=year, selection_aoi=aoi, universe=universe
        )
        # select year of interest
        tabular_gm_annual = tabular_gm[tabular_gm["Year"] == year]
        # Use MultiIndex for efficient filtering
        key_tuples = [tuple(x) for x in flowlines[["COMID", "REACHCODE"]].to_numpy()]
        selected = (
            tabular_gm_annual.set_index(["ComID", "ReachCode"])
            .loc[key_tuples]
            .reset_index()
        )
        # join tabular GM with facility-level data
        joined = selected[["ReleaseNumber", "ToxConc"]].merge(
            releases[["ReleaseNumber", "SubmissionNumber"]], on="ReleaseNumber"
        )
        joined = joined.merge(
            submissions[["SubmissionNumber", "FacilityID"]], on="SubmissionNumber"
        )
        joined = joined.merge(facilities[fac_columns], on="FacilityID")
        joined = joined.merge(
            naics[ind_columns], left_on="NAICS1", right_on="2022NAICSCode"
        )
        # print ("Got {0} unique facilities in {1}".format(len(joined["FacilityID"].unique()), year))
        contributing_facs = (
            joined.groupby(fac_columns + ind_columns).sum().reset_index()
        )
        all_contributing_facs.append(contributing_facs)
    # concatenate all facilities into a single table
    all_contributing_facs = pd.concat(all_contributing_facs)
    print(
        "Got {} unique facilities for the study period".format(
            len(all_contributing_facs["FacilityID"].unique())
        )
    )
    all_contributing_facs = (
        all_contributing_facs[fac_columns + ind_columns + ["ToxConc"]]
        .groupby(fac_columns + ind_columns)
        .sum()
        .reset_index()
    )
    all_contributing_facs.drop(columns=["NAICS1"], inplace=True)
    all_contributing_facs = all_contributing_facs.sort_values(
        by="ToxConc", ascending=False
    )
    return all_contributing_facs


def get_source_chemicals(
    site, tabular_gm, aoi=None, universe="core01", years=range(2008, 2023)
):
    """Return ranked chemicals contributing to selected flowline toxicity."""
    releases, submissions, _, _, chemical = load_facility_data()
    all_contributing_chems = []
    chem_columns = ["ChemicalNumber", "MetalCombinedChemNum", "Chemical"]
    for year in years:
        # read flowlines
        flowlines = load_rsei_flowlines(
            site=site, year=year, selection_aoi=aoi, universe=universe
        )
        # select year of interest
        tabular_gm_annual = tabular_gm[tabular_gm["Year"] == year]
        # Use MultiIndex for efficient filtering
        key_tuples = [tuple(x) for x in flowlines[["COMID", "REACHCODE"]].to_numpy()]
        selected = (
            tabular_gm_annual.set_index(["ComID", "ReachCode"])
            .loc[key_tuples]
            .reset_index()
        )
        # join tabular GM with facility-level data
        joined = selected[["ReleaseNumber", "ToxConc"]].merge(
            releases[["ReleaseNumber", "SubmissionNumber"]], on="ReleaseNumber"
        )
        joined = joined.merge(
            submissions[["SubmissionNumber", "ChemicalNumber"]], on="SubmissionNumber"
        )
        joined = joined.merge(chemical[chem_columns], on="ChemicalNumber")
        # print ("Got {0} unique chemicals in {1}".format(len(joined["ChemicalNumber"].unique()), year))
        contributing_chems = joined.groupby(chem_columns).sum().reset_index()
        all_contributing_chems.append(contributing_chems)
    # concatenate all facilities into a single table
    all_contributing_chems = pd.concat(all_contributing_chems)
    print(
        "Got {} unique chemicals for the study period".format(
            len(all_contributing_chems["ChemicalNumber"].unique())
        )
    )
    all_contributing_chems = (
        all_contributing_chems[chem_columns + ["ToxConc"]]
        .groupby(chem_columns)
        .sum()
        .reset_index()
    )
    all_contributing_chems = all_contributing_chems.sort_values(
        by="ToxConc", ascending=False
    )
    return all_contributing_chems
