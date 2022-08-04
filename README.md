# Landsat Time-series Vegetation Recovery Analyses

## Introduction
This repository provides a pipeline to prepare a dense stack of Landsat imagery for time-series and regression analyses in order to quantify vegetation recovery using appropriate recovery metrics (based on Lawrence and Ripple, 2000; Pickell et al., 2016; White et al., 2017) at Unzen Volcano, Japan. Performing annual time-series analyses across different Landsat satellites requires some preprocessing steps to ensure appropriate continuity across different satellite sensors, derive vegetation indices, and obtain yearly values. By calculating recovery metrics to quantify vegetation recovery, we can get a better understanding of eruption effects on vegetation regrowth. 

## Features
This pipeline comprises two main parts:
1) Preprocessing and generating annual vegetation indices (get_veg_index)
2) Performing regression analysis and deriving recovery metrics to quantify vegetation recovery (post_processing)

The first part (get_veg_index) is to download, pre-process, and derive vegetation indices from Landsat imagery. This is mainly done via the Google Earth Engine (GEE) python api. The first step results in geotiffs of yearly vegetation indices, which are then/can be exported out to be used for further analyses. Vegetation indices of interest are as follows:

NDVI: Normalized Difference Vegetation Index

NBR: Normalized Burn Ratio

The second part (post_processing) is to prepare the vegetation indices geotiffs for subsequent statistical analyses. Post-processing involves the following steps: data cleaning, validating data, reshaping arrays, deriving intermediate values, and trend-fitting for regression analyses. The second step results in arrays of pixel-wise recovery metrics that can be used to characterize vegetation recovery quantitatively.

## Contents
* get_veg_index - folder containing python scripts to obtain yearly vegetation index values 
* post_processing - folder containing python scripts to derive recovery metrics for quantifying vegetation recovery

## Dependencies
Installation of GEE python API is required to run code from the get_veg_index folder
