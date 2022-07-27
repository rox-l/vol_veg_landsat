# ======================
# Export single image or image collection as geotiffs to external folder (e.g., geotiff_output_folder)
# Export imageCollection as geotiffs to google drive; geotiff_output_folder
# Export individual image as geotiff to google driv
# adapted from: https://colab.research.google.com/github/csaybar/EEwPython/blob/dev/index.ipynb
# ======================
import time 
import ee

# test image
# img = ee.Image((vegIndices_NDVI.toList(vegIndices_NDVI.size())).get(0))

def exportSingleImage(img, description, folder, region): 
    '''
    Exports single ee.Image as a raster to external folder

    Args: 
        img (ee.Image): image to save as a raster (geotiff)
        description (string): extension to label img
        folder (string): path to GOOGLE DRIVE folder
        region (ee.Geometry.Polygon): area of interest

    Returns: 
        Doesn't return
    '''
    # Export the image. Specify scale and region.
    task = ee.batch.Export.image.toDrive(**{
        'image': img,
        'description': description,
        'folder': folder,
        'scale': 30,
        'region': region.getInfo()['coordinates']
    })
    task.start()

    # Track import status
    while task.active():
        print('Polling for task (id: {}).'.format(task.id))
        time.sleep(5)
    print('Finished export')

def exportImageCol(imgCol, description, folder, region): 
    """ 
    Function to export imageCollection as geotiffs to google drive
    
    Args: 
        imgCol (ee.ImageCollection): imageCollection to save as geotiff to gdrive
        description (string): string to append to filename. Options: (NDVI, NBR, SAVI)
        folder (string): path to GOOGLE DRIVE folder
        region (ee.Geometry.Polygon): area of interest
    
    Returns: 
        Doesn't return 
     """
    imgCol_size = imgCol.size().getInfo()
    for num in range(imgCol_size): # replace integer in range() with imgCol_size when not testing
        img = ee.Image((imgCol.toList(imgCol.size())).get(num))
        task = ee.batch.Export.image.toDrive(**{
        'image': img,
        'description': img.getInfo()['properties']['system:index'] + '_' + description,
        'folder': folder, 
        'scale': 30, 
        'region': region.getInfo()['coordinates']
        })
        task.start()
        
        # Track import status
        while task.active():
            print('Polling for task (id: {}).'.format(task.id))
            time.sleep(15)
        print('Finished exporting ' + str(num+1) + ' image')
    print('Finished exporting entire collection')

# exportImageCol(vegIndices_SAVI, 'SAVI')