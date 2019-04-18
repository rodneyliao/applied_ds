# %% md
## Import and Initial Cleaning of the Ground Value Dataset
### General Description
# As part of my project in the Tufts class EM212: Applied Datascience, I will
# try to analyse two datasets:
# *   the District Profiles (2007 to 2017) Dataset, containing socio-demographic information about Hamburg's districts
# *   the Ground Value (1964 to 2017) Dataset, containing estimates of the ground value of real estate in Hamburg,
# on an individual property level in Euros / $m^2$

### Information on the Ground Value Dataset
# Each year, the city of Hamburg publishes rough estimates of the value of
# real estate on property level. The so-called "Bodenrichtwert" (abbr. BRW, "reference ground value")
# is the value of a particular property broken down to a $1m^2$ plot of land at a certain location (measured in coordinates).
# The calculation of the BRW takes the following features into account:
# *   location (x,y coordinates)
# *   suitability for development and use (categorical)
# *   current development / use (categorical)
# *   size of the plot
#
# A recent, detailed description of the data and the features used in the calculation is available
# [here (in German)](https://www.hamburg.de/contentblob/10917486/73e458aa8a5e46f772eacb2b00b4c393/data/d-brw-erlaeuterungen-2017.pdf).
# Additional information is available [here (also in German)](https://www.hamburg.de/bsw/grundstueckswerte/7916004/bodenrichtwert-erlaeuterungen/)

# The City of Hamburg makes this data available through its [Open Data Portal](http://suche.transparenz.hamburg.de/dataset/bodenrichtwerte-fur-hamburg6?forceWeb=true).
# Unfortunately, the data is split up into multiple CSV files, each representing
# one year of observations. In order to work with this dataset, I will download
# the individual CSVs, import them into pandas DataFrames, merge these together
# and save the result as a CSV file.

### Heads Up:
# In order to download and process and store the data, about 4GB of free disk space is required.

# %%
# import necessary libraries
import requests
import glob
import pandas as pd
import numpy as np
import datetime
import sys
import re

# %% md
# Only execute the next cell if you would like to download the whole dataset.
# The cell will take a long time to complete, as the server does not seem to offer
# fast download speeds.
# %%
with open("urls.txt") as file:
    urls = [line.rstrip('\n') for line in file]

def download(urls):
    '''Downloads the files specified in list urls'''
    for url in urls:
        successful = 0
        count = len(urls)
        filename = url.rsplit('/', 1)[1]
        print("Downloading " + filename + " (" + str(successful) + "/" + str(count) + " completed)...")
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        print("Done.")
        current += 1

download(urls) # start the download


# %% md
# Assuming that the downloaded CSV files are now present in the working directory,
# I will import them into pandas DataFrames and join these into a larger one:
# %%
files = glob.glob("*.csv") # aggregate all csv files for reading
files = sorted(files) # sort files to start with the smallest one
files

# import the data from the CSV files
dfs = []
for file in files:
    print("Reading file " + file + "...")
    dfs.append(pd.read_csv( file,
                            sep="|",
                            header=0,
                            encoding="ISO-8859-1" # this encoding seems to be correct
                            ))
print("Concatening dataframes...")
data = pd.concat(dfs, axis=0, ignore_index=True)
print("Done.")


# %% md
#### Initial Data Survey and Cleaning
# Let's take a look at the data. It seems like there are many columns where a
# common ```dtype``` could not be recognized. Because of this, the dataset takes
# up much more storage space than it would if the ```dtypes``` were set properly.
# This should be the first priority before saving the joined dataset to save storage
# space.
# %%
data.head(5)
data.info()

# %% md
# From the [dataset metadata information sheet](https://www.hamburg.de/contentblob/8025502/a106909f7f9c11b8d90312a99a5b62c8/data/d-vboris-modellbeschreibung.pdf),
# I have the following list of
# variable names and their description. I will first identify those that I will
# not be using in my data analysis and can thus drop:

