# UB-Video-and-Image-Protocol

This repository contains scripts for processing video annotations for the characterization and mapping of marine benthic communities, used internally at the Departament of Ecology of the University of Barcelona. The scripts aim to georeference video annotations, clean up video transect paths, and determine the most appropriate Sampling Unit (SU) size for ecological analysis, based on species accumulation curves.

## Files Description

- **"01_PostAnnotation_GeoreferenceAnnotations.ipynb"** - Jupyter Notebook (available to run through Google Collab) to processes video annotations done in BIIGLE (biigle.de), combining timestamped annotations with video metadata, to calculate the exact time and georeference each annotation. It also creates continuous timestamped sequences to identify sections of the navigation for substrate type categories and for sections to be removed from the video transect (e.g., sampling, no visibility, etc.).
- **02_Create-VideoTransect.R** - R script to process spatial data to create a final "clean" video transect representing only the areas of interest that were valid during the video analysis stage. Discarded footage is removed to produce a continuous line representing the true video transect path and a polygon with the annotated field of view.
- **03_Determine-SU-size-Create-Species-Subs-matrix.R** - R script to calculate species accumulation curves to help determine the most appropriate Sampling Unit (SU) size for ecological analysis. It also generates a species abundance matrix and calculates substrate type proportions for each SU.

## Requirements

To run these scripts, the following software and packages are needed:

- **Jupyter Notebook** or **Google Collab** for `.ipynb` scripts
- **R** for `.R` scripts
    - Required R packages:
        - `sf`, `raster`, `rgdal`, `dplyr`, `ggplot2`, `BiodiversityR`, `fossil`, `vegan`


Feel free to modify and use the code for your research or projects.
