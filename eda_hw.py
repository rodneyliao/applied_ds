import pandas as pd
import numpy as np
import math
import pdb


def average(series):
    '''Returns the average of a series'''
    sum = np.sum(series) # calculate sum of all the elements
    count = len(series) # count the elements in the series
    mean = sum / count
    return mean


def standard_deviation(series):
    '''Returns the sample standard deviation of a series'''
    mean = average(series)
    count = len(series) - 1
    squared_deviations = np.square(np.subtract(series, mean))
    sample_sd = np.sqrt(np.sum(squared_deviations) / count)
    return sample_sd

def median(series):
    '''Returns the median of a series'''
    count = len(series)
    sorted = np.sort(series)
    midpoint = math.floor(count / 2)
    if count % 2 != 0:
        median = sorted[midpoint]
    else:
        median = (sorted[midpoint] + sorted[midpoint-1]) / 2
    return median
