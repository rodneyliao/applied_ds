# %% md
## Analysis of District Profile and Ground Value data
# In this notebook, I will analyse the two datasets that I have cleaned in the
# notebooks ```notebook-district-profiles``` and ```notebook-ground-values```.
# %%
# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import math

# %% md
### Importing and merging the data
# But first, I have to read and merge the two sets.
# I will first have to import the cleaned datasets. The district profiles dataset
# looks like this:
# %%
profiles = pd.read_pickle("../data/cleaned_district_profiles_2007_2017.pkl")
profiles.head(5)

# %% md
# And the ground values dataset looks like this:
# %%
ground_values = pd.read_pickle("../data/collapsed_ground_values.pkl")
ground_values.head(5)

# %% md
# It seems like there are some districts that are not being matched:
# In the profiles dataset, some districts are listed combined, whereas they
# are listed individually in the ground values dataset. One example is "Finkenwerder",
# which occurs on its own in the ground values set and is listed as "Waltershof
# und Finkenwerder" in the district profiles dataset. In order to merge these
# instances into the district profiles, I will use the individual districts found in
# the ground values data to
# calculate means for each pair of district / year observations. For example,
# I will use the data for districts "Finkenwerder" and "Waltershof" to compute their
# average as "Waltershof und Finkenwerder", which I can then merge with the profiles
# dataset. These are the pair means I need to compute:
# %%
check_districts = profiles.merge(   ground_values,
                                    on=["district", "year"],
                                    indicator=True,
                                    how="outer")
unmatched = check_districts[["district", "year", "_merge"]][check_districts["district"].str.contains("und")]
means_needed = {item.split(" und ")[0]:item.split(" und ")[1] for item in unmatched["district"][:-1]}
means_needed

# %% md
# The next step is actually calculating these means:
# %%
dict = {}
for key, value in means_needed.items():
    dict[key + " und " + value] = ground_values.loc[[key,value]].groupby("year").mean()
interpolated = pd.concat(dict)
interpolated.index.rename(["district", "year"], inplace=True)
interpolated.head()

# %% md
# Next, I need to append these new instances to the existing ground value dataset:
# %%
ground_values = interpolated.append(ground_values)
ground_values.info()

# %% md
# Now that the ground values dataset includes the missing instances, I have to merge
# the two sets once more. This time, a left merge will be sufficient, as I only want
# to keep ground values for those districts for which profile data are available. The final
# DataFrame will have the name ```dd``` (District Dataset):
# %%
dd = profiles.merge(ground_values,
                    on=["district", "year"],
                    how="left") # merge once more, this time as a left join

dd.set_index(["district", "year"], inplace=True)
dd.sort_values(["district", "year"], ascending=[True, True], inplace=True)
dd.head()


# %% md
# With the data cleaning and merging complete, I will save a copy of the dataset:
# %%
dd.to_pickle("../data/final_dataset.pkl")


# %% md
### Exploratory Data Analysis
# My eventual goal is to find out if and which sociodemographic features found in
# the district profiles dataset might be used to predict the mean or median estimated
# ground value of a district.
# %%
dd = pd.read_pickle("../data/final_dataset.pkl")

# %% md
##### Missing values
# But first, I will try to check the data for flaws that might still exist in the data
# after my initial cleaning. One such example are missing values.
# Since not all of the features have been observed in every year, there are many columns with a high share of
# missing values. These are the columns with a share of missing values that is $\ge 50%$
# %%
missing = dd.isnull().sum()/len(dd) # calculate share of missing values
missing.sort_values(ascending=False, inplace=True)
missing = missing.reset_index()
missing.columns = ["feature", "share_missing"]
fig = sns.barplot(x="feature", y="share_missing", data=missing.loc[missing.share_missing >= 0.5])
plt.xticks(rotation=90)
fig.set_title("Missing Values")
fig.set_ylabel("Share of missing values")
fig.set_xlabel("Feature")

# %% md
# Although there are some columns that have a high share of missing data, I will try to
# keep them around for now. At this point, I am not sure if I can confidently drop any of
# these columns.


# %% md
##### Correlation with the ground value
# Since my main goal is predicting the ground value, I would like to see which district features are correlated with the ground value.
# To do this, I will calculate both the Pearson and Spearman correlation coefficients pairwise across
# my dataframe:
# %%
pearson = dd.corr()
spearman = dd.corr("spearman")
corrs_w_GV = pd.DataFrame(pearson["GV_mean"]) # correlations with mean ground value
corrs_w_GV["spearman"] = spearman["GV_mean"]
corrs_w_GV.columns = ["pearson", "spearman"]
corrs_w_GV.sort_values(by="pearson", ascending=False).head()


