# ======================
# Create annual median composites
# ======================

import ee

def addDate(image): 
    '''
    Function to add date to imagery
    '''
    date = ee.Date(image.get('system:time_start'))
    dateString = date.format('YYYY-MM-dd')
    return image.set('date', dateString)

def median_composite(imageCollection):
    '''
    Creates yearly median composites from image collection. 
    Args: 
        imageCollection (ee.ImageCollection): image collection to create yearly median composites from

    Returns: 
        medianComp (ee.ImageCollection): image collection of yearly median composites

    '''
    # group images by year by first adding a new 'year' property
    imageCollection_withyear = imageCollection.map(lambda img : img.set('year', img.date().get('year')))
    distinct_imageCollection_withyear = imageCollection_withyear.distinct('year')
    filter = ee.Filter.equals(leftField='year', rightField='year')
    join = ee.Join.saveAll('year_matches')
    join_imgCol = ee.ImageCollection(join.apply(distinct_imageCollection_withyear, imageCollection_withyear, filter))
    
    def medianReduction(img): 
        '''
        Function to apply median reduction among matching year collections for an ee.imageCollection
        '''
        yearLS = ee.ImageCollection.fromImages(img.get('year_matches'))
        return yearLS.reduce(ee.Reducer.median()).set('system:time_start', 
                                                img.date().update(month=6, day=1)).set('year', 
                                                                                      img.date().get('year'))

    medianComp = join_imgCol.map(medianReduction)
    # sort medianComp to get in date order
    medianComp = medianComp.sort('system:time_start')
    return medianComp

# # group images by year by first adding a new 'year' property
# growing_LS = growing_LS.map(lambda img : img.set('year', img.date().get('year')))
# distinctYearLS = growing_LS.distinct('year')

# filter = ee.Filter.equals(leftField='year', rightField='year')
# join = ee.Join.saveAll('year_matches')
# joinLS = ee.ImageCollection(join.apply(distinctYearLS, growing_LS, filter))

# def medianReduction(img): 
#     """Function to apply median reduction among matching year collections for an ee.imageCollectio"""
#     yearLS = ee.ImageCollection.fromImages(img.get('year_matches'))
#     return yearLS.reduce(ee.Reducer.median()).set('system:time_start', 
#                                                 img.date().update(month=6, day=1)).set('year', 
#                                                                                       img.date().get('year'))

# medianComp = joinLS.map(medianReduction)
# # sort medianComp to get in date order
# medianComp = medianComp.sort('system:time_start')
# # print(medianComp.size().getInfo())