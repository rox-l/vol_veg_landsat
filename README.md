# Landsat Time-series Vegetation Recovery Analyses

## Introduction
This repository provides a pipeline to prepare a dense stack of Landsat imagery for time-series and regression analyses in order to quantify vegetation recovery at Unzen Volcano, Japan. Performing annual time-series analyses across different Landsat satellites requires some preprocessing steps to ensure appropriate continuity across different satellite sensors, derive vegetation indices, and obtain yearly values. 

## Features
This pipeline generates vegetation recovery metrics (based on Lawrence and Ripple, 2000; Pickell et al., 2016; White et al., 2017) to quantify vegetation recovery over a relatively long timeframe (in remote sensing terms). 

The first step (get_veg_index folder) is to download, pre-process, and derive vegetation indices from Landsat imagery. This is mainly done via the Google Earth Engine (GEE) python api. The first step results in geotiffs of the vegetation indices, which are then/can be exported out to be used for further analyses. Vegetation indices of interest are as follows:

NDVI: Normalized Difference Vegetation Index

NBR: Normalized Burn Ratio

SAVI: Soil Adjusted Vegetation Index

The second step is post-processing (post_processing folder) to prepare the vegetation indices geotiffs for subsequent statistical analyses. Post-processing involves the following steps: data cleaning, validating data, reshaping arrays, and deriving intermediate values.

## Contents
* get_veg_index - folder containing scripts to obtain yearly vegetation index values 
* post_processing - folder containing scripts to derive recovery metrics for quantifying vegetation recovery

## Dependencies
Installation of GEE python API is required to run code from the get_veg_index folder
