#####Author: Beatriz Vinha
#####contact: beatrizmouravinha@ub.edu

#####This code is used to process spatial data to create a final video transect 
#####that represents the true annotated area during video analysis done in BIIGLE.
#####The code removes parts of the transect that were annotated to be discarded 
#####(e.g., low visibility, no lasers, etc.) and generates a clean transect that
#####represents the field of view considered during the video analysis stage.

#####To run this code, you will need:
#####1. The navigation file, as a points shapefile
#####2. The points to be removed from the navigation, as a shapefile 
#####(extracted as "transect_to_discard.csv") after running 
#####https://colab.research.google.com/github/bvinha/UB-Video-and-Image-Protocol/blob/main/01_PostAnnotation_GeoreferenceAnnotations.ipynb


#####The final output consists of:
#####1. A clean set of navigation points, without the areas annotated as to be discarded
#####2. A continuous line representing the valid transect path.
#####3. A polygon that represents the true video transect, based on a specified annotation width

#load libraries
#if needed, run install.packages("sf")
library(sf)
library(dplyr)

######1. Load shapefiles#######
#load shapefile with navigation points and 
# the shapefile indicating parts of the transect to be discarded (e.g., regions with bad data).

#Load navigation points shapefiles and the annotated parts of the video 
navigation_points <- st_read("rov_navigation.shp") #change name/directory
transect_to_discard <- st_read("transect_to_discard.shp") #change name/directory

######2. Reproject shapefiles to UTM CRS#######

#If your shapefile is a geographic CRS (degrees), you will need to reproject it
#to a coordinate reference system (CRS) that uses meters (e.g., UTM zones).
#If your shapefile is already in a CRS using meters as unit, ignore this step!

#Ensure you use the appropriate EPSG code for your area. 
#example: Catalan coast is in UTM Zone 31 (EPSG: 32631). 
#You can use the following websites to find your UTM zone and EPSG code:
#UTM zone map: https://mangomap.com/robertyoung/maps/69585/what-utm-zone-am-i-in-#
#EPSG codes: https://docs.up42.com/data/reference/utm

navigation_points_utm <- st_transform(navigation_points, crs = 32626)  #change EPSG code of your region
transect_to_discard_utm <- st_transform(transect_to_discard, crs = 32626)  #change EPSG code of your region

st_crs(navigation_points_utm) #check current CRS of the reprojected shapefile

######3. Remove points to discard from navigation#######

#add an ID column to order points
#this helps to create groups and preserve the order of nearby points
navigation_points <- navigation_points_utm %>% mutate(id = row_number())

#identify which navigation points intersect with the 'transect_to_discard' shapefile,
#to identify which points to remove from the final transect
intersections <- st_intersects(navigation_points, transect_to_discard_utm, sparse = FALSE)

clean_navigation <- navigation_points[!apply(intersections, 1, any), ]

#create a grouping variable that groups nearby points
clean_navigation <- clean_navigation %>%
  mutate(group = cumsum(c(0, diff(id) != 1)))

#Export the clean navigation points as a shapefile
st_write(clean_navigation, "01_clean_navigation_pts.shp")

######4. Create a line representing the clean navigation#######

#group nearby points into separate line segments
navigation_line <- clean_navigation %>%
  group_by(group) %>%
  summarize(do_union = FALSE) %>%
  st_cast("LINESTRING")

#remove invalid geometries, such as line segments made from a single point
#keep only valid LINESTRING geometries.
clean_navigation_line <- navigation_line %>%
  filter(st_is_valid(.) & st_geometry_type(.) == "LINESTRING") 

#dissolve all line segments into a single line object
nav_line <- st_union(clean_navigation_line)

##Export clean navigation, as a line shapefile
st_write(nav_line, "02_nav_line_clean.shp")


######5. Create final video transect representing the true video annotation area#######

#Create a polygon, where the width represents the field of view during video analysis.
#the buffer is created taking into account the center point
#so for a width of 1-meter wide transect, you would need to create a buffer of 0.5 m (0.5 m on each side of the line)

video_transect_buffer <- st_buffer(nav_line, dist = 0.5, endCapStyle = "ROUND", joinStyle = "ROUND") #adjust buffer distance in 'dist'

#Export final video transect polygon
st_write(video_transect_buffer, "03_video_transect_buffer.shp")
