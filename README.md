# LA-NY COVID-19 Comparison Study
![alt text](images/la-ny.png)

## Study Overview
This is a cross-sectional study over New York City and Los Angeles city exploring the characteristics between the two geographies through a public health lens. This study is ongoing and the methods used are still being refined. The general purpose of this study is to identify characteristics that are present in both cities and to investigate the notion of vulnerability within communities of color whom are generally at higher risk of poorer physical health conditions and thus at a higher risk of contracting COVID19.

## Challenges
Public health departments from both cities are publishing data at different geography levels and make it challenge to make direct comparisons. Additionally, because most variables of interest (Census Demographics and CDC Health Estimates) are published at smaller geographies, an apportionment method is required to aggregate up to target geographies. This methodology has its own drawbacks that are still being evaluated if suitable for this study. In addition reviewing spatial methods, other data sources are being considered for more accurate data.

## Initial Findings

Within both geographies, poor physical health is significantly present within communities of color and in turn have significant associations with COVID19 positive case rates when taking into account insured persons and people over the age of 55, and average number of people per household. Various other variables are still being analyzed, however, differnces in geography and data aggregation prove to be a larger challenge that requires more time to fully understand. 

![alt text](images/ny-minority-phlth.png)
![alt text](images/ny-minority-covid.png)


![alt text](images/la-minority-phlth.png)
![alt text](images/la-minority-covid.png)

## Replication

In order to replicate this study you must run below programs in order.

- `census-api.py` (pulls data from census api)
- `la-apportionment.py` (apportions census tract variables to neighborhood geography)
- `ny-join.py` (joins previously gathered NY data and census variables)
- `compare.r` (analysis and visualization)


## To Do

- Implement fixed effects model
