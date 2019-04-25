# %% md
## Import and Initial Cleaning of the District Profiles Dataset
### General Description
# As part of my project in the Tufts class EM212: Applied Datascience, I will
# try to analyse two datasets:
# *   the District Profiles (2007 to 2017) Dataset, containing socio-demographic information about Hamburg's districts
# *   the Ground Value (1964 to 2017) Dataset, containing estimates of the ground value of real estate in Hamburg,
# on an individual property level in Euros / $m^2$

### Information on the District Profiles Dataset
# The dataset consists of two parts and provided by [Statistik Nord](https://www.statistik-nord.de) at
# *   [Profiles 2007 to 2016](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/Stadtteilprofile-Berichtsjahre-2007-2016.xlsx)
# *   [Profiles 2017](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/StadtteilprofileBerichtsjahr2017.xlsx)
#
# In this notebook, I will import these Excel files into pandas dataframes and save
# them as pickle files for use in my data analysis notebook.

### Heads Up:
# I will use the current path of this notebook to store and manipulate files.

# %%
# import necessary libraries
import pandas as pd
import seaborn as sns
import datetime
import pickle
import re

# %% md
# Because the original German column names used in the Excel sheet are not very easy to
# understand for non-Germans and are also very long and thus difficult to work with, I
# have created a dedicated Excel sheet ```column_titles.xlsx``` which maps the German column names to
# 1.   each other, where they differ across years
# 2.   an abbreviation of the English translation of the column names
# This way, each old German column will be matched to its German counterparts and then
# converted to an English name which I will use in the rest of the analysis.
# The sheet contains missing values for those features which were not observed in particular years.
# %%
coltitles = pd.read_excel(  "../data/column_titles.xlsx",
                            encoding='utf-8')
coltitles.sort_index().head()

# %% md
#### District Profiles from 2007 to 2016

# I will import the 2007-2016 Excel file as a pandas DataFrame. Since the data is stored in sheets,
# the result is an associative array of DataFrames with the sheet names as the keys.
# %%
dfs = pd.read_excel(    "https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/Stadtteilprofile-Berichtsjahre-2007-2016.xlsx",
                        None,
                        skiprows = 3
                    )
dfs.keys() # keys
dfs["Berichtsjahr_2016"].head(5) # df for year 2016


# %% md
# Since the year is contained in each key, I can infer the observation year from the sheet
# name (key) and add it to each sub-df as a new column called "year". I am defining functions
# here because I will have to apply these again to the second dataset (2017 profiles).
# %%
def add_year_to_df(dfs):
    """Reads the year from the sheet name and adds it as a column"""
    for key in dfs.keys():
        year = key.replace(" ", "_").split("_")[1]
        dfs[key]["year"] = year
    return dfs

dfs = add_year_to_df(dfs)

# %% md
# These functions help me match the columns of each DataFrame to the ones present in
# the coltitles DataFrame. I have had some problems with the built-in string matching
# functions that are part of pandas, so I decided to write some myself.
# %%
def tedious_match(col, string):
    """My own function that matches strings better than the built-in tools for some reason"""
    for i in range(0, len(col)):
        if col.iloc[i] == string:
            return True
    return False


def pairs(dfs, names, return_not_found):
    """Returns df containing pairs of old and new titles"""
    result = {}
    not_found = {}
    for key in dfs.keys():
        result[dfs[key].columns[0]] = "district" # first column doesn't have a title in the excel file
        for old_title in dfs[key].columns:
            for new_title in names.columns:
                # assign the new column title to any column that is found in my mapping sheet
                if old_title == names[new_title].any():
                    result[old_title] = new_title
                # I have had some problems with the built-in options, this one seems to work, but is slow!
                elif tedious_match(names[new_title], old_title):
                    result[old_title] = new_title
                else:
                    not_found[old_title] = "not found"
    # convert output to a dataframe
    assignment = pd.DataFrame(result, index=[0])
    result = assignment.transpose()
    result.reset_index(inplace=True)
    result.columns = ["old", "new"]
    if return_not_found:
        not_found = pd.DataFrame(not_found, index=[0])
        not_found = not_found.transpose()
        not_found.reset_index(inplace=True)
        not_found.columns = ["old", "new"]
        return result, not_found
    return result

def list_all_titles(df):
    """Returns a df holding all unique column titles of df"""
    all_titles = []
    for key in df.keys():
        all_titles.extend([title for title in df[key].columns])
    all_titles = pd.DataFrame(all_titles)
    all_titles.columns = ["old"]
    return all_titles.drop_duplicates().reset_index(drop=True)

def find_frame(df, s):
    """Returns a list of the subframes of df a string s occurs in"""
    occurs_in = []
    for key in df.keys():
        if s in df[key].columns:
            occurs_in.append(key)
    return occurs_in

