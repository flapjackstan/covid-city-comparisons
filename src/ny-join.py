# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:35:32 2020

@author: elmsc
"""
#%%
import pandas as pd
import geopandas as gpd

#%%

import os
os.chdir('C:/Users/elmsc/Documents/gis/che-lab/covid-city-comparisons')

#%% GRAB CDC VARS THAT WERE APPORTIONED IN ARCMAP IN A PREVIOUS STUDY

ny_cdc = pd.read_csv('data/csv/ny_zcta.csv')
ny_cdc = ny_cdc[['GEOID_ZIP', 'AVG_ASTHMA', 'AVG_SMOKING','AVG_DIABETES', 'AVG_MHLTH', 'AVG_OBESITY', 'AVG_PHLTH']]

#%% READ, JOIN, AND OUTPUT DATA

ny = pd.read_csv('output/csv/ny++.csv')
ny = pd.merge(ny,ny_cdc, how='left', left_on='ZCTA', right_on='GEOID_ZIP')
ny.to_csv('output/csv/ny19++.csv')
