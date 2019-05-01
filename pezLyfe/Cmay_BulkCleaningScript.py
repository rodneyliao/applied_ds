# -*- coding: utf-8 -*-
"""
The data from the original kickstarter dataset is from four different scrape dates

Between scrape dates, webrobots.io must have changed the script they used to pull the data

The column labels are different across files, so we need to normalize them

This script drop labels that aren't included in the original 2016 version of the dataset
"""

import pandas as pd
import re
import json
import math  as mt
import os

if not os.path.exists('2019Merged_test.csv'):
    print('reading files from box')
    nineteenData = pd.read_csv('https://tufts.box.com/shared/static/zc0tobgsu34jqu4msxxnpdqrl5rpfzue.csv')
    print('Writing file locally for later use')
    nineteenData.to_csv('2019Merged_test.csv', sep = ',')
    
else:
    print('reading files from directory')
    nineteenData = pd.read_csv('2019Merged_test.csv')


#Make a list with all of the columns names we want to drop from the dataframes
dropColumns = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'currency_symbol', 'friends', 'is_backing', 'is_starred', \
               'permissions', 'photo', 'pledged', 'disable_communication', 'is_starrable', 'permissions', \
               'is_starable', 'current_currency', 'converted_pledged_amount', \
               'usd_type']

def columnDrop(file, labels):
    '''This function cycles through the column names in the dropColumns list. For each item in the 
    dropColumns list, the script tries to drop the column. If the column doesn't exist, it prints
    a quick alert message
    '''
    for label in labels:
        try:
            file.drop(labels = label, axis = 1, inplace = True)
        except: 
            print('label not in axis')

#Now run the columnDrop function on each of the files
columnDrop(nineteenData, dropColumns)

def catJson(target):
    '''
    This function is used to pull the correct JSON object out of the category row of the
    temporary dataframe used
    '''
    return(target['name'])

def fcJson(target):
    '''
    This function is used to pull the parent category from the JSON object. Start by calling the
    full category label from the JSON object, then split it at the forward slash and extract the
    first item in the resulting list
    '''
    y = re.split('/', target['slug'])
    return(y[0])
    
#Need to review the location splits for international spots to be sure the list location makes sense
def cityJson(target):
    return(target['short_name'])

def ctryJson(target):
    return(target['country'])
    
def creatorJson(target):
    return(target['id'])
    
#This function separates the strings by :, ',', and "" characters. The function returns URL for rewards categories
def nameSplit(target):
    '''This function pulls out the url for project rewards from the url column which lists various
    urls associated with the project
    '''
    x = re.split('\W+', target)
    result = x[2]
    return(result)

#This function separates the strings by :, ',', and "" characters. The function returns URL for rewards categories
def rewardsSplit(target):
    '''This function pulls out the url for project rewards from the url column which lists various
    urls associated with the project
    '''
    x = re.split(': | , |"', target)
    result = x[9]
    return(result)
    
def creDelta(target, origin):
    '''
    This function calculates the difference in time between one column and the 
    created date of a kickstarter project
    '''
    delta = target - origin
    return(delta) 
    
print('Dropping rows with empty spaces')
try:
    nineteenData.dropna(axis = 0, how='any', thresh = None, subset = None, inplace = True)
except:
    pass
print('Empty rows dropped')
'''
Since the entries are scraped from the kickstarter website, some creators didn't add locations
to their projects. We can't impute the location, and the number of these projects is small,
so dropping is the best option
'''
print('Dropping Redundant Indices')
try:
    nineteenData.drop(labels = 'Unnamed: 0', axis = 1, inplace = True)
except:
    pass
print('Redundant Indices dropped')

print('Category Function Start')
nineteenData['category'] = nineteenData['category'].apply(json.loads)

print('Name Function Start')
nineteenData['creator'] = nineteenData['creator'].apply(nameSplit)
 
print('Location Function Start')
nineteenData['location'] = nineteenData['location'].apply(json.loads)

print('Rewards Function Start')
nineteenData['urls'] = nineteenData['urls'].apply(rewardsSplit)

print('resetting index')
nineteenData.reset_index(inplace = True) #reset the index because we dropped some rows
try:
    nineteenData.drop(labels = 'index', axis = 1, inplace = True)
except:
    pass
print('index reset')

print('loading subcategories')
nineteenData['subcats'] = nineteenData['category'].apply(catJson)
print('loading categories')
nineteenData['fullcats'] = nineteenData['category'].apply(fcJson)
print('loading cities')
nineteenData['city'] = nineteenData['location'].apply(cityJson)
print('loading countries')
nineteenData['country'] = nineteenData['location'].apply(ctryJson)

print('dropping unused columns')
nineteenData.drop(labels = ['location','category', 'source_url', 'currency_trailing_code', \
                 'static_usd_rate', 'profile'], axis = 1, inplace = True)

'''
The following functions calculate the amount of time that's passed between a few different analysis points
- The amount of time passed between creating the project and launching the project
- The amount of time passed between launching the project and the project deadline
- The amount of time passed between launching the project and the project changing states
'''
print('Calculating Launch Deltas')
nineteenData['creLauDelta'] = nineteenData.apply(lambda x: mt.floor((x['launched_at']-x['created_at'])/60/60/24), axis = 1)

print('Calculating Deadline Deltas')
nineteenData['lauDeadDelta'] = nineteenData.apply(lambda x: mt.floor((x['deadline']-x['launched_at'])/60/60/24), axis = 1)

print('Calculating State Change Deltas')
nineteenData['staLauDelta'] = nineteenData.apply(lambda x: mt.floor((x['state_changed_at']-x['launched_at'])/60/60/24), axis = 1)

print('Tagging projects that originated from Kickstarter.com')
nineteenData['source'] = 'Kickstarter'

print('Calculating % of funding goal reached')
nineteenData['funds_raised_percent'] = nineteenData.apply(lambda x: x['usd_pledged'] / x['goal'] * 100, axis = 1)

print('exporting to .csv file')
nineteenData.to_csv('2019KickDataCleaned.csv', sep = ',')
