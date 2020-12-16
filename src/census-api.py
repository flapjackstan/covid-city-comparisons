"""
Created on Tue Dec 15 18:43:25 2020

This script allows you to download census variables from respective
subject, profile and narrative tables via API.

@author: elmsc
"""

#%%
import pandas as pd
import censusdata

#%%

import os
os.chdir('C:/Users/elmsc/Documents/gis/che-lab/covid-city-comparisons')

#%% EXPLORE 

# censusdata.printtable(censusdata.censustable('acs5', 2018, 'B23025')) # employment status
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'B15003')) # educational attainment
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'B19013')) # median income
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'B03002')) # race (hispanic origin)

# censusdata.printtable(censusdata.censustable('acs5', 2018, 'DP02')) # social characteristics
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'DP03')) # economic characteristics
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'DP04')) # housing characteristics
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'DP05')) # demographic characteristics

# censusdata.printtable(censusdata.censustable('acs5', 2018, 'S2701')) # social characteristics

# censusdata.printtable(censusdata.censustable('acs5', 2018, 'S0501')) # demographic characteristics
# censusdata.printtable(censusdata.censustable('acs5', 2018, 'B05001')) # citizenship

# censusdata.search('acs5', 2018, field='label', criterion='Civilian employed population 16 years and over', tabletype='subject')
# #censusdata.search('acs5', 2018, field='name', criterion='S', tabletype='subject')

#%% STORE CENSUS ID AND DESIRED VARIABLE NAME 

# https://api.census.gov/data/2018/acs/acs5/groups.html

census_dict = {}
census_dict['B03002_001E'] = 'TOTAL_POP'
census_dict['B03002_003E'] = 'NH_WHITE'
census_dict['B03002_004E'] = 'NH_BLACK'
census_dict['B03002_005E'] = 'NH_NATIVE'
census_dict['B03002_006E'] = 'NH_ASIAN'
census_dict['B03002_007E'] = 'NH_HAWAIIAN'
census_dict['B03002_008E'] = 'NH_OTHER_RACE'
census_dict['B03002_009E'] = 'NH_TWO_OR_MORE'
census_dict['B03002_012E'] = 'NH_HISPANIC_LATINO'

census_dict['B05001_002E'] = 'US_BORN'
census_dict['B05001_005E'] = 'NATURALIZED'
census_dict['B05001_006E'] = 'NON_CITIZEN'

#%% SAME AS ABOVE, HOWEVER DIFFERENT CENSUS TABLES NEED DIFFERENT API CALLS

# https://api.census.gov/data/2018/acs/acs5/profile/groups.html

profile_dict = {}
profile_dict['DP04_0045E'] = 'TOTAL_HOUSING'
profile_dict['DP04_0046E'] = 'OWNER_OCCUPIED'
profile_dict['DP04_0047E'] = 'RENTER_OCCUPIED'

profile_dict['DP05_0013E'] = 'AGE_55_59'
profile_dict['DP05_0014E'] = 'AGE_60_64'
profile_dict['DP05_0015E'] = 'AGE_65_74'
profile_dict['DP05_0016E'] = 'AGE_75_84'
profile_dict['DP05_0017E'] = 'AGE_85+'

profile_dict['DP05_0002E'] = 'MALE'
profile_dict['DP05_0003E'] = 'FEMALE'

profile_dict['DP02_0058E'] = 'ED_POP_25+'
profile_dict['DP02_0059E'] = 'LESS_THAN_9TH'
profile_dict['DP02_0060E'] = 'LESS_THAN_HS'
profile_dict['DP02_0061E'] = 'HS_OR_GED'
profile_dict['DP02_0062E'] = 'SOME_COLLEGE'
profile_dict['DP02_0063E'] = 'ASSOCIATES'
profile_dict['DP02_0064E'] = 'BACHELORS'
profile_dict['DP02_0065E'] = 'GRAD_OR_PROFESSIONAL'

profile_dict['DP03_0095E'] = 'HEALTH_COVERAGE_POP'
profile_dict['DP03_0096E'] = 'INSURED'
profile_dict['DP03_0099E'] = 'UNINSURED'

profile_dict['DP03_0062E'] = 'MEDIAN_INCOME'

profile_dict['DP03_0003E'] = 'LABOR_FORCE_POP_16+'
profile_dict['DP03_0004E'] = 'EMPLOYED'
profile_dict['DP03_0005E'] = 'UNEMPLOYED'

profile_dict['DP03_0027E'] = 'BUSINESS'
profile_dict['DP03_0028E'] = 'SERVICE'
profile_dict['DP03_0029E'] = 'SALES_OFFICE'
profile_dict['DP03_0030E'] = 'CONSTRUCTION_MAINTENANCE'
profile_dict['DP03_0031E'] = 'PRODUCTION_TRANSPORTATION'

profile_dict['DP02_0110M'] = 'LANGUAGE_POP_5+'
profile_dict['DP02_0111E'] = 'ENGLISH_ONLY'
profile_dict['DP02_0112E'] = 'OTHER_LANGUAGE'
profile_dict['DP02_0113E'] = 'OTHER_LANGUAGE_POOR_ENGLISH'

#%% SAME AS ABOVE

# https://api.census.gov/data/2018/acs/acs5/subject/groups/S1702.html

subject_dict = {}

subject_dict['S1901_C01_012E'] = 'MEDIAN_INCOME_2'

