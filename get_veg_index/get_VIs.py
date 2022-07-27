import ee

# ======================
# Functions to calculate NDVI, NBR, SAVI bands and add band to original image 
# for harmonized and merged landsat collection (all_LS) where band names have been changed
# NDVI = (NIR - RED) / (NIR + RED)
# NBR = (NIR - SWIR)/(NIR + SWIR) (Lopez, 1991; Key and Benson, 1995)
# SAVI = ((NIR - RED)/ (NIR + RED + 0.5)) * 1.5

# new indices
# B5 (landsat 5/7); B6 (Landsat 8) (Schroeder et al., 2011) = SWIR2
# Bare Soil Index = ((SWIR1 + RED) - (NIR + BLUE))/((SWIR1 + RED) + (NIR+BLUE)) (Roy et al., 2006?)
# ======================

def getNDVI(image): 
    NDVI = image.normalizedDifference(['NIR', 'Red']).rename('NDVI')
    return image.addBands(NDVI)

def getNBR(image): 
    NBR = image.normalizedDifference(['NIR', 'SWIR2']).rename('NBR')
    return image.addBands(NBR)

def getSAVI(image): 
    SAVI = image.expression('((NIR - RED)/(NIR + RED + 0.5))* 1.5', 
    {
    'NIR': image.select('NIR').multiply(0.0001),
    'RED': image.select('Red').multiply(0.0001)
    }).rename('SAVI')
    return image.addBands(SAVI)

def getBSI(image): 
    BSI = image.expression('((SWIR1 + RED) - (NIR + BLUE))/((SWIR1 + RED) + (NIR+BLUE))',
            {
            'BLUE': image.select('Blue').multiply(0.0001),
            'NIR': image.select('NIR').multiply(0.0001),
            'RED': image.select('Red').multiply(0.0001),
            'SWIR1': image.select('SWIR1').multiply(0.0001)
            }).rename('BSI')
    return image.addBands(BSI)

# def getB5(image): 
#     B5 = 
