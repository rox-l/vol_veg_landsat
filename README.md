# Landsat time-series image preparation to retrieve vegetation indices

## Introduction
Pipeline to process Landsat imagery to monitor vegetation recovery at volcanic areas
This repository contains relevant scripts to process Landsat imagery in order to quantify vegetation recovery at selected volcanic areas.

## Features
The first step is to download, pre-process, and derive vegetation indices from raw Landsat imagery. This is mainly done via the Google Earth Engine (GEE) python api. The first step results in geotiffs of the vegetation indices, which are then/can be exported out to be used for further analyses. Vegetation indices of interest are as follows:

NDVI: Normalized Difference Vegetation Index

NBR: Normalized Burn Ratio

SAVI: Soil Adjusted Vegetation Index

The second step is post-processing to prepare the vegetation indices geotiffs for subsequent statistical analyses. Post-processing involves the following steps: data cleaning, validating data, reshaping arrays, and deriving intermediate values.
