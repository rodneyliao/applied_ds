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
    #sl = len(series)
    #ss = sum(series)
    #sa = ss / sl
    sa = sum(series) / len(series) 
    return sa

#x = average([1,2,3,4,5,6,7,8])
#print(average([1,2,3,4,5,6,7,8]))

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
    sa = average(series)
    sl = len(series) 
    ss = 0
    i=1
    for i in range(0,sl):
        x = series[i] - sa 
        y = x ** 2
        ss = ss + y
        #print (x, y, ss, i)
    #print (ss)
    sd = math.sqrt(ss/(sl-1))
    return sd
    
#print(standard_deviation([1,2,3,4]))

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
    sl = len(series)
    if sl < 1:
            return None
    if sl % 2 == 1:
            return sorted(series)[sl//2]
    else:
            return sum(sorted(series)[sl//2-1:sl//2+1])/2.0
    
    