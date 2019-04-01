import pandas as pd
import numpy as np
import math
import pdb
import test_eda

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
    avg = sum(series)/len(series)
    return avg

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
    mean = average(series)
    sum_diffsq = 0
    for i in range(len(series)):
        diffsq = (series[i] - mean)**2
        sum_diffsq = sum_diffsq + diffsq
    
    s = (sum_diffsq/(len(series)-1))**(1/2)
    
    return s
        

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
    #sorted_series = series.sort_values(ascending=True)
    
    #length = len(sorted_series)
    
    #if remainder of length/2 = 0  ====> even number of values
   # if (length % 2 == 0):
   #     first_index = length / 2
   #     second_index = length / 2 - 1
        
   #     median = (series[first_index] + series[second_index]) / 2
        
   # else: #not even ===> must be odd
   #     index = (length + 1) / 2
   #     median = series[index]
 #return median
    n = len(series)
    if n < 1:
        return None
    if n % 2 == 1:
        return sorted(series)[n//2]
    else:
        return sum(sorted(series)[n//2-1:n//2+1])/2
    
    #return median