# %% md
# In order to be able to better compare the correlation results, I will plot both the Pearson
# and Spearman coefficients in the same barplot using this function:
# %%
exclusion_list = ["GV_mean", "GV_median", "GV_std", "GV_count"] # exclude the descriptive stats

def show_strongest_corr(type, negative, exclude=exclusion_list, n=10, target="Ground Value", corr_df=corrs_w_GV):
    """Returns a barplot of the strongest correlations with the target variable"""
    strongest = corr_df.drop(labels=exclude).sort_values(by=type, ascending=negative).head(n)
    melted = strongest.reset_index().melt("index", var_name="corr_type", value_name="corr_coef")
    result = sns.barplot(x="index", y="corr_coef", hue="corr_type", data=melted)
    plt.xticks(rotation=90)
    result.set_ylabel("Correlation Coefficient" + "\n" + "ordered by " + type[0])
    result.set_xlabel("Variable")
    result.set_title("Strongest Correlations with " + target)


# %% md
# These are the variables that have the strongest positive Pearson correlation with the mean ground value:
# %%
show_strongest_corr(type=["pearson", "spearman"], negative=False, n=10)


# %% md
# And these the strongest positive Spearman correlations with the ground value:
# %%
show_strongest_corr(type=["spearman", "pearson"], negative=False, n=10)


# %% md
# These are the strongest negative Pearson correlations with the mean ground value:
# %%
show_strongest_corr(type=["pearson", "spearman"], negative=True, n=10)


# %% md
# And these the strongest negative Spearman correlations with the ground value:
# %%
show_strongest_corr(type=["spearman", "pearson"], negative=True, n=10)

# %% md
# The variables with the strongest positive overall correlation with the ground value are the following:
# %%
sp_pearson = corrs_w_GV.drop(labels=exclusion_list).sort_values(by=["pearson", "spearman"], ascending=False).head(15).reset_index()
sp_spearman = corrs_w_GV.drop(labels=exclusion_list).sort_values(by=["spearman", "pearson"], ascending=False).head(15).reset_index()
sp = sp_pearson.merge(sp_spearman, on="index", how="inner")
sp.iloc[:, 0:3]

# %% md
# These variables have the strongest negative overall correlation with the ground value:
# %%
sn_pearson = corrs_w_GV.drop(labels=exclusion_list).sort_values(by=["pearson", "spearman"]).head(15).reset_index()
sn_spearman = corrs_w_GV.drop(labels=exclusion_list).sort_values(by=["spearman", "pearson"]).head(15).reset_index()
sn = sn_pearson.merge(sn_spearman, on="index", how="inner")
sn.iloc[:, 0:3]


# %% md
##### Cross-Correlations of the potentially influential variables
# Since the variables might not only be correlated with the ground value, but also
# with one another, it makes sense to use pairplots to visualize these relationships.
# Among the variables with a positive correlation with the ground value, a few relationships
# are clearly visible:
# *   the general mean real estate price is correlated with the mean house price (by design of the feature)
# *   it is also correlated with the mean condo price
# *   it could also be that the share of single households in a ditrict is correlated with the mean real estate price
# %%
# the relationship between the five strongest positive correlations with the ground value
sns.pairplot(   data=dd,
                vars=sp["index"].head(5))
# %% md
# Among the variables with a negative correlation with the ground value, it looks like
# *   the mean size of a household is strongly correlated with the share of children in the household,
# which makes intuitive sense
# *   household size is also correlated with the share of people under 18 in a district, which also seems plausible:
# %%
# the relationship between the five strongest negative correlations with the ground value
sns.pairplot(   data=dd,
                vars=sn["index"].head(5))


# %% md
##### Real Estate Price and Estimated Ground Value
# Let's turn back to the variables with a potential influence on the ground value. Although
# I have already computed the correlation coefficients, it can be beneficial to also
# examine the actual joint distribution. Here is an example for the most obvious positive correlation
# with the ground value, the mean real estate price. I am expecting a positive correlation because
# the ground value is supposed to estimate the mean sale price of a property. Both distributions
# are very similar in their long tail of high values / property prices:
# %%
fig = sns.jointplot(  x="real_estate_price_mean",
                y="GV_mean",
                data=dd.reset_index() )
fig.set_axis_labels("Mean Real Estate Price", "Mean Ground Value")

