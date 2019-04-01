import pandas as pd
import numpy as np
import math
import pdb

   
dataset = pd.read_csv('https://storage.googleapis.com/project-sunroof/csv/latest/project-sunroof-census_tract.csv')
df = pd.DataFrame(dataset)
col = [18]
df = df[df.columns[col]]

def average(series):
 
    length = len(series)
    total = sum(series)
    average = total/length
    return(average)

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
    stDev = []
    avg = average(series)
    length = len(series)
    for i in series:
        stDev.append((i-avg)**2)
    ss = sum(stDev)
    standard_deviation = math.sqrt((ss/(length-1)))
    return(standard_deviation)
    

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
    sortedData = sorted(series)
    num = len(series)
    if (num%2)==0:
        tempnum = len(series)/2
        tempnumlow = int(tempnum)
        tempnumhigh = int(tempnum)-1
        median = (sortedData[tempnumlow]+sortedData[tempnumhigh])/2
    else:
        index = len(series)/2
        median = sortedData[index]
    print(median)
    return(median)


