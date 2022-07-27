# ======================
# Functions for ingesting and cleaning Landsat geotiff
# ======================

# import libraries 
import numpy as np
import rasterio 

# ======================
# Function to read in vegetation index images and create np image stack
# ======================
def create_image_stack(files, extension): 
    """
    This function creates an image stack from the geotiff files given, 
    and adds a year element 
    
    Args: 
        files (list): list of file paths
        extension (string): 'NDVI', 'NBR', 'SAVI'
    
    Returns: 
        image_stack (numpy array): numpy ndarray 
        year_list (list): list of years in image stack
        stack_depth (int): depth of image stack
        meta (dict): meta data for raster file
        bounds: bounds for raster file
    """
    # get year list
    if extension == 'NBR':
        year_list = [int(i[-16:-12]) for i in files]
    elif extension == 'NDVI' or extension == 'SAVI':
        year_list = [int(i[-17:-13]) for i in files]
    stack_depth = len(year_list)

    # get image shape
    with rasterio.open(files[0]) as f:
        meta = f.meta
        bounds = f.bounds
        image_get_shape = f.read(1)
    height, width = image_get_shape.shape
    
    # create empty np array for image stack
    image_stack = np.empty([height, width, stack_depth])
    print('empty image stack shape: ', image_stack.shape)
     
    # create image stack
    for i, file in enumerate(files): 
        with rasterio.open(file) as f: 
            image = f.read(1)
            image_stack[:, :, i] = image
    print('Finished reading and creating raw image stack...')
    return image_stack, year_list, stack_depth, meta, bounds

# ======================
# Function to add missing years of np.nan arrays to original image stack
# ======================

def add_missing_years(image_stack, year_list):
    """
    This function adds missing years as np.nan arrays to the original images stack 
    to ensure that image stack depth covers the time period

    Args: 
        image_stack (numpy array): ndarray stack of yearly vegetation indices
        year_list (list): list of years in image stack (potentially missing some years)

    Returns: 
        actual_arr (numpy array): ndarray stack of yearly vegetation indices without any missing years; 
                                missing years have been filled as np.nan arrays

    """
    # full list of years with no missing values
    yearly_years = [year for year in range(year_list[0], year_list[-1] + 1)]

    actual_depth = len(yearly_years)
    height, width, depth = image_stack.shape
    actual_arr = np.full([height, width, actual_depth], np.nan)
    img_stack_index = 0
    for i in range(len(yearly_years)): 
        if yearly_years[i] in year_list: 
            actual_arr[:, :, i] = image_stack[:, :, img_stack_index]
            img_stack_index += 1
    print("Added missing years to image stack...")
    return actual_arr

# ======================
# DATA CLEANING: Create valid pixel mask to label if pixel is valid or not
# Check for poor quality data; missing data is recorded in numpy array as nan
# ======================
# count number of nans for each pixel over the years

def clean_data(full_pix_arr, valid_num=20): 
    """
    This function creates a mask to label is a pixel is considered "valid" or not.
    Pixels are considered valid if the number of nans (valid_num) is <20, i.e., if there at least
    19 data points (i.e., half of the full 38)

    Args: 
        full_pix_arr (numpy array): full np array of yearly VIs without missing years
        valid_num (int): at least half of the total time period (total number of years);
                        default for Unzen volcano is 20 (total time period = 38 years)

    Returns: 
        val_pix_reshaped (numpy array): mask of valid pixels 
    """
    bool_mask = np.isnan(full_pix_arr)
    nan_per_pixel = np.count_nonzero((bool_mask), axis=2)
    
    val_pix = nan_per_pixel < valid_num
    # if pixel is valid, bool = True
    # plt.imshow(val_pix)
    
    # reshape pixel array to concatenate with reshaped base array
    shp = val_pix.shape
    val_pix_reshaped = val_pix.reshape(shp[0]*shp[1], 1)
    print('reshaped shape of valid pixel mask: ', val_pix_reshaped.shape)
    print('Created mask of valid pixels...')
    return val_pix_reshaped

# ======================
# Function to reshape image stack to apply regression
# ======================
def reshape_image_stack(image_stack, year_list): 
    """
    Function to reshape image stack into 2D array, then concatenate with year array
    along axis = 2 to create a final 3D np array 
    
    Args:
        image_stack (ndarray): full VI image stack without missing years
        year_list (list): list of years from original data set
    
    Returns:
        base_array: 3D ndarray 
    """
    # full list of years with no missing values
    yearly_years = [year for year in range(year_list[0], year_list[-1] + 1)]

    # create empty base array
    print('START: reshaping data...')
    row, col, stack_depth = image_stack.shape
    print('row, col: ',row, col)
    base_array = np.empty([row*col, stack_depth])
    print('base array shape: ', base_array.shape)
    
    for i in range(stack_depth): 
        img = image_stack[:, :, i]
        img_reshape = img.reshape((row*col))
        base_array[:, i] = img_reshape
        
    # add years array
    years_array = np.array(yearly_years)
    years_array_reshaped = years_array.reshape((1, years_array.shape[0]))
    
    # reshape years array to combine with base array along axis=2
    shp = base_array.shape
    base_years_array = np.repeat(years_array_reshaped, shp[0], axis = 0).reshape((shp[0], shp[1], 1))
    base_array = base_array.reshape((shp[0], shp[1], 1))

    # concatenate years to data
    base_array = np.concatenate((base_years_array, base_array), axis=2)
    
    # print('max and min veg: ', max_veg, min_veg)
    print('FINISHED: shape of reshaped array that is returned: ', base_array.shape)
    return base_array