# %% md
# This relationship seems to be stable over time as well:
# %%
sns.scatterplot(x="real_estate_price_mean", y="GV_mean", data=dd.reset_index(), hue="year")


# %% md
# Let's take another look, broken down by year. In the years 2007 and 2009, the ground
# values were not estimated by the city:
# %%
g = sns.FacetGrid(dd.reset_index(), col="year")
g = g.map(plt.scatter, "real_estate_price_mean", "GV_mean", edgecolor="w")
g.set_xlabels("Mean Real Estate Price")
g.set_ylabels("Mean Ground Value")

# %% md
# All in all, there seems to be a consistently strong relationship between the two
# variables, making the ground value a good predictor of the actual real estate price.
# It thus fulfills its main objective:
# %%
sns.regplot(    x="real_estate_price_mean",
                y="GV_mean",
                data=dd)


# %% md
##### Distribution of the ground values: mean and median
# Since I am trying to predict the ground value (and indirectly also the real estate
# price) on a district level, it makes sense to analyse this variable's distribution.
# Let's start with an overview over the ground values across the most recent years:
# %%
sns.boxplot(x="year", y="GV_mean", data=dd.reset_index())


# %% md
# It looks like the data from 2008 are distributed very differently from the data
# for the years from 2010 onwards, with outliers that reduce the readability of
# the other distributions. To get a better look, here is the data excluding the year
# 2008:
# %%
sns.boxplot(x="year", y="GV_mean", data=dd.reset_index().loc[dd.reset_index().year >= 2010])


# %% md
# It seems like the majority of the districts has a relatively stable ground value,
# while the outlier districts keep getting ever more expensive. To support this argument,
# I need to look at the median ground values as well. Again, the 2008 distribution appears to
# be very different from the ones found in the later years:
# %%
sns.boxplot(x="year", y="GV_median", data=dd.reset_index())


# %% md
# Again, I plot the distribution for the more recent years excluding 2008.
# Here, too, it seems like the most drastic price increases are found among the
# outliers of the distribution:
# %%
sns.boxplot(    x="year",
                y="GV_median",
                data=dd.reset_index().loc[dd.reset_index().year >= 2010])


# %% md
# The general trend actually seems to be mostly flat:
# %%
g = sns.regplot(    x="year",
                    y="GV_median",
                    data=dd.reset_index().loc[dd.reset_index().year >= 2010],
                    robust=True )
g.set_xlabel("Year")
g.set_ylabel("Median Ground Value")
g.set_title("Linear Model of Median Ground Value and Year, robust")


# %% md
# The same seems to be true for the mean:
# %%
g = sns.regplot(    x="year",
                    y="GV_mean",
                    data=dd.reset_index().loc[dd.reset_index().year >= 2010],
                    robust=True )
g.set_xlabel("Year")
g.set_ylabel("Median Ground Value")
g.set_title("Linear Model of Mean Ground Value and Year, robust")


# %% md
# To sum up the current findings: while the majority of the districts of Hamburg
# generally does not see large increases in the ground value, the outliers seem
# be become more and more expensive. In order to further dive into this issue,
# I will have a look at the average increase in the ground value and identify those
# districts which experience exceptionally large increases. Since I have a gap in
# my ground values between 2008 and 2010, I will only look at the years 2011 and up.
# I decided to include the ```GV_count``` column, as it tells me how the size of
# the ground value dataset changed year on year.
# %%
gv = dd[["GV_mean", "GV_median", "GV_count"]].sort_values(  ["district", "year"],\
                                                            ascending=[True, True])\
                                             .groupby(["district"])
abs_change = gv.diff()
rel_change = gv.pct_change()
abs_change.columns = list(map(lambda name: name + "_abs", abs_change.columns))
rel_change.columns = list(map(lambda name: name + "_rel", rel_change.columns))
changes = abs_change.join(rel_change)
changes = changes.reset_index()\
                 .loc[changes.reset_index().year >= 2011]\
                 .set_index(["district", "year"])
changes.head()


# %% md
# In order to identify the districts with above-average increases in ground value,
# I first have to compute the general average. In the ```year``` column, the values
# refer to the period ending with the year displayed. For example, 2011 means the
# change in the ground value from 2010 to 2011:
# %%
changes.groupby("year").mean()