def overwrite_old_colnames(dfs, pairs):
    """Changes the old column name to the new one"""
    result = dfs
    for key in result.keys():
        for old_title in result[key]:
            try:
                new_title = pairs.loc[pairs["old"] == old_title, "new"].values[0]
                result[key].rename(columns={old_title:new_title}, inplace=True)
            except:
                continue
    return result

# %% md
# It is important that all columns are assigned a new column name. To do this, I check if all column titles
# that are present in the Data sheet were found in my prepared reassignment sheet:
# %%
all_old_column_titles = list_all_titles(dfs)
proposed_assignments = pairs(dfs, coltitles, False)
# # perform outer join to receive list of all old titles, indicator makes clear which assignments are missing
merged = all_old_column_titles.merge(proposed_assignments, on="old", how="outer", indicator=True)
# list those titles that have not yet been mapped to a new title and show which sheet they occur in
missing_assignment = merged[merged.isnull().any(axis=1)]
missing_assignment["occurence"] = missing_assignment["old"].apply(lambda x: find_frame(dfs, x))
missing_assignment[["old", "occurence"]]

# %% md
# Since I did not specify a new column name for ```year``` in coltitles, I did not expect
# to find a match with this column. It seems like all other column have been matched
# with a counterpart from my coltitles mapping sheet! These are the proposed assignments:
# %%
proposed_assignments.head() # the first column (district) doesn't have a title in the source

# %% md
# Since the matching process went well, I can now overwrite the old column titles with
# the new, common English ones:
# %%
reassigned_dfs = overwrite_old_colnames(dfs, proposed_assignments)
titles_post_assignment = list_all_titles(reassigned_dfs)
titles_post_assignment.head()

# %% md
# It seems like all column titles have been updated successfully!

# %% md
#### District Profiles for the year 2017

# The newest dataset is from 2018 and holds the observations for the year 2017.
# It comes in another excel sheet that I have to import separately:
# %%
df_2017 = pd.read_excel( "https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/StadtteilprofileBerichtsjahr2017.xlsx",
                        None,
                        skiprows = 3
                        )

# %% md
# The steps taken for the district profiles from 2007 to 2016 should also
# be applicable for the 2017 data:
# %%
df_2017 = add_year_to_df(df_2017) # add year data
all_old_column_titles_2017 = list_all_titles(df_2017)
proposed_assignments_2017 = pairs(df_2017, coltitles, False)
# check for missing assignments
merged_2017 = all_old_column_titles_2017.merge(proposed_assignments_2017, on="old", how="outer", indicator=True)
missing_assignment_2017 = merged_2017[merged_2017.isnull().any(axis=1)]
missing_assignment_2017["occurence"] = missing_assignment_2017["old"].apply(lambda x: find_frame(df_2017, x))
proposed_assignments_2017.head() # proposed reassignments
missing_assignment_2017[["old", "occurence"]]

# %% md
# Again, the only unmatched column is ```year````, for which I do not expect to find a match.
# I proceed with reassigning the new names:
# %%
# reassign column titles
reassigned_df_2017 = overwrite_old_colnames(df_2017, proposed_assignments_2017)
titles_post_assignment_2017 = list_all_titles(reassigned_df_2017)
titles_post_assignment_2017
# one last check
still_unmatched_2017 = titles_post_assignment_2017.merge(all_old_column_titles_2017, on="old")
still_unmatched_2017["occurence"] =  still_unmatched_2017["old"].apply(lambda x: find_frame(df_2017, x))
still_unmatched_2017 # this is expected, as I do not have a "year" column in my mapping sheet

# %% md
# This too seems to have worked. The 2017 data is now ready to be merged with the rest
# of the district profiles dataset.

# %% md
#### Merging the two District Profile Datasets
# This too seems to have worked. In the next step, I have to combine all of the excel
# sheets of the 2007 to 2016 profiles into one single dataframe, which I can then merge
# with the 2017 DataFrame:
# %%
combined_2007_2016 = pd.concat(reassigned_dfs, axis=0, sort=False) # concatenate all DataFrames in the list into one
combined_2007_2016.reset_index(inplace=True)
combined_2007_2016.drop(columns=["level_0", "level_1"], inplace=True)
combined_2007_2016.head()

# %% md
# I still have to append the dataset from 2017:
# %%
data = combined_2007_2016.append(reassigned_df_2017["Stadtteilprofile 2017"], sort=False)
data.head()

# %% md
# The DataFrame ```data``` now holds all instances from both of the district profile Excel files.
# I will pickle the dataset to have a backup and to be able to skip the cells above in the future:
# %%
data.to_pickle("../data/district_profiles_2007_2017.pkl")

# %% md
#### Cleaning the dataset
# If the cells above have been skipped, the data can be read from the pickle file at this point.
# Let's take a quick look at the columns of the combined dataset:
# %%
data = pd.read_pickle("../data/district_profiles_2007_2017.pkl") # read the stored dataset
data.info()
data.describe()

