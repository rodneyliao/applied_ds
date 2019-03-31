import pandas as pd
import numpy as np
import math
import pdb


def average(series):
    a1 = sum(series)
    b1 = len(series)
    c1 = a1/b1
    """
    print(c1)
    """
    
    return c1
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
    """
        things = [1,3,5,7,9]
        average(things)
    """
def standard_deviation(series):
    a1 = average(series)
    sum1 = 0
    for i in range(0,len(series)):
        sum1 = sum1 + (series[i]-a1)**2
    b1 = sum1 / (len(series)-1)
    c1 = math.sqrt(b1)
    """
    print(c1)
    """
    return c1

    """
    implements the sample standard deviation of a series from scratch
    you may need a for loop and your average function
    also the function math.sqrt
    you should get the same result as calling .std() on your data
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.std.html
    See numpy documenation for implementation details:
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html

    """
    """
    things = [1,3,5,7,9]
    standard_deviation(things)
    print(np.std(things))
    """

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

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
    a1 = bubbleSort(series)
    print(a1)
    b1 = len(a1)
    med = 0
    if b1%2 == 0:
        med = (a1[b1/2]+a1[b1/2 + 1])/2

    else:
        med = (a1[b1//2])
    return med
    """
    things = [3,5,9,7,1]
    median(things)
    """
