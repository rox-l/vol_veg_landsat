from os import times_result
import composite as cp
import filter
import get_VIs as vi
import harmonize
import export_as_geotiff as exp
import ee

def wrapper_prep(params): 
    '''
    This function prepares each Landsat collection for merging by filtering for appropriate parameters 
    and harmonizing collection

    Args: 
        imgCollection (ee.ImageCollection): raw Landsat image collection 
        params (dictionary): parameters to extract image collection of vegetation indices from Landsat
                            image collection

    Returns: 
        filtered_collection (ee.ImageCollection): filtered and harmonized image collection 

    '''
    # extract params
    IMAGE_COLLECTION = params['IMAGE_COLLECTION']
    FILTER_POINT = params['FILTER_POINT']
    LANDSAT_SAT = params['LANDSAT_SAT']
    CLOUD_COVER_OVER_LAND = params['CLOUD_COVER_OVER_LAND']
    IMAGE_QUALITY = params['IMAGE_QUALITY']
    GEOMETRIC_RMSE = params['GEOMETRIC_RMSE']

    good_landsat_names = ['LS5', 'LS7', 'LS8']
    if LANDSAT_SAT not in good_landsat_names: 
        raise ValueError("Inappropriate landsat name!")

    if LANDSAT_SAT == 'LS5' or LANDSAT_SAT == 'LS7': 
        HARMONIZE_FUNC = harmonize.harmonizeEtm
    elif LANDSAT_SAT == 'LS8': 
        HARMONIZE_FUNC = harmonize.prepOli
    
    # filter and harmonize
    filtered_harmonized_collection = filter.filter_collection(imgCollection=IMAGE_COLLECTION, 
                                                filterpoint=FILTER_POINT, 
                                                landsat_sat= LANDSAT_SAT,
                                                harmonizefunc=HARMONIZE_FUNC, # harmonize
                                                cloudcover=CLOUD_COVER_OVER_LAND, 
                                                img_qual=IMAGE_QUALITY, 
                                                rmse=GEOMETRIC_RMSE)

    return filtered_harmonized_collection

def wrapper_VI(prepped_LS5, prepped_LS7, prepped_LS8): 
    '''
    Merges, adds vegetation indices, selects growing season, and creates annual median composites
    
    Args: 
        prepped_LS5 (ee.ImageCollection): filtered and harmonization Landsat 5 image collection
        prepped_LS7 (ee.ImageCollection): filtered and harmonization Landsat 7 image collection
        prepped_LS8 (ee.ImageCollection): filtered and harmonization Landsat 8 image collection

    Returns: 
        annual_median_composites (ee.ImageCollection): annual median composites
    '''
    # merges all landsat collection
    all_LS = prepped_LS5.merge(prepped_LS7).merge(prepped_LS8)

    # adds vegetation indices as bands to image collection
    all_LS = all_LS.map(vi.getNDVI).map(vi.getNBR).map(vi.getSAVI)

    # select only growing season
    growing_LS = all_LS.filter(ee.Filter.calendarRange(6, 9, 'month'))

    # create annual median composites
    annual_median_composites = cp.median_composite(growing_LS)

    return annual_median_composites

    # print(growing_LS.size().getInfo())

def test(a, b): 
    print("TESTING: ", a*b)