# %% md
# Some rows appear to hold averages across some or all districts. It makes sense to exclude these for now,
# as this information can easily be recovered from the individual districts and would only skew results.
# In Hamburg, there are no districts or larger administrative units with more than 1,000,000 inhabitants,
# so any "districts" with those numbers must be aggregates. Here is a plot showing the current distribution:
# %%
sns.boxplot(x="year", y="population", data=data)

# %% md
# There are no districts or "Bezirke" with more than 1,000,000 inhabitants, these can only be city-wide aggregates.
# %%
data["district"].loc[data["population"] > 1000000]
# %% md
# There are also no districts with a population of more than 100,000 inhabitants, these can only be wards.
# %%
data["district"].loc[data["population"] > 100000]
# %% md
# I will exclude all of these aggregate values, since I will conduct my analysis on a district level. Furthermore,
# these aggregates should be easy to recover by averaging the district data.
# %%
districts = data[data.population < 100000]
# %% md
# The updated population distribution looks much more plausible now, with Rahlstedt as the outlier.
# It is the most populous district with more than 90,000 inhabitants, followed by Billstedt.
# %%
sns.relplot(x="year", y="population", data=districts)
districts[["year", "district", "population"]].loc[districts["population"] > 60000].tail(2) # the largest two districts


# %% md
# In the ground values dataset with which I will eventually merge this one,
# the districts St. Pauli and St. Georg are
# spelled with the "." after the "St". In order to prevent merge conflicts
# later, I will change all occurences of "St  Pauli" and "St  Georg" in this
# dataset to "St. Pauli" and "St. Georg".
# %%
districts.district.replace("St  Pauli", "St. Pauli", inplace=True)
districts.district.replace("St  Georg", "St. Georg", inplace=True)
districts.district.replace("Altenwerder und Moorburg", "Moorburg und Altenwerder", inplace=True) #switch these around

# %% md
# Some of the columns do not seem to have the right datatype set:
# %%
non_float64 = pd.DataFrame(districts.select_dtypes(exclude="number").dtypes).reset_index()
non_float64.columns = ["column", "dtype"]
non_float64

# %% md
# I will reassign the columns new datatypes that make more sense to me. Since I
# will have to perform this action quite often, I have packaged pandas' ```to_numeric```
# function in a function of my own:
# %%
def force_col_to_num(col, df=districts):
    """Convert a column col in dataframe df to numeric values"""
    df[col] = pd.to_numeric(df[col], errors="coerce")

# %% md
# Districts should be categorical values:
# %%
districts["district"] = districts["district"].astype("category")

# %% md
# Years can be cast down to integers to save space:
# %%
districts["year"] = districts["year"].astype(int)

# %% md
# The following columns have only been encoded as ```objects```
# because they contain the odd empty string. I will force convert
# these to float64:
# %%
force_col_to_num("unemp_15_25")
force_col_to_num("unemp_15_25_rel")
force_col_to_num("unemp_55_65")
force_col_to_num("unemp_55_65_rel")
force_col_to_num("unemp_sgb2")
force_col_to_num("rec_sgb2")
force_col_to_num("rec_sgb2_rel")
force_col_to_num("hholds_shared")
force_col_to_num("tax_revenue")

# %% md
# The cdu column (share of the vote for CDU party) contains some values that are part of strings.
# I need to extract them and convert to column to a numeric one:
# %%
districts["cdu"].unique()

def extract_nnd(num):
    """Extracts the first two digits followed by a point and another digit in a string"""
    result = re.findall('(\d\d.\d)', str(num))
    if not result:
        return float("NaN")
    return result[0]

# apply the function to the column
districts["cdu"] = districts.cdu.apply(extract_nnd)
districts["cdu"].unique() # seems to have worked!

force_col_to_num("cdu") # convert the column to numeric

# %% md
# The issue is repeated in the other columns that hold the share of the vote for the different parties.
# I will apply the same function to these columns as well:
# %%
districts["spd"] = districts.spd.apply(extract_nnd)
force_col_to_num("spd")

districts["greens"] = districts.greens.apply(extract_nnd)
force_col_to_num("greens")

districts["left"] = districts.left.apply(extract_nnd)
force_col_to_num("left")

# %% md
# The remaining columns seem not to contain any non-numeric values except for NaNs.
# I will force convert them to numeric data as well:
# %%
force_col_to_num("real_estate_price_mean")
force_col_to_num("house_price_mean")
force_col_to_num("condo_price_mean")
force_col_to_num("doctors_resident")
force_col_to_num("rec_sgb2_u15")
force_col_to_num("rec_sgb2_u15_rel")

# %% md
# Let's compare the old and the new datatypes:
# %%
non_float64["new dtype"] = [districts[col].dtype for col in non_float64["column"]]
non_float64

# %% md
# I think that this should conclude the cleaning of the most obvious flaws in the dataset.
# I will store dataset as a pickle file that I will use in my data analysis later:
# %%
districts.info()
districts.describe()
districts.to_pickle("../data/cleaned_district_profiles_2007_2017.pkl")
