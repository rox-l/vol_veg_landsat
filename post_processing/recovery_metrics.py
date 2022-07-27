# ======================
# Functions to obtain recovery metrics from trend curve
# Only obtain recovery metrics from pixels where curve fitting r2 > 0.7, and pval < 0.05
# 1. Obtain years to a certain recovery percentage (e.g., 80% (Pickell et al., 2016) / 10% (Lawrence and Ripple, 2000))
# 2. Obtain slope of trend curve (DeSchutter et al., 2015)
# 3. Obtain absolute measure of post-disturbance regrowth after 5 years (Kennedy et al., 2012)
# 4. Obtain relative measure of post-disturbance regrowth after 5 years (Kennedy et al., 2012)
# ======================

import numpy as np

def numyears_from_trend(valid_veg_withyears, ind_fit_result, recovery_percent): 
    '''
    Obtains the number of years needed to reach a certain recovery percentage,
    as modeled from the trend fitted curve. 
    (e.g., to reach 80% (Pickell et al., 2016) or 10% (Lawrence and Ripple, 2000))

    Args: 
        ind_fit_result (numpy_array): n-dim array of trend fitting results
        valid_veg_withyears (numpy array): complete image stack
        recovery_percent (float): from 0 to 1 to represent percentage recovery. e.g., 0.8 for 80% recovery
    Returns: 
        final_filtered (numpy_array): number of years for each pixel
    '''
    
    # get pre-eruption veg ind values at the desired percentage
    shp = valid_veg_withyears.shape
    valid_veg_withoutyears = valid_veg_withyears[:, :, 1]
    years = valid_veg_withyears[:, :, 0]

    veg_1985 = valid_veg_withoutyears[:, 1]
    veg_1986 = valid_veg_withoutyears[:, 2]
    veg_pre_avg = np.where(np.isnan((veg_1985 + veg_1986)/2), veg_1985, (veg_1985 + veg_1986)/2)
    veg_pre_avg_recovered = recovery_percent*veg_pre_avg # y value
    
    # get slope and constant for log equation (y = alog(x) + b)
        # x = year; y = veg index value
    slope = ind_fit_result[:, 0]
    const = ind_fit_result[:, 1]
    pval_arr = ind_fit_result[:, 2]
    r2_arr = ind_fit_result[:, 3]
    
    # pre_const = veg_pre_avg_recovered - const
    pre_const = veg_pre_avg_recovered - const
    pre_const = pre_const/slope
    
    year = (np.rint(10**(pre_const)))
    # filter year for valid values. Invalid = < 0 or > 100
    year_filtered = np.where(year < 30, year, np.nan).astype(int)
    
    # add filter for good r2 and p values
    # filter slope, p, r2 by certain thresholds 
    # p < 0.05 and r2 >= 0.7
    filtered_for_p = np.where(pval_arr < 0.05, year_filtered, np.nan)
    filtered_for_r2 = np.where(r2_arr >= 0.7, filtered_for_p, np.nan)
    
    final_filtered = filtered_for_r2
    return final_filtered

# slope (beta)
def get_slope(ind_fit_result):
    """
    Gets the slope (beta) of linear-log regression curve, after filtering for p < 0.05 and r2 > 0.7
    
    Args: 
        ind_fit_result (numpy_array): n-dim array of trend fitting results
    Returns: 
        final_slope (numpy_array): slope of regression curve for each pixel
    """
    # get slope and constant for log equation (y = alog(x) + b)
        # x = year; y = veg index value
    slope = ind_fit_result[:, 0]
    const = ind_fit_result[:, 1]
    pval_arr = ind_fit_result[:, 2]
    r2_arr = ind_fit_result[:, 3]
    
    # add filter for good r2 and p values
    # filter slope, p, r2 by certain thresholds 
    # p < 0.05 and r2 >= 0.7
    filtered_for_p = np.where(pval_arr < 0.05, slope, np.nan)
    filtered_for_r2 = np.where(r2_arr >= 0.7, filtered_for_p, np.nan)
    
    final_slope = filtered_for_r2
    return final_slope

# get absolute measure of post-disturbance regrowth after 5 years
def abs_regrowth(ind_fit_result, num_years=5): 
    """
    Gets the absolute measure of post-disturbance regrowth from the linear-log regression curve (Kennedy et al., 2012)
    after filtering for p < 0.05 and r2 > 0.7, 
    where absolute measure = fitted_ind(year5) - fitted_ind(year0) # year 0 has no value? 

    Args:
        ind_fit_result (numpy_array): n-dim array of trend fitting results
        num_years (int): number of years post-disturbance regrowth. Default is 5
    Returns:
        filtered_abs_regrowth (numpy array): absolute regrowth value for each pixel
    """
    # get slope and constant for linear-log equation (y = alog(x) + b)
    # x = year; y = veg index value
    slope = ind_fit_result[:, 0]
    const = ind_fit_result[:, 1]
    pval_arr = ind_fit_result[:, 2]
    r2_arr = ind_fit_result[:, 3]
    
    ind_yearpost = const + slope*np.log10(num_years) # linear-log equation (y = alog(x) + b)
    ind_year0 = const + slope*np.log10(1)
    abs_diff = ind_yearpost - ind_year0 
    
    filtered_for_p = np.where(pval_arr < 0.05, abs_diff, np.nan)
    filtered_for_r2 = np.where(r2_arr >= 0.7, filtered_for_p, np.nan)
    
    # add filtering for r2 and p
    filtered_abs_regrowth = filtered_for_r2
    
    return filtered_abs_regrowth
    
# get relative measure of post-disturbance regrowth
def rel_regrowth(ind_fit_result, abs_regrowth, dVI): 
    """
    Gets the relative measure of post-disturbance regrowth from the linear-log regression curve (Kennedy et al., 2012)
    after filtering for p < 0.05 and r2 > 0.7, 
    where relative measure = abs_regrowth / dVI
    Args: 
        dVI (numpy array): magnitude of change caused by the eruption (e.g., dNBR; dNDVI)
        ind_fit_result (numpy array): n-dim array of trend fitting results
        abs_regrowth (numpy array): absolute regrowth result from abs_regrowth()
    Returns: 
        RI (numpy array): relative regrowth values for each pixel
    """
    # get slope and constant for linear-log equation (y = alog(x) + b)
    # x = year; y = veg index value
    slope = ind_fit_result[:, 0]
    const = ind_fit_result[:, 1]
    pval_arr = ind_fit_result[:, 2]
    r2_arr = ind_fit_result[:, 3]
    
    # filter dIND for r2 and p
    filtered_for_p = np.where(pval_arr < 0.05, dVI, np.nan)
    filtered_for_r2 = np.where(r2_arr >= 0.7, filtered_for_p, np.nan)
    filtered_dIND = filtered_for_r2
    
    RI = abs_regrowth / filtered_dIND
    
    return RI