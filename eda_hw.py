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
    sa = average(series)
    sl=len(series)
    ss=0
    i=1
    for i in range(0,sl):
        a = series[i]-sa
        b = a ** 2
        ss += b
        print(a,b,i,ss)
    m = math.sqrt(ss/(sl-1))
    return m


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
    n = sorted(series)
    if len(n) < 1:
        return None
    elif len(n)%2 == 1:
        return n[len(n)//2]
    else:
        return (n[len(n)//2-1] + n[len(n)//2])/2