# ======================
# function1: classify whether pixel is disturbed or not. Log reg fitted only to disturbed pixels
# function2: combine disturbed and nan filters
# function3: filter original image stack by combined filters to produce valid and disturbed image stack

# Filter pixels by validity array and disturbed pixel array 
# original array to filter: only_NBR from (reshaped_NBR)
# validity array: val_pix_arr_reshaped
# disturbed pixel array: disturbed_pixels (array of bools)
# ======================

def get_disturbed_pixel_array(reshaped_image_stack, year_list):
    """
    This functions classifies pixels as disturbed (affected by eruption) or not. Pixels are considered "disturbed" 
    if VImax_pre - VIerup > 0.20 (adapted from DeSchutter et al., 2015)
    
    Args: 
        reshaped_image_stack (numpy array): reshaped vegetation index image stack
        year_list (list): incomplete list of years
    
    Returns: 
        disturbed_pix_reshaped (numpy array): retrieved disturbed pixels array
        only_years (numpy array): only the years of the original array
        only_veg_ind (numpy array): only the vegetation indices of the original array
    """

    # full list of years with no missing values
    yearly_years = [year for year in range(year_list[0], year_list[-1] + 1)]

    only_years = reshaped_image_stack[:, :, 0]
    only_veg_ind = reshaped_image_stack[:, :, 1]
    
    year_ind_dict = {} # dictionary to get year index
    for ind, year in enumerate(yearly_years):
          if year not in year_ind_dict: 
                year_ind_dict[year] = ind
    veg1985 = only_veg_ind[:, year_ind_dict[1985]]
    veg1986 = only_veg_ind[:, year_ind_dict[1986]]
    veg_erup = only_veg_ind[:, year_ind_dict[1995]] # veg index value for year 1995 (immediately post eruption)
    veg_max_pre = np.where(np.isnan((veg1985 + veg1986)/2), veg1985, (veg1985 + veg1986)/2) # average of veg ind values for two pre-eruption years; 1985, 1986

    # check if nbr_max_pre - nbr_erup > 0.20 (or determine own value) # change this to percentage 
    pre_020 = veg_max_pre * 0.2
    pix_diff = veg_max_pre - veg_erup
    disturbed_pix = pix_diff > pre_020
    
    # original disturbed calculatation
    # pix_diff = ((veg_max_pre - veg_erup)/veg_max_pre)
    # isturbed_pix = pix_diff > 0.20 # used 0.20 after checking disturbed/undisturbed pixels
    
    # reshape to concatenate with base array
    disturbed_pix_reshaped = disturbed_pix.reshape(disturbed_pix.shape[0], 1)
    print('disturbed_pix_reshaped shape: ', disturbed_pix_reshaped.shape)
    return disturbed_pix_reshaped, only_years, only_veg_ind

def get_valid_pixel_filter(val_pix_reshaped, disturbed_pix_reshaped): 
    '''
    Applies valid pixel mask to disturbed pixel array mask
    '''
    # pixel is considered valid if it is disturbed + has > x nan values
    concat_val_disturbed = np.concatenate([val_pix_reshaped, disturbed_pix_reshaped], axis=1)
    pix_to_filter = concat_val_disturbed.all(axis=1)
    pix_to_filter_reshaped = pix_to_filter.reshape(pix_to_filter.shape[0], 1)
    print('valid pixel array shape: ', pix_to_filter_reshaped.shape)
    return pix_to_filter_reshaped

def get_valid_image_stack(pix_to_filter_reshaped, only_years, only_veg_index): 
    '''
    Applies combined mask to image stack

    Returns: 
        Complete clean and valid image stack
    '''
    pixels_to_filter_mask = np.repeat(pix_to_filter_reshaped, only_veg_index.shape[1], axis=1)
    valid_veg = np.where(pixels_to_filter_mask, only_veg_index, np.nan)

    # concatenate valid_veg with only_years
    shp = valid_veg.shape
    valid_veg = valid_veg.reshape(shp[0], shp[1], 1)
    only_years = only_years.reshape(shp[0], shp[1], 1)

    valid_veg_withyears = np.concatenate((only_years, valid_veg), axis=2)
    print('valid veg index with years shape: ', valid_veg_withyears.shape)
    return valid_veg_withyears
