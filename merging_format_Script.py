# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os
import re

mergedData = pd.DataFrame() #Initialize an empty Pandas datafrme
for filename in os.listdir(): #Make an iterator for all files in this directory
    try: 
        tempDF = pd.read_csv(filename)
        mergedData = mergedData.append(tempDF, ignore_index = False)
        print(filename, len(mergedData))
    except: 
        print('non-CSV')
        
mergedData.reset_index()

try: #If there's unnamed columns leftover from old indices, drop them
    mergedData.drop('Unnamed: 0', axis = 1, inplace = True)
except: #If there's not, then leave it alone and print a message
    print('No old indices to drop')     

try: # If there's an old named index column, drop that
    mergedData.drop('index', axis = 1, inplace = True)
except: #If not, then leave it alone and print a message
    print('No index to drop')
    
mergedData.to_csv('fullMerged.csv', sep = ',')

column_names = list(mergedData.columns.values)
columns = pd.DataFrame()
columns['Names'] = column_names
columns.to_csv('originalColumns.csv', sep = ',')
    
'''
#Need to update the categoryStrip function to split out the paraent/subcategory
##def catStrip(target): #Define a function to strip info from the category column
   # x = re.split(': | , |"', target)
   # results = [x[5], x[9]]
   # return(results)
    
#Need to update the nameStrip function to break out Name and creator ID's 
#def nameStrip(target):
#    x = re.split(': | , |"', target)
#    results = [x[2], x[5]]
#    results[0] = results[0].strip(':')
#    results[0] = results[0].strip(',')
#    print(results)
   
#This function separates the strings by :, ',', and "" characters. The function returns the City, State for US and City, Country for international
def locSplit(target):
    x = re.split(': | , |"', target)
    result = x[13]
    return(result)

#This function separates the strings by :, ',', and "" characters. The function returns URL for rewards categories
def rewardsSplit(target):
    x = re.split(': | , |"', target)
    result = x[9]
    return(result)
'''
   
   