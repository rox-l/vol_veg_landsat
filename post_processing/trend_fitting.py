
# Linear log fitting
# refactoring code for: do linear fitting (log) using statsmodel.api 
# # https://www.statology.org/sklearn-linear-regression-summary/

import statsmodels.api as sm
import numpy as np

def trend_fit(valid_vegstack_withyears): 
    """
    This function performs pixel-wise linear-log regression to obtain components of the regression curve
    Args: 
        valid_vegstack (numpy array): complete image stack
    Returns: 
        trend_attr (n-dim numpy array): n-dim array of regression curve components (slope, const, pval, r2)
    """
    # Get just vegetation indices
    valid_vegstack = valid_vegstack_withyears[:, :, 1]

    post_erup_stack = valid_vegstack[:, 11:] # used to be from 9; 11 is more accurate
    print(post_erup_stack.shape[0])
    
    # initialize np array to store slope, p, and r2 values (in that order)
    
    trend_attr = np.full([post_erup_stack.shape[0], 4], np.nan)
                             
    # loop through each pixel (height) to fit trend through years
    for i in range(post_erup_stack.shape[0]): 
        # response data
        y = post_erup_stack[i, :].reshape(-1, 1)
        y_len = y.shape[0]
        
        # predictor dataset
        x = np.array([i for i in range(y_len)]).reshape(-1, 1)
        
        idx = np.isfinite(x) & np.isfinite(y) # drops nan 
        # idx = np.isfinite(y)
        x = np.where(x[idx]>0, np.log10(x[idx]), 0).reshape(-1, 1) # select non-nan values; log
        # x = np.where(x>0, np.log10(x), 0).reshape(-1, 1) # select non-nan values; log
        # x = np.log10(x[idx].reshape(-1, 1)) # select non-nan values; log
        # x = x[idx].reshape(-1, 1)
        y = y[idx].reshape(-1, 1) # select non-nan values
        
        # model fitting
        try: 
            x2 = sm.add_constant(x)
            models = sm.OLS(y, x2)
            result = models.fit()
        
        # extracting values. # slope = params[1] and const = params[0]
            params = result.params
            slope = params[1] # slope for x variable
            const = params[0]
            pval = result.pvalues[1] # p value for x variable
            r2 = result.rsquared
            
            trend_attr[i, 0] = slope
            trend_attr[i, 1] = const
            trend_attr[i, 2] = pval
            trend_attr[i, 3] = r2
        except ValueError: 
            trend_attr[i, 0] = np.nan
            trend_attr[i, 1] = np.nan
            trend_attr[i, 2] = np.nan
            trend_attr[i, 3] = np.nan
        
     # return array of slope and pval?? 
    return trend_attr

