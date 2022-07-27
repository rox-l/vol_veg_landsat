# ======================
# Wraps up all the functions from ingest and clean helper module to ingest and clean
# Landsat geotiffs
# ======================

# import modules 
import ingest_and_clean as ic
import matplotlib.pyplot as plt

# ======================
# Wrapper function for data ingesting and cleaning 
# ======================
def wrapper_clean_ingest(file_list, veg_index): 
    '''
    Args: 
        file_list (list): list of file paths to geotiffs of vegetation indices
        veg_index (string): either 'NDVI', 'SAVI', 'NBR'

    Returns: 
        valid_veg_withyears (numpy array): 3D numpy array where [:, :, 0] is the flattened yearly vegetation index values, and 
        [:, :, 1] is the years repeated along axis1
    '''
    # Check for valid vegetation index
    
    good_veg_index = ['NBR', 'NDVI', 'SAVI']
    if veg_index not in good_veg_index: 
        raise ValueError("Inappropriate vegetation index chosen!")

    # create numpy image stack
    image_stack, year_list, stack_depth, meta, bounds = ic.create_image_stack(file_list, veg_index)

    # Add missing years of np.nan arrays to original image stack
    full_image_stack = ic.add_missing_years(image_stack, year_list)

    # Create valid pixel mask to label if pixel is valid or not
    # 
    val_pix_reshaped = ic.clean_data(full_image_stack)

    # Reshape data set to apply regression
    valid_veg_index_withyears = ic.reshape_image_stack(full_image_stack, year_list)

    # To get vegetation index without the years along axis 2
    # valid_veg_index_withoutyears = valid_veg_index_withyears[:, :, 1]
    
    # get disturbed pixel array
    disturbed_veg_arr, only_years, only_veg_ind = ic.get_disturbed_pixel_array(valid_veg_index_withyears, year_list)

    # get valid pixels using mask
    valid_veg_arr = ic.get_valid_pixel_filter(val_pix_reshaped, disturbed_veg_arr)

    # get complete cleaned dataset
    valid_veg_withyears = ic.get_valid_image_stack(valid_veg_arr, only_years, only_veg_ind)

    return valid_veg_withyears