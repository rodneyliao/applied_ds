import pandas as pd
import numpy as np
import math
import pdb


def average(series):
    """
    implements the average of a pandas series from scratch
    suggested functions:
    len(list)
    sum(list)
    you should get the same result as calling .mean() on your series
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.mean.html
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    """
    l = len(series)
    s = sum(series)
        
    average = s/l
    
    return(average)
    
    pass

def standard_deviation(series):
    """
    implements the sample standard deviation of a series from scratch
    you may need a for loop and your average function
    also the function math.sqrt
    you should get the same result as calling .std() on your data
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.std.html
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html
    
    NOTES:
    - Likely requires a for-loop
    - Look up how to append
    - Standard Deviation = sqrt((x - x.mean()2/(n-1))
    
    PLAN:
    - For loop, calculate data point, append to value
    
    AFTER NOTES:
    - Don't forget ":" after range!!!!
    - To call value in array use [] not () as in series[i]
    
    """
    stdev_num = 1
    
    '''Must predefine value used in for-loop.'''
    
    a = average(series)
    
    '''Added average variable to type less.'''
    
    for i in range (len(series)):
        stdev_num += (series[i] - a)**2
        
    '''This for-loop finds the sum of the square of the subtractive
    sum of each data point minus the average'''

    standard_deviation = math.sqrt(stdev_num / (len(series)-1))
    
    '''For some reason it did not work to use math. in
    the for loop so had to put it outside.'''
        
    return(standard_deviation)
    
    pass

def median(series):
    """
    finds the median of the series from scratch
    you may need to sort your values and use
    modular division
    this number should be the same as calling .median() on your data
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.median.html
    https://pandas.pydata.org/pandas-docs/version/0.23.0/generated/pandas.Series.median.html
    """
    
    data_sort = np.sort(series)
    
    while len(data_sort) > 2:
        data_sort = data_sort[1:len(data_sort)-1]
    '''This while loop removes the fist and last
    line of the data array until only 1 or 2 remain'''
    
    if len(data_sort) == 1:
        mdn = data_sort(0)
        return (mdn)
    else:
        mdn = sum(data_sort)/2
        return (mdn)
    '''This if/else logical statement checks if only
    one datapoint remains (odd number of data) or if
    two do. Then returns if one, returns averages if 2.'''
    
    pass