subject_dict['S1702_C01_032E'] = '2_ppl_fam'
subject_dict['S1702_C01_033E'] = '3_to_4_ppl_fam'
subject_dict['S1702_C01_034E'] = '5_to_6_ppl_fam'
subject_dict['S1702_C01_035E'] = 'GT_7_ppl_fam'
subject_dict['S1101_C01_002E'] = 'avg_ppl_per_household'


#%% TURN INTO DATAFRAME FOR EASIER RENAME LATER

names_df = pd.DataFrame.from_dict(census_dict, orient='index')
names_df = names_df.reset_index()
names_df.columns = ['key', 'value']

profile_names_df = pd.DataFrame.from_dict(profile_dict, orient='index')
profile_names_df = profile_names_df.reset_index()
profile_names_df.columns = ['key', 'value']

subject_names_df = pd.DataFrame.from_dict(subject_dict, orient='index')
subject_names_df = subject_names_df.reset_index()
subject_names_df.columns = ['key', 'value']

#%% CLEAN CENSUS

# grabs GEOID variables from single joined column
def get_tract_geoid(df):
    df = df.reset_index()
    df = df.rename(columns={"index": "id"})
    
    geoid = df[['id']].astype(str)
    geoid = geoid['id'].str.split(":",expand=True)
    geoid = geoid[[3,4,5]]
    geoid.columns = ['STATE', 'COUNTY', 'TRACT']
    geoid['STATE'] = geoid['STATE'].str.replace('> county','', regex=False)
    geoid['COUNTY'] = geoid['COUNTY'].str.replace('> tract','', regex=False)
    geoid['GEOID'] = geoid['STATE'] + geoid['COUNTY'] + geoid['TRACT']
    
    df = pd.concat([df,geoid], axis=1)
    
    return df

# renames all census variables according to dictionary 
def census_clean(df, names_df, geoid):
    
    names_df = names_df.append({'key': geoid, 'value' : geoid}, ignore_index=True)
    
    # selects the columns you want
    df = df[names_df['key']]
    
    for i in range(0,len(names_df['key'])):
        df = df.rename(columns = {names_df['key'][i]:names_df['value'][i]})
    del(i)
    
    return df

# grabs ZCTA variable from single joined column
def get_zcta(df):
    df = df.reset_index()
    df = df.rename(columns={"index": "id"})
    
    geoid = df[['id']].astype(str)
    geoid = geoid['id'].str.split(":",expand=True)
    geoid = geoid[[3]]
    geoid.columns = ['ZCTA']
    
    df = pd.concat([df,geoid], axis=1)
    
    return df

#%% DOWNLOAD DATA

la = censusdata.download('acs5', 2018, censusdata.censusgeo([('state', '06'),
                                                             ('county', '037'),
                                                             ('tract', '*')]),
                         names_df['key'].to_list())

la_profile = censusdata.download('acs5', 2018, censusdata.censusgeo([('state', '06'),
                                                             ('county', '037'),
                                                             ('tract', '*')]),
                         profile_names_df['key'].to_list(),tabletype='profile')

la_subject = censusdata.download('acs5', 2018, censusdata.censusgeo([('state', '06'),
                                                             ('county', '037'),
                                                             ('tract', '*')]),
                         subject_names_df['key'].to_list(),tabletype='subject')

#%% CLEAN AND JOIN DATA FOR LA

la = get_tract_geoid(la)
la = census_clean(la,names_df,'GEOID')

la_profile = get_tract_geoid(la_profile)
la_profile = census_clean(la_profile,profile_names_df,'GEOID')

la_subject = get_tract_geoid(la_subject)
la_subject = census_clean(la_subject,subject_names_df,'GEOID')

la_census = pd.merge(la,la_profile,how='left',on='GEOID')

la_census = pd.merge(la_census,la_subject,how='left',on='GEOID')


#%% DOWNLOAD DATA
# Grab required borough ZCTAs to avoid downloading all ZCTAs in NY
zips = pd.read_csv('data/csv/ny_zcta.csv')
zips['GEOID_ZIP'] = zips[['GEOID_ZIP']].astype(str)
zips = zips['GEOID_ZIP'].to_list()
joined_string = ",".join(zips)

ny = censusdata.download('acs5', 2018, censusdata.censusgeo([('zip code tabulation area', joined_string)]),
                         names_df['key'].to_list())

ny_profile = censusdata.download('acs5', 2018, censusdata.censusgeo([('zip code tabulation area', joined_string)]),
                         profile_names_df['key'].to_list(),tabletype='profile')

ny_subject = censusdata.download('acs5', 2018, censusdata.censusgeo([('zip code tabulation area', joined_string)]),
                         subject_names_df['key'].to_list(),tabletype='subject')



#%% CLEAN AND JOIN DATA FOR NY

ny = get_zcta(ny)
ny = census_clean(ny,names_df,'ZCTA')


ny_profile = get_zcta(ny_profile)
ny_profile = census_clean(ny_profile,profile_names_df,'ZCTA')

ny_subject = get_zcta(ny_subject)
ny_subject = census_clean(ny_subject,subject_names_df,'ZCTA')

ny_census = pd.merge(ny,ny_profile,how='left',on='ZCTA')
ny_census = pd.merge(ny_census,ny_subject,how='left',on='ZCTA')

#%%

ny_census.to_csv('output/csv/ny++.csv')
la_census.to_csv('output/csv/la++.csv')
