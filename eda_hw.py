import pandas as pd
import numpy as np
import math
import pdb

def average(series):

    return sum(series) / len(series)
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

def standard_deviation(series):

    avg = average(series)
    ser_len = float(len(series))
    stdsum = 0
    for i in range(0, len(series)):
        stdsum += (series[i] - avg)**2


    return math.sqrt(stdsum / (ser_len - 1.0))
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

def median(series):

    ser_sort = np.sort(series)
    while len(ser_sort) > 2:
        ser_sort = ser_sort[1:len(ser_sort)-1]

    if len(ser_sort) == 1:
        return ser_sort[0]
    else:
        return (ser_sort[0] + ser_sort[1]) / 2
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
