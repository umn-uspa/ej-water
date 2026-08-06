import pandas as pd

# these are demographic and socioeconomic variables of interest 
var_names = {
    'share_nonhsp_white': 'Non Hispanic White',
    'share_black': 'Black or African American',
    'share_native': 'American Indian and Alaska Native',
    'share_asian': 'Asian',
    'share_hispanic': 'Hispanic or Latino',
    'share_2_above_poverty': 'Twice Above Poverty',
    'share_below_poverty': 'Below Poverty'
}

# we compare racial/ethnic minorities to non hispanic white and poor to nonpoor
references = {
    'Non Hispanic White': None, # this IS a reference group
    'Black or African American': 'Non Hispanic White',
    'American Indian and Alaska Native': 'Non Hispanic White',
    'Asian': 'Non Hispanic White',
    'Hispanic or Latino': 'Non Hispanic White',
    'Twice Above Poverty': None, # this IS a reference group
    'Below Poverty': 'Twice Above Poverty'
}

def compute_weighted_exposure_stats(table, study_period='2018_2022', metric='2018_2022_TOXCONC'):
    # takes an input DataFrame with demographic data already filled in
    # metric of environmental burden - TOXCONC for RSEI and violation_intensity for NPDES
    exposures = {}
    for var_name, var_name_long in var_names.items():
        weighted = (table[f'{study_period}_{var_name}']*table[f'{study_period}_total']*table[metric]).sum()
        indicator = weighted/(table[f'{study_period}_{var_name}']*table[f'{study_period}_total']).sum()
        #print (var_name_long, f'{indicator:.2f}')
        exposures[var_name_long] = indicator
    result = pd.DataFrame(exposures.items(), columns=['Group', 'Weighted Exposure'])
    result['Reference Group'] = result['Group'].map(references)
    # compute ratio
    ref_exposure = result.set_index('Group')['Weighted Exposure']
    result['Disparity Ratio'] = result['Weighted Exposure'] / result['Reference Group'].map(ref_exposure)
    return result