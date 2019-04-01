import pandas as pd
import numpy as np
import math
import pdb


def average(series):
    return sum(series)/len(series)


def standard_deviation(series):
    y=average(series)
    n = 0 
    for i in series:
        n = n + (i-y)**2
    x = len(series)
    return math.sqrt(n/(x-1))


def median(series):
    t = len(series)
    if t < 1:
            return None
    if t % 2 == 1:
            return sorted(series)[t//2]
    else:
            return sum(sorted(series)[t//2-1:t//2+1])/2
   