# | Variable Name | Description                                      | ```dtype``` / drop |
# |---------------|--------------------------------------------------|--------------------|
# | GESL          | Ward (code)                                      | drop               |
# | GENA          | Ward (name)                                      | drop               |
# | GASL          | Surveying institution (code)                     | drop               |
# | GABE          | Surveying institution (name)                     | drop               |
# | GENU          | Land Survey Registry (code)                      | drop               |
# | GEMA          | Land Survey Registry (name)                      | drop               |
# | ORTST         | District (name)                                  | category           |
# | WNUM          | Ground Value Number (code)                       | drop               |
# | BRW           | Ground Value                                     | float              |
# | STAG          | Observation / Survey Date                        | date (dd.mm.yyyy)  |
# | BRKE          | kind of ground value                             | integer            |
# | BEDW          | "Requirements value"                             | drop               |
# | PLZ           | zip code                                         | integer            |
# | BASBE         | base map reference                               | drop               |
# | BASMA         | base map scale                                   | drop               |
# | YWERT         | BRW geo-reference (east)                         | integer            |
# | XWERT         | BRW geo-reference (north)                        | integer            |
# | BEZUG         | coordinate system used                           | drop               |
# | ENTW          | current state of development                     | category           |
# | BEIT          | development state according to taxes             | category           |
# | NUTA          | kind of current usage                            | category           |
# | ERGNUTA       | extension of NUTA                                | category           |
# | BAUW          | current building type                            | category           |
# | GEZ           | number of floors                                 | float              |
# | WGFZ          | number of floors relevant for BRW                | float              |
# | GRZ           | site coverage factor                             | float              |
# | BMZ           | cubic index                                      | float              |
# | FLAE          | site area  in $m^2$                              | float              |
# | GTIE          | site depth  in meters                            | float              |
# | GBREI         | site width in meters                             | float              |
# | ERVE          | accessibility                                    | category           |
# | VERG          | zoning city development information              | category           |
# | VERF          | state of remediation                             | category           |
# | YVERG         | coordinate of city planning measure (east)       | drop               |
# | XVERG         | coordinate of city planning measure (north)      | drop               |
# | BOD           | kind of ground                                   | float              |
# | ACZA          | index value of agricultural land                 | drop               |
# | GRZA          | index value of agricultural land                 | drop               |
# | AUFW          | historical reference for reforestation           | drop               |
# | WEER          | accessible roads for agriculture / forestry      | drop               |
# | KOORWERT      | geo-reference polygon for BRW zone               | drop               |
# | KOORVERF      | geo-reference polygon for city planning measures | drop               |
# | BEM           | notes                                            | drop               |

# As a first step, I will mark the selected columns to be dropped:
# %%
cols_to_drop = [    "GESL", "GENA", "GASL", "GABE", "GENU", "GEMA",
                    "WNUM", "BEDW", "BASBE", "BASMA", "BEZUG", "YVERG",
                    "XVERG", "ACZA", "GRZA", "AUFW", "WEER", "KOORWERT",
                    "KOORVERF", "BEM" ]


# %% md
# Next, I will list all columns that were not detected as being numerical:
# %%
non_numerical = pd.DataFrame(data.select_dtypes(exclude="number").dtypes).reset_index()
non_numerical


# %% md
# I know that there are some column that are empty or that only contain one value.
# I wrote a function that should check each column for this condition and then
# save its only value and mark it to be dropped from the main dataset.
#
# The following columns appear to be empty or contain only one value, which has been saved in
# ´´´saved_info´´´. They can thus be dropped from the main dataset.
# %%
saved_info = {} # dictionary for info that might be useful, but does not need to be in dataframe

def save_info_and_mark(drop=cols_to_drop, save=saved_info, df=data):
    """If a column only contains one unique value, save it into save and mark to column to be dropped"""
    for column in df:
        unique_values = df[column].unique()
        if len(unique_values) == 1:
            save[column] = df[column].unique()[0]
            if column not in drop:
                drop.append(column)
    return save, drop

# iterate over all columns in non-numerical and check for columns containing only one value,
# save its content and mark it to be dropped
saved_info, cols_to_drop = save_info_and_mark()

almost_empty = pd.DataFrame(saved_info, index=[0]).transpose().reset_index() # show the stored content
almost_empty.columns = ["column", "only value"]
almost_empty

# %% md
# It is now time to actually drop the columns that I earmarked:
# %%
data.drop(columns=cols_to_drop, inplace=True)

# %% md
# Let's take a closer look at the remaining columns:
# %%
# list the remaining non-numerical columns
non_numerical = pd.DataFrame(data.select_dtypes(exclude="number").dtypes).reset_index()
non_numerical

unique = {}
for column in non_numerical["index"]: # list the unique values of the remaining non numerical columns
    unique[column] = data[column].unique()
unique


