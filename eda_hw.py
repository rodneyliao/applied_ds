import pandas as pd
import numpy as np
import math
import pdb

def average(series):
    
    average = sum(series)/len(series)
    return average
    pass

def standard_deviation(series):
 
    lstlen= len(series)
    sqDiff= 0
    variance = 0
    for index in series:
        sqDiff= ((index-average(series))**2)
        variance += sqDiff
    std = math.sqrt(variance/lstlen)
    return std

def median(series):
    
    sortedSeries= sorted(series)
    lstlen= len(series)
    
    if (lstlen % 2) == 0:
        median = (sortedSeries[round(lstlen/2)]+sortedSeries[round(lstlen/2+1)])/2
    else:
        median = sortedSeries[(lstlen+1)/2]
        
    return median 
  
