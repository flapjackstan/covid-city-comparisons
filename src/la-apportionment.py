"""
Created on Tue Dec 15 18:43:25 2020

This script apportions LA city tracts to the LA neighborhood geography by
using the intersection of the datasets and calculates census variables based on
geography size.

THIS APPORTIONMENT METHOD IS STILL UNDER REVIEW. 
SOME ISSUES IVE FOUND IS THAT SOME VARIABLES DONT ALLIGN WITH SOME OF
THE NUMBERS TRACKED BY LA TIMES WHICH SEEMS TO BE A RELIABLE SOURCE 

http://maps.latimes.com/neighborhoods/


@author: elmsc
"""
#%%
import pandas as pd
import geopandas as gpd

#%%

import os
os.chdir('C:/Users/elmsc/Documents/gis/che-lab/covid-city-comparisons')

#%% READ AND CLEAN LA DATA 

la = pd.read_csv('output/csv/la++.csv')

# remove tracts with no population, median income, and ppl per household
# not removing them throws off the apportionment and under estimates variables
la = la[la.TOTAL_POP > 0]
la = la[la.MEDIAN_INCOME > 0]
la = la[la.avg_ppl_per_household > 0]

# another way to handle this issue is to set the variables to 0 or 1
# la['MEDIAN_INCOME'] = la['MEDIAN_INCOME'].apply(lambda x: 0 if x < 0 else x)
# la['avg_ppl_per_household'] = la['avg_ppl_per_household'].apply(lambda x: 1 if x < 0 else x)

#%% READ AND JOIN CDC COMORBIDITIES

la_cdc = pd.read_csv('data/csv/cdc_comorbidities_2016.csv')
la_cdc = la_cdc[la_cdc['StateAbbr'] == 'CA']

cols = ['TractFIPS','PHLTH_CrudePrev', 'MHLTH_CrudePrev', 'DIABETES_CrudePrev', 'CASTHMA_CrudePrev', 
        'BPHIGH_CrudePrev', 'CHD_CrudePrev', 'OBESITY_CrudePrev']

la = pd.merge(la,la_cdc[cols], left_on='GEOID', right_on='TractFIPS', how='left')
la['GEOID'] = '0' + la['GEOID'].astype(str)

#%% READ AND JOIN TRACT GEOMETRY 

la_tracts = gpd.read_file('data/shp/la_tracts.shp')

cols = range(13,33)
la_tracts.columns[cols]
la_tracts = la_tracts.drop(la_tracts.columns[cols],axis=1)

la = pd.merge(la_tracts,la,on='GEOID', how='left')

# convert to pcrs that calculates meters
la = la.to_crs("+proj=cea +lat_0=35.68250088833567 +lon_0=139.7671 +units=m")
la.plot()

#%% INTERSECT GEOGRAPHIES 

ncu = gpd.read_file('data/shp/NCU_final.shp')

ncu = ncu.to_crs(la.crs)
ncu.crs=la.crs

ncu = ncu.rename(columns={'COMTY_NAME': 'COMMUNITY'})
cols = ['COMMUNITY', 'cases', 'case_rate', 'deaths', 'death_rate', 'Date',
        'Cases_1', 'Case_Rat_1', 'Deaths_1', 'Death_Ra_1', 'COVID19__2','geometry']
ncu = ncu.drop_duplicates('COMMUNITY', keep='first')

# required for apportionment
la['tracts_meters'] = la.area

intersection = gpd.overlay(la,ncu[cols], how='intersection')

# required for apportionment
intersection['intersect_meters'] = intersection.area

intersection.plot()

#%% APPORTION

# apportionment formula: variable * (intersected geography/size of geography with variables)
def apportion_variable(df,var):
    df['intersect_'+var] = df[var] * (df['intersect_meters']/ df['tracts_meters'])
    return df

#%% APPORTION ALL VARIABLES

cols = range(13,76)
intersection.columns[cols]

for i in intersection.columns[cols]:
    print(i)
    intersection = apportion_variable(intersection, i)
    
#%% DEFINE WHAT NEEDS TO BE AVERAGED AND SUMMED

