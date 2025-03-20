#####Author: Beatriz Vinha
#####contact: beatrizmouravinha@ub.edu

#####This code is used to find out the most appropriate Sampling Unit (SU) area 
#####for ecological analysis, based on species accumulation curves. 
#####It creates a species matrix, with species abundances in each SU and
#####it also calculates the proportion of each substrate type category in each SU.

#####To run this code, you will need:
#####1. Video transect polygons, as a shapefile, divided by different SU sizes
#####2. Species annotations, as a points shapefile, 
#####created from "species_annotations.csv" after running "01_PostAnnotation_GeoreferenceAnnotations.ipynb")
#####3. Substrate type annotations, as a points shapefile,
#####created from "substrate_type_annotations.csv" after running "01_PostAnnotation_GeoreferenceAnnotations.ipynb")


#####The final output consists of:
#####1. A species matrix, based on abundance data, that can be used for ecological analysis
#####2. Species accumulation curves for the different SU sizes
#####3. A dataframe with the proportions of each substrate type category in each SU

#load libraries
#if needed, run install.packages("sf")
library(raster)
library(rgdal)
library(sf)
library(dplyr)
library(ggplot2)
library(BiodiversityR)
library(fossil)
library(vegan)

########1. Import data########
#load species annotations and video transects divided with different SUs sizes
#Here, as example, testing for SUs of 20m2, 50m2 and 100 m2
species <- shapefile("species_data.shp")
transect_SU_20 <- shapefile("video_transect_SU_20m2.shp")
transect_SU_50 <- shapefile("video_transect_SU_50m2.shp") 
transect_SU_100 <- shapefile("video_transect_SU_100m2.shp") 

#convert to sf object for spatial operations
species_sf <- st_as_sf(species)
transect_SU_20_sf <- st_as_sf(transect_SU_20)
transect_SU_50_sf <- st_as_sf(transect_SU_50)
transect_SU_100_sf <- st_as_sf(transect_SU_100)

#ensure all shapefiles have the same Coordinate Reference System (CRS)
transect_SU_20_sf <- st_transform(transect_SU_20_sf, crs = st_crs(species_sf))
transect_SU_50_sf <- st_transform(transect_SU_50_sf, crs = st_crs(species_sf))
transect_SU_100_sf <- st_transform(transect_SU_100_sf, crs = st_crs(species_sf))

########2. Extract species data for each SU########
#join species data and SUs ("POLY_ID" column in transects data) 
#based on intersection with the polygons.
#keep only species that intersect with the SUs (left = FALSE).
species_SU_20 <- st_join(species_sf, transect_SU_20_sf["POLY_ID"], left = FALSE)
species_SU_50 <- st_join(species_sf, transect_SU_50_sf["POLY_ID"], left = FALSE)
species_SU_100 <- st_join(species_sf, transect_SU_100_sf["POLY_ID"], left = FALSE)

#Count number of species in each SU
species_count_SU20 <- species_SU_20 %>%
  group_by(POLY_ID, label_name) %>%
  summarize(count = n()) %>%   
  ungroup()

species_count_SU50 <- species_SU_50 %>%
  group_by(POLY_ID, label_name) %>%
  summarize(count = n()) %>%   
  ungroup()

species_count_SU100 <- species_SU_100 %>%
  group_by(POLY_ID, label_name) %>%
  summarize(count = n()) %>%   
  ungroup()

#convert to summarized data (species counts) to a dataframe
species_count_SU20 <- as.data.frame(st_drop_geometry(species_count_SU20))
species_count_SU50 <- as.data.frame(st_drop_geometry(species_count_SU50))
species_count_SU100 <- as.data.frame(st_drop_geometry(species_count_SU100))

########3. Create species matrix########
#transform species count data into matrices where rows represent species and 
#columns represent SUs.This format is required for biodiversity analysis such 
#as species accumulation curves.

spe_SU20_matrix <- t(create.matrix(
  species_count_SU20,
  tax.name="label_name", #species labels column
  locality="POLY_ID", #SU identifier column
  time.col=NULL,
  time=NULL, 
  abund=TRUE, #Using abundance data - change if using PA data
  abund.col="count")) #column with abundance data

