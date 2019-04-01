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
    pass
    a = sum(series) / len(series)
    return a


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
    pass
    a = average(series)
    sum = 0
    for i in series:
        sum = sum + pow((i - a),2)
    b = math.sqrt(sum/(len(series)-1))
    return b

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
    pass
    n = len(series)
    for j in range(n - 1):
        count = 0
        for i in range(0, n - 1 - j):
            if series[i] > series[i + 1]:
                series[i], series[i + 1] = series[i + 1], series[i]
                count += 1
        if 0 == count:
            break
            
    if n/2 == int(n/2):
        c = series[n//2-1] + series[n//2]
        d = c/2
        return d
    else:
        c = series[n//2]
        return c
