# -*- coding: utf-8 -*-
"""
The data from the original kickstarter dataset is from four different scrape dates

Between scrape dates, webrobots.io must have changed the script they used to pull the data

The column labels are different across files, so we need to normalize them

This script drop labels that aren't included in the original 2016 version of the dataset
"""

import pandas as pd
import os
import re
import json

sixteenData = pd.read_csv('2016Short.csv')
seventeenData = pd.read_csv('2017Short.csv')
eighteenData = pd.read_csv('2018Short.csv')
nineteenData = pd.read_csv('2019Short.csv')

#Since some subcategories and parent categories use more than one word, I'm going to have
# to fix this. Use one functions to pull the slug out of the shit, and then split on the slah
# if that's possible
def catStrip(target): 
    '''
    This function strips out the parent category and subcategory of the project
    The regex.split method with r'\W+' splits the input string at all non-alphanumeric characters
    The list locations where the parent/subcategory are change between scrape dates
    So the correct positions have to be chosen for each
    '''
    x = re.split(': | , |"', target)
    return(x[23]) #This is for the 2016 version of the dataset only
    
#def subcatStrip(target): 
    '''
    This function strips out the parent category and subcategory of the project
    The regex.split method with r'\W+' splits the input string at all non-alphanumeric characters
    The list locations where the parent/subcategory are change between scrape dates
    So the correct positions have to be chosen for each
    '''
#    x = re.split(r'\W+', target) 
#    return(x[11])
    

def nameStrip(target):
    '''
    This functions strips out the creator id from the creator column of the dataset
    Since we're only interested in tying the creator back to the creator profile, we're only
    extracting the creator ID in this function
    This also allows us to leave out potential personal identifying information
    '''
    x = re.split(r'\W+', target)
    results = x[26]
    return(results)
    
def nameStrip2018(target):
    '''
    This functions strips out the creator id from the creator column of the dataset
    Since we're only interested in tying the creator back to the creator profile, we're only
    extracting the creator ID in this function
    This also allows us to leave out potential personal identifying information
    '''
    x = re.split(r'\W+', target)
    results = x[29]
    return(results)
   
#Need to review the location splits for international spots to be sure the list location makes sense
def locSplit(target):
    '''
    This function does the same thing as the previous two, except for locations
    '''
    x = re.split(': | , |"', target)
    result = x[29]
    return(result)

#This function separates the strings by :, ',', and "" characters. The function returns URL for rewards categories
def rewardsSplit(target):
    '''This function pulls out the url for project rewards from the url column which lists various
    urls associated with the project
    '''
    x = re.split(': | , |"', target)
    result = x[9]
    return(result)

print('Dropping rows with empty spaces')
sixteenData.dropna(axis = 0, how='any', thresh = None, subset = None, inplace = True)
seventeenData.dropna(axis = 0, how='any', thresh = None, subset = None, inplace = True)
eighteenData.dropna(axis = 0, how='any', thresh = None, subset = None, inplace = True)
print('Empty rows dropped')
'''
Since the entries are scraped from the kickstarter website, some creators didn't add locations
to their projects. The number of these projects is small, so it shouldn't affect the dataset
too much
'''
    
print('Category Function Start')
sixteenData['category'] = sixteenData['category'].apply(json.loads)
seventeenData['category'] = seventeenData['category'].apply(json.loads)
eighteenData['category'] = eighteenData['category'].apply(json.loads)
nineteenData['category'] = nineteenData['category'].apply(json.loads)
print('Cateogry Function Complete')

#I got an error when using the name function and json.loads, so it's back to the old style
print('Name Function Start')
sixteenData['creator'] = sixteenData['creator'].apply(nameStrip)
seventeenData['creator'] = seventeenData['creator'].apply(nameStrip)
eighteenData['creator'] = eighteenData['creator'].apply(nameStrip)
nineteenData['creator'] = nineteenData['creator'].apply(nameStrip)
print('Name Function Complete')
 
print('Location Function Start')
sixteenData['location'] = sixteenData['location'].apply(locSplit)
seventeenData['location'] = seventeenData['location'].apply(locSplit)
eighteenData['location'] = eighteenData['location'].apply(locSplit)
nineteenData['location'] = nineteenData['location'].apply(locSplit)
print('Location Function Complete')

print('Rewards Function Start')
sixteenData['urls'] = sixteenData['urls'].apply(rewardsSplit)
seventeenData['urls'] = seventeenData['urls'].apply(rewardsSplit)
eighteenData['urls'] = eighteenData['urls'].apply(rewardsSplit)
nineteenData['urls'] = nineteenData['urls'].apply(rewardsSplit)
print('Rewards Function Completed')
   