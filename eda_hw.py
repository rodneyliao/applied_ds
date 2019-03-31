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
    avgnumber = sum(series) / len(series)
    return avgnumber


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
    for each in series:
        sum = sum + pow((each-a),2)
    stdnumber = math.sqrt(sum/(len(series)-1))
    return stdnumber


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

    length = len(series)
    for j in range(length - 1):
        t = 0
        for i in range(0, length - 1 - j):
            if series[i] > series[i + 1]:
                temp = series[i+1]
                series[i + 1] = series[i]
                series[i] = temp
                t += 1
        if t == 0:
            break
    if length/2 == int(length/2):
        mediannumber = (series[length//2-1]+series[length//2])/2
    else:
        mediannumber = series[length//2]
    return mediannumber
    
