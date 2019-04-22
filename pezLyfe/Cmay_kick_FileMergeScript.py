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

'Make a list with all of the columns names we want to drop from the dataframes'
dropColumns = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'currency_symbol', 'friends', 'is_backing', 'is_starred', \
               'permissions', 'photo', 'pledged', 'disable_communication', 'is_starrable', 'permissions', \
               'is_starable', 'current_currency', 'converted_pledged_amount', \
               'usd_type']
        
'Read each .csv file into a dataframe'
nineteenData = pd.read_csv('2019Merged.csv')

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

'Now run the columnDrop function on each of the files'
columnDrop(nineteenData, dropColumns)

'And export each dataframe'
nineteenData.to_csv('2019Short.csv', sep = ',')
   