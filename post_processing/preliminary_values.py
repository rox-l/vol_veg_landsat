# ======================
# Function to generate preliminary values 
# ======================

import numpy as np

def get_dVI(valid_vegstack_withyears): 
    '''
    This function creates the differenced vegetation index value (dVI), where dVI 
    is the absolute vegetation index difference pre- and post- eruption

    Args: 
        valid_vegstack_withyears (numpy array): complete image stack

    Returns: 
        dVI (numpy array): differenced vegetation index value for pre- and post-eruption years 
    '''
    # remove the years
    valid_vegstack = valid_vegstack_withyears[:, :, 1]

    # Get the average of pre-eruption VI values. 1985 and 1986 were chosen 
    # due to best data quality
    vi85 = valid_vegstack[:, 1] # 1985
    vi86 = valid_vegstack[:, 2] # 1986
    vi_pre = np.where(np.isnan((vi85 + vi86) / 2), vi85, (vi85 + vi86) / 2)

    # get post-eruption VI values: 1995
    vi_post = valid_vegstack[:, 11]

    dVI = vi_pre - vi_post
    return dVI