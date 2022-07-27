# ======================
# Filter landsat collections, apply cloudmasking, and harmonize
# Then merge, apply terrain correction, and add NDVI/NBR/SAVI bands
# ====================== 

import ee

def filter_collection(imgCollection, filterpoint, harmonizefunc, landsat_sat, cloudcover=80, img_qual=7, rmse=10):
    '''
    Filters imageCollection according the given parameters
    Args: 
        imgCollection (ee.ImageCollection):
        filterpoint (ee.Geometry.Point): longitude, latitude of point at area of interest
        harmonizefunc (function): harmonization function (harmonizeEtm (LS5/7) or prepOli (LS8))
        specify_years (bool): If years are to be specified
        start_yr (int): year to start filtering from (default = 0)
        end_yr (int): year to end filtering (default = 0)
        cloudcover (int): cloud cover over land (0 - 100)
        img_qual (int): image quality (0 - 10)
        rmse (int): geometric root mean square error

    Returns: 
        filtered_collection(ee.ImageCollection): Filtered image collection
    '''
    if landsat_sat == 'LS5':
        filtered_collection = imgCollection.filterMetadata('CLOUD_COVER_LAND', 'less_than', cloudcover) \
            .filterBounds(filterpoint) \
            .filterMetadata('GEOMETRIC_RMSE_MODEL', 'less_than', rmse) \
            .filterMetadata('IMAGE_QUALITY', 'greater_than', img_qual) \
            .map(harmonizefunc)

    elif landsat_sat == 'LS7': 
        filtered_collection = imgCollection.filterMetadata('CLOUD_COVER_LAND', 'less_than', cloudcover) \
            .filterBounds(filterpoint) \
            .filterMetadata('GEOMETRIC_RMSE_MODEL', 'less_than', rmse) \
            .filterMetadata('IMAGE_QUALITY', 'greater_than', img_qual) \
            .filter(ee.Filter.calendarRange(1999, 2002, 'year')) \
            .map(harmonizefunc)
    
    elif landsat_sat == 'LS8': 
        filtered_collection = imgCollection.filterMetadata('CLOUD_COVER_LAND', 'less_than', cloudcover) \
            .filterBounds(filterpoint) \
            .filterMetadata('GEOMETRIC_RMSE_MODEL', 'less_than', rmse) \
            .filterMetadata('IMAGE_QUALITY_OLI', 'greater_than', img_qual) \
            .map(harmonizefunc)
    
    print('Number of images in collection: ', filtered_collection.size().getInfo())
    
    return filtered_collection

# LS5_filtered = LS5.filterMetadata('CLOUD_COVER_LAND', 'less_than', 80) \
#     .filterMetadata('IMAGE_QUALITY', 'greater_than', 7) \
#     .filterMetadata('GEOMETRIC_RMSE_MODEL', 'less_than', 10) \
#     .filterBounds(filterpoint) \
#     .map(harmonizeEtm)

# LS7_filtered = LS7.filterMetadata('CLOUD_COVER_LAND', 'less_than', 80) \
#     .filterMetadata('IMAGE_QUALITY', 'greater_than', 7) \
#     .filterMetadata('GEOMETRIC_RMSE_MODEL', 'less_than', 10) \
#     .filter(ee.Filter.calendarRange(1999, 2002, 'year')) \
#     .filterBounds(filterpoint) \
#     .map(harmonizeEtm)

# LS8_filtered = LS8.filterMetadata('CLOUD_COVER_LAND', 'less_than', 80) \
#     .filterMetadata('IMAGE_QUALITY_OLI', 'greater_than', 7) \
#     .filterMetadata('GEOMETRIC_RMSE_MODEL', 'less_than', 10) \
#     .filterBounds(filterpoint) \
#     .map(prepOli)