means = ['intersect_PHLTH_CrudePrev', 'intersect_MHLTH_CrudePrev',
       'intersect_DIABETES_CrudePrev', 'intersect_CASTHMA_CrudePrev',
       'intersect_BPHIGH_CrudePrev', 'intersect_CHD_CrudePrev',
       'intersect_OBESITY_CrudePrev','intersect_MEDIAN_INCOME', 'intersect_avg_ppl_per_household']

sums = ['intersect_TOTAL_POP','intersect_NH_BLACK', 'intersect_NH_NATIVE', 'intersect_NH_ASIAN',
       'intersect_NH_HAWAIIAN', 'intersect_NH_OTHER_RACE',
       'intersect_NH_TWO_OR_MORE', 'intersect_NH_HISPANIC_LATINO',
       'intersect_US_BORN', 'intersect_NATURALIZED',
       'intersect_NON_CITIZEN', 'intersect_TOTAL_HOUSING',
       'intersect_OWNER_OCCUPIED', 'intersect_RENTER_OCCUPIED',
       'intersect_AGE_55_59', 'intersect_AGE_60_64',
       'intersect_AGE_65_74', 'intersect_AGE_75_84', 'intersect_AGE_85+',
       'intersect_MALE', 'intersect_FEMALE', 'intersect_ED_POP_25+',
       'intersect_LESS_THAN_9TH', 'intersect_LESS_THAN_HS',
       'intersect_HS_OR_GED', 'intersect_SOME_COLLEGE',
       'intersect_ASSOCIATES', 'intersect_BACHELORS',
       'intersect_GRAD_OR_PROFESSIONAL', 'intersect_HEALTH_COVERAGE_POP',
       'intersect_INSURED', 'intersect_UNINSURED', 'intersect_LABOR_FORCE_POP_16+',
       'intersect_EMPLOYED', 'intersect_UNEMPLOYED', 'intersect_BUSINESS',
       'intersect_SERVICE', 'intersect_SALES_OFFICE',
       'intersect_CONSTRUCTION_MAINTENANCE',
       'intersect_PRODUCTION_TRANSPORTATION', 'intersect_LANGUAGE_POP_5+',
       'intersect_ENGLISH_ONLY', 'intersect_OTHER_LANGUAGE',
       'intersect_OTHER_LANGUAGE_POOR_ENGLISH', 'intersect_2_ppl_fam',
       'intersect_3_to_4_ppl_fam', 'intersect_5_to_6_ppl_fam', 'intersect_GT_7_ppl_fam']

#%% KEEP ONLY THE NECESSARY COLUMNS FOR ANALYSIS


cols = ['COMMUNITY', 'cases', 'case_rate', 'deaths', 'death_rate', 'Date',
         'Cases_1', 'Case_Rat_1', 'Deaths_1', 'Death_Ra_1', 'COVID19__2','geometry']

ncu = ncu[cols]

#%%


for i in sums:
    print(i)
    agg = intersection.groupby("COMMUNITY").agg({i: ["sum"]})
    agg.reset_index(drop=False, inplace=True)
    agg.columns = ['COMMUNITY', i]
    ncu = pd.merge(ncu,agg,how='left', on='COMMUNITY')

for i in means:
    print(i)
    agg = intersection.groupby("COMMUNITY").agg({i: ["mean"]})
    agg.reset_index(drop=False, inplace=True)
    agg.columns = ['COMMUNITY', i]
    ncu = pd.merge(ncu,agg,how='left', on='COMMUNITY')

ncu = ncu.rename(columns={'MEDIAN_INCOME_b': 'MEDIAN_INCOME'})
ncu.columns = ncu.columns.str.replace('intersect_', '')
ncu.columns = ncu.columns.str.replace('_CrudePrev', '')

ncu = ncu.drop_duplicates('COMMUNITY', keep='first')

ncu.drop('geometry', axis=1).to_csv('output/csv/NCU18++.csv')
intersection.drop('geometry', axis=1).to_csv('output/csv/intersected_tracts.csv', index=False)

ncu.to_file('output/shp/NCU18++.shp', driver="ESRI Shapefile")
