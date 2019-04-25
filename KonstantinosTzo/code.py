import pandas as pd
import numpy as np
import math
import pdb
import random
from math import sqrt



def average(series):

    y = len(series)
    x = sum(series)

    av = x/y
    return(av)
    

def standard_deviation(series):

    r = 0
    aver = average(series)

    for x in range (len(series)):
        k = abs( series[x] - aver)**2
        r = r + k
    
    
    ss = r/(len(series)-1)
    if ss>0 :
        return (sqrt(ss))
    else:
        return(n/a)
    """
    implements the sample standard deviation of a series from scratch
    you may need a for loop and your average function
    also the function math.sqrt
    you should get the same result as calling .std() on your data
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.std.html
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html
    """


def median(series):

    l=sorted(series)
    t= len(l)

    if t<1:
        return None
    if t % 2 == 0:
        return (l[int(t/2)] + l[int(t/2)-1]) / 2
    else:
        return l[int((t-1)/2)]
    

    """
    finds the median of the series from scratch
    you may need to sort your values and use
    modular division
    this number should be the same as calling .median() on your data
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.median.html
    https://pandas.pydata.org/pandas-docs/version/0.23.0/generated/pandas.Series.median.html
    """