spe_SU50_matrix <- t(create.matrix(
  species_count_SU50,
  tax.name="label_name",
  locality="POLY_ID",
  time.col=NULL,
  time=NULL, 
  abund=TRUE,
  abund.col="count"))

spe_SU100_matrix <- t(create.matrix(
  species_count_SU100,
  tax.name="label_name",
  locality="POLY_ID",
  time.col=NULL,
  time=NULL, 
  abund=TRUE,
  abund.col="count"))

########4. Generate species accumulation curves########
#use species accumulation curves to evaluate species richness as a function of sampling effort (SUs).
#here, accumulation curves are generated for each SU size (20m², 50m², 100m²).
accum_curve_SU20 <- vegan::specaccum(spe_SU20_matrix, method = "random")
accum_curve_SU50 <- vegan::specaccum(spe_SU50_matrix, method = "random")
accum_curve_SU100 <- vegan::specaccum(spe_SU100_matrix, method = "random")

#Convert to curves to a data frame to plot using ggplot
accum_curve_SU20_df <- data.frame(Sampling_Units = 1:length(accum_curve_SU20$richness),
                                  Species_Richness = accum_curve_SU20$richness,
                                  SD = accum_curve_SU20$sd,
                                  Area = "20 m²")

accum_curve_SU50_df <- data.frame(Sampling_Units = 1:length(accum_curve_SU50$richness),
                            Species_Richness = accum_curve_SU50$richness,
                            SD = accum_curve_SU50$sd,
                            Area = "50 m²")

accum_curve_SU100_df <- data.frame(Sampling_Units = 1:length(accum_curve_SU100$richness),
                             Species_Richness = accum_curve_SU100$richness,
                             SD = accum_curve_SU100$sd,
                             Area = "100 m²")

#combine the data frames for different SU sizes into one for plotting
accum_curves_combined <- bind_rows(accum_curve_SU20_df, 
                                   accum_curve_SU50_df, 
                                   accum_curve_SU100_df) #add df if using more SU sizes

#plot the species accumulation curves using ggplot
#you can adjust the plot according to your preferences for visualization
sps_curves <- ggplot(accum_curves_combined, 
                     aes(x = Sampling_Units, y = Species_Richness, color = Area)) +
  geom_line(size = 1.2) +  
  geom_ribbon(aes(ymin = Species_Richness - SD, ymax = Species_Richness + SD, fill = Area), alpha = 0.2) +  # Confidence interval
  labs(x = "Number of Sampling Units (SU)", 
       y = "Species Richness", 
       title = "Species Accumulation Curves",
       color = "Sampling Unit (SU) Area", fill = "Sampling Unit (SU) Area") +
  theme_classic() + 
  scale_color_manual(values = c("blue", "red", "green")) +  #Add same number of colors as SUs to test
  scale_fill_manual(values = c("lightblue", "pink", "lightgreen"))  ##Add same number of colors as SUs to test

sps_curves

########5. Calculate substrate type proportions/SU (optional)#######
#once the appropriate SU is determined for your study, 
#you can calculate the proportions (%) of substrate type categories in each SU

#import substrate type shapefile
substrate_type <- shapefile("substrate_type_annotations.shp")
substrate_type_sf <- st_as_sf(substrate_type)

#ensure CRS matches the species data (if needed).
substrate_type_sf <- st_transform(substrate_type_sf, crs = st_crs(species_sf))

#keep only intersecting points to make sure that the points that were discarded from 
#the final video transect are not kept on the substrate type layer 
intersecting_points <- st_intersects(substrate_type_sf, transect_SU_20_sf, sparse = FALSE) #check which points intersect between both layers 
substrate_type_clean <- substrate_type_sf[apply(intersecting_points, 1, any), ] #filter those points

#export clean substrate type data, as a shapefile
#this will be useful for data visualization
write_sf(substrate_type_clean, "substrate_type_clean.shp")

#Join substrate type with SU polygons
substrate_SU_20 <- st_join(substrate_type_clean, transect_SU_20_sf["POLY_ID"], left = FALSE)

#Calculate the percentage of each Substrate type category in each SU
substrate_perc_SU20 <- substrate_SU_20 %>%
  group_by(POLY_ID, label_hier) %>%     #change to column name with subs type categories 
  summarize(count = n()) %>%                      
  mutate(total = sum(count),                      
         percentage = (count / total) * 100) %>%   
  ungroup()                                     