# %% md
# It looks like there are a few more columns that I can drop or convert:
# *   ORTST contains the district names, I will make it categorical
# *   STAG holds the date the real estate evaluation was done for, so convert it to datetime
# *   PLZ holds ZIP codes and can safely be converted to integer
# *   there appear to be some categorical variables, I will convert them to categorical format
#     - ENTW
#     - NUTA
#     - ERGNUTA
#     - BAUW
#     - VERG
#     - VERF
# *   FREI seems very messy, I will try to work without it for now
# *   BRZNAME holds only a few addresses, I will not need it for my analysis
# *   LUMNUM contains a reference to the PDF holding the corresponding metadata, should be safe to drop
# %%
cols_to_drop = ["FREI", "BRZNAME", "LUMNUM"] # drop these columns
data.drop(columns=cols_to_drop, inplace=True)

data.ORTST = data.ORTST.astype("category") # convert ORTST to category
data.STAG = pd.to_datetime(data.STAG, format="%d.%m.%Y") # convert STAG to datetime
data.PLZ = pd.to_numeric(data.PLZ, downcast="integer", errors="coerce") # convert PLZ to numerical, it contains some strings
# convert BASBE, ENTW, NUTA, ERGNUTA, BAUW, VERG, VERF, BEM to categorical
to_convert = ["ENTW", "NUTA", "ERGNUTA", "BAUW", "VERG", "VERF"]
for var in to_convert:
    data[var] = data[var].astype("category")


# %% md
# Let's check if there are any columns that only contain missing values. These can be dropped
# as well:
# %%
for column in data:
    if data[column].isnull().all():
        data.drop(columns=column, inplace=True)
        print("Dropped column " + column)


# %% md
# It looks like there are some issues with the German Umlauts in ORTST:
# %%
data.ORTST.loc[data.ORTST.str.contains("Ã")].unique()


# %% md
# The problem seems to be wrong encoding:
# - "ß" has been replaced with "Ã"
# - "ü" has been replaced with "Ã¼"
# - "ö" has been replaced with "Ã¶"
# I will try to undo these changes:
# %%
def revert_encoding(s):
    if "Ã¶" in s:
        return s.replace("Ã¶", "ö")
    if "Ã¼" in s:
        return s.replace("Ã¼", "ü")
    if "Ã\x9f" in s:
        return s.replace("Ã\x9f", "ß")
    return s

data.ORTST = data.ORTST.apply(revert_encoding) # apply the new function to the ORSTS column
data.ORTST = data.ORTST.astype("category") # convert ORTST to category again
pd.DataFrame(item for item in data.ORTST.unique()) # this looks much better!


# %% md
# The somewhat reduced dataset now looks like this:
# %%
data.head(5)
data.info()


# %% md
# With the basic cleaning done, I can now store the dataset as a pickle file.
# Since it is still rather large, I will compress it after pickling:
# %%
data.to_pickle("../data/joined_ground_values.pkl.zip")


# %% md
#### Preparing the dataset for merging
# Assuming the data has been saved into ```../data/joined_ground_values.pkl``` before,
# it is possible to continue from this cell:
# %%
data = pd.read_pickle("../data/joined_ground_values.pkl.zip")

# %% md
# Since the other dataset (district profiles) is on a district-year-level, I need to collapse this dataset
# over districts and years. For this step, it is important to know which variables
# can be collapsed in a meaningful way. For example, it does not make sense to
# collapse the zip codes using an average. Since my analysis will focus on the ground value,
# I will first collapse only this column by district (```ORTST```) and year (```STAG```). In
# the collapsed dataset, I will use the new column name ```GV``` for the ground value.
# Since the average of the ground values might be skewed by expensive clusters within
# districts, I will also include the median and some descriptive statistics while collapsing:
# %%
to_collapse = data[["ORTST", "STAG", "BRW"]]
to_collapse.columns = ["district", "year", "GV"]
to_collapse["year"] = to_collapse["year"].dt.year # preserve only the year for now

collapsed = to_collapse.groupby(["district", "year"]).mean()
collapsed.columns = ["GV_mean"]
collapsed["GV_median"] = to_collapse.groupby(["district", "year"]).median()
collapsed["GV_std"] = to_collapse.groupby(["district", "year"]).std()
collapsed["GV_count"] = to_collapse.groupby(["district", "year"]).count()["GV"]
collapsed.head()

# %% md
# Looks like everything went well! It is now time to store the finished dataset and
# continue with the data analysis (see ```data-analysis``` notebook).
# %%
collapsed.to_pickle("../data/collapsed_ground_values.pkl") # holds collapsed data across all years