# %% md
# With the exception of 2013 and 2016, the general trend in the average change in the mean
# ground value is at around 5%. The median seems to keep up in 2010-11 and 2011-12, but lags
# behind the mean in 2013-14 and 2014-15. In 2013, the number of instances used to compute the
# median ground value dropped by 8%, which could explain the drop in the median and average
# ground value if there is data missing for some of the more expensive districts. Similarly,
# it could be the case that more expensive districts where added among the 2% increase in data points
# that happened in 2015-16. An increase in the median ground value of around 90% still seems very peculiar
# to me, though, as it is a robust measure that should not be affected this much when the number of
# instances grows by only 2%. I suspect a flaw in the data, that I will investigate further.
# %%
g = sns.lineplot(   data=changes.groupby("year").mean()[["GV_mean_rel", "GV_median_rel", "GV_count_rel"]],
                    style="event",
                    markers=True)
g.set_xlabel("Year")
g.set_ylabel("Relative Change")
g.legend(["Mean Ground Value", "Median Ground Value", "# of data points"])
g.set_title("Relative y-o-y change in mean and median ground value")


# %% md
# My goal is to find out which district out- or underperfomed their counterparts
# over the course of my observation period. In order to do this, I have to
# calculate the difference between the average change in the median ground value
# across all districts and the change in the median ground value inside a particularl
# district. Then, I count the number of years in which this difference was positive
# (for the outperformers) or the number of years in which this difference was negative
# (in the case of the underperformers). I am again using the median as my measure of
# centrality, because some of the changes are much too large to be plausible and I
# do not want these values to skew my overall trends:
# %%
cm = changes.join(changes.groupby("year").median(), rsuffix="_avg_change")
cm = cm[["GV_mean_rel", "GV_median_rel", "GV_mean_rel_avg_change", "GV_median_rel_avg_change"]]
cm["diff_from_mean"] = cm["GV_mean_rel"] - cm["GV_mean_rel_avg_change"]
cm["diff_from_median"] = cm["GV_median_rel"] - cm["GV_median_rel_avg_change"]
no_of_periods = len(cm.index.levels[-1]) # keep track of the total number of periods
cm.head()


# %% md
# These are the district/year combinations with the largest positive difference between
# the median change in the median ground value. These values signify the cases
# where a district outperformed the median change in median ground value:
# %%
cm.sort_values(by="diff_from_median", ascending=False)["diff_from_median"].head(15) # greatest outperformers in terms of change in median


# %% md
# These are the district/year combinations with the largest negative difference between
# the median change in the median ground value. These values signify the cases
# where a district underperformed the median change in median ground value:
# %%
cm.sort_values(by="diff_from_median", ascending=True)["diff_from_median"].head(15) # greatest underperformers in terms of change in median


# %% md
# In order to better visualize these resuls and find potential spatial clusters,
# I would like to show my results overlayed onto a map of the city. For this,
# I will use the shapefiles I have cleaned in the ```spatial``` notebook. I will
# use Geopandas to import the shapefiles and append my data to the GeoDataFrame, which
# I can then plot:
# %%
import geopandas
geodata = pd.read_pickle("../data/geodata.pkl")
cm["median_performance"] = np.where(cm["diff_from_median"] > 0, 1, -1) # 1 if outperformed, -1 if underperformed
perf = cm.groupby("district")["median_performance"].sum().sort_values(ascending=False)
perf = pd.DataFrame(perf)
perf["share_periods"] = perf["median_performance"] / no_of_periods
perf_geo = geodata.merge(perf, on="district", how="right") # merge shapefiles in
perf_geo.head()


# %% md
# The following plot summarizes my results: the districts are coloured according
# to a scale between -1 and 1. A value of 1 would mean that the district's change
# in median ground value exceeded (and thus outperformed) the median of the change
# in median ground value calculated across all districts *in every single one of the 7
# periods*. A value of -1 would mean that the district underperformed the median in
# *in all of the 7 periods the differences were calculated for*. The seven periods
# are the differences from 2010-11, 2011-12 and so on.
# Based on this map, I can draw a few conclusions:
# *   the district which is most constently outperforming its peers is "Sternschanze",
# which has been heavily gentrifying over the course of the last ten years and is still a very
# attractive location
# *   the districts in the South of the city have all experienced underperformant growth,
# which could be due to the many industrial areas south of the river Elbe.
# * in general, centrality seems to be a driving factor in determining the ground value performance
# of a district, although there are outliers such as the district in the Northeast
# %%
g = perf_geo.plot(  column="share_periods",
                    legend=True,
                    figsize=(20, 10))
g.set_title("Share of years of over/underperformance" + "\n" + "in terms of change in median" + "\n" + "ground value, 2010 to 2017")
