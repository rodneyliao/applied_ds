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
    return sum(series)/len(series)

def standard_deviation(series):
    """
    implements the sample standard deviation of a series from scratch
    you may need a for loop and your average function
    also the function math.sqrt
    you should get the same result as calling .std() on your data
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.std.html
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html
    """

    aver_val = average(series)
    n = len(series)
    square_sum = 0
    for i in series:
        square_sum = square_sum + (i - aver_val)**2
    return math.sqrt(square_sum/(n-1))
        
    
=======
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

    n = len(series)
    median = 0
    val_ls = series.values.tolist()
    val_sort = sorted(val_ls)
    if n%2 == 0:
        median = float(val_sort[(n//2)-1]/2 + val_sort[n//2]/2)
    else:
        median = val_sort[(n-1)/2]
    return median
=======
    pass

