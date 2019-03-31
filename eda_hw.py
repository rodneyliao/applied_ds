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
    return(sum(series)/len(series))
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
    """
    diff  = []
    for i in range(len(series)):
        temp = (series.iloc[i] - average(series))**2
        diff.append(temp)
    stDev = math.sqrt(sum(diff)/(len(series) - 1))
    return(stDev)
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
    new = np.sort(series)
    length = len(new)
    n1 = int(length / 2)
    n2 = int(length / 2) + 1
    if length % 2 == 0:
        mid = (new[n1] + new[n2])/2
    else: 
        location = (length-1) // 2
        mid = new[location]
    return(mid)
    pass
