# ======================
# Functions to harmonize LS5/7/8 according to https://developers.google.com/earth-engine/tutorials/community/landsat-etm-to-oli-harmonization?hl=en
# get coefficients from Roy et al., 2016
# these coefficients tranform 5/7SR to 8SR
# ======================

import ee

def harmonizeEtm(img): 
    """
    Function to harmonize Landsat 5 and 7 to Landsat 8. 
    Includes wrapper function to consolidate ETM harmonization and mask clouds (fmask)
    
    Args: 
        img (ee.Image): images from Landsat 5 or 7 
    
    Returns: 
        harmonized Landsat 5 or 7 image with renamed bands and cloud masking applied
    """
    orig = img
    img = renameEtm(img)
    img = fmask(img)
    img = etmToOli(img)
    return ee.Image(img.copyProperties(orig, orig.propertyNames()))

def prepOli(img): 
    """
    Function to prepare Landsat 8 for harmonization with Landsat 7 and 5
    Includes wrapper function to rename bands and mask clouds (fmask)
    
    Args: 
        img (ee.Image): Landsat 8 images
    
    Returns: 
        Landsat 8 image with renamed bands and cloud masking applied
    """
    orig = img
    img = renameOli(img)
    img = fmask(img)
    return ee.Image(img.copyProperties(orig, orig.propertyNames()))


# Helper functions for above harmonizeEtm and prepOli functions

coefficients = {
  'itcps': ee.Image.constant([0.0003, 0.0088, 0.0061, 0.0412, 0.0254, 0.0172])
             .multiply(10000),
  'slopes': ee.Image.constant([0.8474, 0.8483, 0.9047, 0.8462, 0.8937, 0.9071])
}

def renameOli(img): 
    """Function to get and rename bands of interest from Landsat 8 to standardize between OLI and ETM/TM"""
    return img.select(
    ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'pixel_qa'],
    ['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2', 'pixel_qa'])

def renameEtm(img): 
    """Function to get and rename bands of interest from Landsat 5 or 7 to standardize between OLI and ETM/TM"""
    return img.select(
    ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'pixel_qa'],
    ['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2', 'pixel_qa'])

def etmToOli(img): 
    """Function to apply transformation from TM/ETM to OLI"""
    return img.select(['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2']).multiply(coefficients['slopes']) \
    .add(coefficients['itcps']) \
    .round() \
    .toShort() \
    .addBands(img.select('pixel_qa'))

def fmask(img): 
    """cloud masking function using CFmask (Zhu et al., 2015)"""
    cloudShadowBitMask = 1 << 3
    cloudsBitMask = 1 << 5
    qa = img.select('pixel_qa')
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    return img.updateMask(mask)