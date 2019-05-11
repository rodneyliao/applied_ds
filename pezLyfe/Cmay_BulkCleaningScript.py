# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os
import zipfile
import requests
import io
import re
import json
import math  as mt

url = 'https://s3.amazonaws.com/weruns/forfun/Kickstarter/Kickstarter_2019-02-14T03_20_04_734Z.zip'
f = 'Kickstarter_2019-02-14T03_20_04_734Z.zip'
loc = os.getcwd()
cmay_dump = os.path.join(loc, r'kick_web_data')

if not os.path.exists(cmay_dump):
    print('Creating new folder for zip file')
    os.makedirs(cmay_dump)
else:
    pass

print('requesting Kickstarter data')
r = requests.get(url)
if r.ok == True:
    print('Request returned ok')
else:
    print('Download request failed')

z = zipfile.ZipFile(io.BytesIO(r.content))
print('extracting zipped data' )
z.extractall(cmay_dump)

os.chdir(cmay_dump)
print('Merging files in a single .csv')
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
    
def cityJson(target):
    return(target['short_name'])

def ctryJson(target):
    return(target['country'])
    
def creatorJson(target):
    return(target['id'])
    
def nameSplit(target):
    '''This function pulls out the url for project rewards from the url column which lists various
    urls associated with the project
    '''
    x = re.split('\W+', target)
    result = x[2]
    return(result)

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
    
#Run the columnDrop function on each of the files
columnDrop(mergedData, dropColumns)
    
print('Dropping rows with empty spaces')
try:
    mergedData.dropna(axis = 0, how='any', thresh = None, subset = None, inplace = True)
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
    mergedData.drop(labels = 'Unnamed: 0', axis = 1, inplace = True)
except:
    pass
print('Redundant Indices dropped')

print('Category Function Start')
mergedData['category'] = mergedData['category'].apply(json.loads)

print('Name Function Start')
mergedData['creator'] = mergedData['creator'].apply(nameSplit)
 
print('Location Function Start')
mergedData['location'] = mergedData['location'].apply(json.loads)

print('Rewards Function Start')
mergedData['urls'] = mergedData['urls'].apply(rewardsSplit)

print('resetting index')
mergedData.reset_index(inplace = True) #reset the index because we dropped some rows
try:
    mergedData.drop(labels = 'index', axis = 1, inplace = True)
except:
    pass
print('index reset')

print('loading subcategories')
mergedData['subcats'] = mergedData['category'].apply(catJson)
print('loading categories')
mergedData['fullcats'] = mergedData['category'].apply(fcJson)
print('loading cities')
mergedData['city'] = mergedData['location'].apply(cityJson)
print('loading countries')
mergedData['country'] = mergedData['location'].apply(ctryJson)

print('dropping unused columns')
mergedData.drop(labels = ['location','category', 'source_url', 'currency_trailing_code', \
                 'static_usd_rate', 'profile'], axis = 1, inplace = True)

'''
The following functions calculate the amount of time that's passed between a few different analysis points
- The amount of time passed between creating the project and launching the project
- The amount of time passed between launching the project and the project deadline
- The amount of time passed between launching the project and the project changing states
'''
print('Calculating Launch Deltas')
mergedData['creLauDelta'] = mergedData.apply(lambda x: mt.floor((x['launched_at']-x['created_at'])/60/60/24), axis = 1)

print('Calculating Deadline Deltas')
mergedData['lauDeadDelta'] = mergedData.apply(lambda x: mt.floor((x['deadline']-x['launched_at'])/60/60/24), axis = 1)

print('Calculating State Change Deltas')
mergedData['staLauDelta'] = mergedData.apply(lambda x: mt.floor((x['state_changed_at']-x['launched_at'])/60/60/24), axis = 1)

print('Tagging projects that originated from Kickstarter.com')
mergedData['source'] = 'Kickstarter'

print('Calculating % of funding goal reached')
mergedData['funds_raised_percent'] = mergedData.apply(lambda x: x['usd_pledged'] / x['goal'] * 100, axis = 1)

print('exporting to .csv file')
mergedData.to_csv('2019KickDataCleaned.csv', sep = ',')   