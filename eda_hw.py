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
    return float(sum(series)) / max(len(series), 1)


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
    n = len(series)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    mean = average(series)
    numerator = sum((x - mean) ** 2 for x in series)
    return (numerator/(n-1)) ** 0.5


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
    l = sorted(series.tolist())
    l = sorted(l)
    if n % 2 == 1:
        return l[math.floor(n/2)]
    else:
        return (l[int(n/2)] + l[int(n/2 - 1)])/2
series = pd.Series(np.array([6, 1, 3, 9, 7]))


