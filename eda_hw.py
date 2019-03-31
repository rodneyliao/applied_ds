import pandas as pd
import numpy as np
import math
import pdb

def average(series):
   
    # implements average of pandas series from scratch    
    avg = sum(series)/len(series)
    return avg
    pass

def standard_deviation(series):
   
    # implements sample standard deviation of a series from scratch
    
    # go through loop to find variance
    n = len(series)
    sqDiff = 0
    variance = 0
    for idx in series:
        sqDiff = ((idx - average(series))**2)
        variance += sqDiff
    std = math.sqrt(variance/n)
    
    return std
    pass

def median(series):
   
    # implements median of series from scratch
    
    #sorts series
    s = sorted(series)
    n = len(series)
    m = n+1
    
    # determines whether even or odd and determines median
    if (n % 2) == 0:
        return (s[int(n/2)]+ s[int(n/2)+1])/2
    else:
        return s[int(m/2)]
    
    pass
