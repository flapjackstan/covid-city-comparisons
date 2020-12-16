library(tidyverse)
library(sf)
library(tmap)

setwd("C:/Users/elmsc/Documents/gis/che-lab/covid-city-comparisons")

#############################[DATA]#####################################

ny <- read_csv("output/csv/ny18++.csv")
la <- read_csv("output/csv/NCU18++.csv")

#############################[GEOGRAPHIES]#####################################

ny_shp <- st_read("data/shp/bor_zip_codes.shp")
ny_shp <- ny_shp %>% select(ZCTA5CE10,boro_code_)

la_shp <- st_read("data/shp/NCU_final.shp")
la_shp <- la_shp %>% select(COMTY_NAME)

#############################[JOINS]#####################################

la <- merge(la_shp,la, by.x='COMTY_NAME', by.y = "COMMUNITY", all.x = TRUE)
tm_shape(la) + tm_polygons()

ny <- merge(ny_shp, ny, by.x= "ZCTA5CE10", by.y='ZCTA', all.x = TRUE)
tm_shape(ny) + tm_polygons()

#############################[SIZE COMPARISON]#####################################

Area_Equidistant <- "+proj=eqdc +lat_0=0 +lon_0=0 +lat_1=33 +lat_2=45 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m no_defs"

ny <- ny %>% mutate(m2 = st_transform(ny, Area_Equidistant) %>% st_area())
la <- la %>% mutate(m2 = st_transform(la, Area_Equidistant) %>% st_area())

ny <- ny %>% mutate(km2 = m2/1e+6)
la <- la %>% mutate(km2 = m2/1e+6)

mean(ny$m2) / 1e+6
sum(ny$m2) / 1e+6

mean(la$m2) / 1e+6
sum(la$m2) / 1e+6


#############################[TRANSFORMATIONS]#####################################

ny <- ny %>% mutate(WHITE_P = NH_WHITE/TOTAL_POP)
ny <- ny %>% mutate(MINORITY_COMMUNITY = case_when(WHITE_P < .5 ~ 1, TRUE ~ 0))
ny <- ny %>% mutate(OVER_55 = `AGE_55_59`+`AGE_60_64`+`AGE_65_74`+`AGE_75_84`+`AGE_85+`,
                    POP_DENSITY = TOTAL_POP/km2)


la <- la %>% mutate(WHITE_P = NH_WHITE/TOTAL_POP)
la <- la %>% mutate(MINORITY_COMMUNITY = case_when(WHITE_P < .5 ~ 1, TRUE ~ 0))
la <- la %>% mutate(OVER_55 = `AGE_55_59`+`AGE_60_64`+`AGE_65_74`+`AGE_75_84`+`AGE_75_84`+`AGE_85+`,
                    POP_DENSITY = TOTAL_POP/km2)

#############################[REGRESSIONS]#####################################

ny_mod <- lm(AVG_PHLTH~ MINORITY_COMMUNITY+MEDIAN_INCOME+avg_ppl_per_household, data=ny)
summary(ny_mod)

ny_covid <- lm(`4_16_2020_positive_rate`~ AVG_PHLTH + POP_DENSITY + UNINSURED +OVER_55, data=ny)
summary(ny_covid)

la_mod <- lm(PHLTH~ MINORITY_COMMUNITY+MEDIAN_INCOME+avg_ppl_per_household, data=la)
summary(la_mod)

la_covid <- lm(`Case_Rat_1`~ PHLTH + POP_DENSITY + UNINSURED +OVER_55, data=la)
summary(la_covid)

#############################[NY MAPS]#####################################

positive_rate <- tm_shape(ny) + tm_polygons(col = "4_16_2020_positive_rate", style = "jenks", title = "COVID Test  Positive Rate\nApril 16, 2020")
map_covid <- positive_rate + tm_layout(scale = 1, frame = FALSE)
map_covid

minority <- tm_shape(ny) + tm_polygons(col = "MINORITY_COMMUNITY",n=2,labels = c("White", "Minority"), title = "White and Minority\nZipcodes")
map_minority <- minority + tm_layout(scale = 1, frame = FALSE)
map_minority

phlth <- tm_shape(ny) + tm_polygons(col = "AVG_PHLTH",style = "jenks", title = "CDC Estimated\nNegative Indications\nof Physical Health")
map_phlth <- phlth + tm_layout(scale = 1, frame = FALSE)
map_phlth

map <- tmap_arrange(map_minority, map_phlth)
map

map <- tmap_arrange(map_minority, map_covid)
map

#############################[LA MAPS]#####################################

minority <- tm_shape(la) + tm_polygons(col = "MINORITY_COMMUNITY",n=2,labels = c("White", "Minority"), title = "White and Minority\nNeighborhoods")
map_minority <- minority + tm_layout(scale = 1, frame = FALSE)
map_minority

phlth <- tm_shape(la) + tm_polygons(col = "PHLTH",style = "jenks", title = "CDC Estimated\nNegative Indications\nof Physical Health")
map_phlth <- phlth + tm_layout(scale = 1, frame = FALSE)
map_phlth

positive_rate <- tm_shape(la) + tm_polygons(col = "Case_Rat_1", style = "jenks", title = "COVID Positive Rate\nJuly 27, 2020")
map_covid <- positive_rate + tm_layout(scale = 1, frame = FALSE)
map_covid

map <- tmap_arrange(map_minority, map_phlth)
map

map <- tmap_arrange(map_minority, map_covid)
map
