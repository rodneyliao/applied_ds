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
from sklearn.cluster import KMeans
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
#### Real Estate Price and Estimated Ground Value
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
#### Correlations with the ground value
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
#### Linear Regression: Predicting the median ground value
# Let's turn back to the variables with a potential influence on the ground value.
# In order to build the best model explaining the median ground value,
# I will construct a linear regression based on the correlations discussed before.
# Recursive Feature Elimination can help with selecting the most influential
# features. I rely on the appropriate scikit-learn libraries to do this.

# %% md
# First, I have to eliminate rows containing missing values, however. For the logistic
# regression, I will try to include as many variables as possible while. This
# is only possible at the cost of dropping instances: The more variables I include,
# the higher the chance of a missing value in one instance. I will therefore settle
# for all those features with a share of missing features below 33%:
# %%
model_data = dd[missing.loc[missing.share_missing < 0.33].feature].dropna()
model_data.reset_index(inplace=True) # include year as a variable
model_data.drop(columns="district", inplace=True) # drop non-numerical district name

y = ["GV_median"] # store labels
X = [col for col in model_data.columns if col not in ["GV_median", "GV_mean", "GV_std"]] # store features
model_data[X].info()

# %% md
# This step leaves me with more than 500 instances and 57 variables that could be relevant for predicting the
# median ground value. To find the most important ones, I will run a RFE with the
# goal of reducing the number of independent variables in my model to 15:
# %%
from sklearn.feature_selection import RFE
from sklearn import linear_model

linear = linear_model.LinearRegression()
lin_rfe = RFE(linear, 15) # keep the 15 most important features
lin_rfe = lin_rfe.fit(model_data[X], model_data[y].values.ravel())

reduced_feats = [model_data[X].columns[i] for i in range(len(X)) if lin_rfe.support_[i]]
reduced_feats # reduced set of relevant features

# %% md
# Now it is time to run the actual regression and interpret the results:
# %%
smf.ols(    "GV_median ~ " + " + ".join(reduced_feats),
            data = model_data).fit().summary()

# %% md
# It looks like the median ground value is statistically significantly ($\alpha=0.01$) associated with
# *   the number of students not enrolled in high schools with an academic focus (```students-not-gym```),
#     which seems plausible given that parental income is still a predictor for attendance
#     of these schools. Cheaper neighbourhoods might not send that many children to these
#     schools or might not contain such institutions.
# *   the share of residents aged 64 or above (```o64_rel```). This seems counterintuitive,
#     I would have expected these areas to be associated with a higher ground value.
# *   the share of residents that are not German citizens (```for_rel```). This seems plausible, as
#     many of these tend to be refugees who in many cases are not permitted to work
#     and thus tend to live in cheaper neighbourhoods
# *   the number of pharmacies in a district (```pharmacies```). I would have expected
#     the opposite, as the expensive inner city center tends to house more pharmacies
#     than the districts on the outskirts. However, some districts in the periphery
#     are also very expensive, which could support this finding.


# %% md
#### Distribution of the ground values: mean and median
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
#### Identifying the most performant districts
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
# the median change in the median ground value and the overall change in median ground
# value. These values signify the cases where a district outperformed the median change
# in median ground value:
# %%
cm.sort_values(by="diff_from_median", ascending=False)["diff_from_median"].head(15) # greatest outperformers in terms of change in median

# %% md
# The first three instances seem implausible and are likely due to very small sample
# sizes and / or large changes in instance count year to year.

# %% md
# These are the district/year combinations with the largest negative difference between
# the median change in the median ground value and the overall change in median ground
# value. These values signify the cases where a district underperformed the median change
# in median ground value:
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

# %% md
#### K-Means-Clustering
# It might be worthwhile to search for clusters among district features. My idea
# was that be plotting the identified clusters on the map, I could be able to
# discern spatial patterns of similarities. I therefore made use of scikit-learns
# ```k-means-clustering``` function.
# %%
features = dd[missing.loc[missing.share_missing < 0.15].feature].dropna().reset_index()
features = features.loc[features.year == 2017].set_index("district")
kmeans = KMeans(n_clusters=3, random_state=0).fit(features)
centers = features
centers["labels"] = kmeans.labels_
centers
clusters_geo = geodata.merge(centers, on="district", how="right") # merge shapefiles in
clusters_geo.plot(column="labels", cmap="tab20")

# %% md
# Without additional information about my clusters, I am not able to see a clear
# pattern here. One interesting aspect is the distribution of the brown and the dark
# blue regions: with a few exceptions, the dark blue regions are in the northern
# half of the city, while the brown areas are located more in the southern parts.
# They are actually pretty well divided by the river runnin through the city, which
# historically separates the populous areas on the northern bank from the industrial
# areas on the soutern bank. Without more information, this is just guesswork, however.


# %% md
#### Logistic Regression to predict outperformance based on demographic features
# My goal is to extract those variables that best explain a district's outperformance
# in comparison to the average change across all districts. To do this, I will
# run a logistic regression on the dependent variable dummy "outperformance", which
# will be marked 1 if the district's change in median ground value exceeded
# the median change in ground value that occured in all districts:
# %%
cm["outperformed"] = np.where(cm["diff_from_median"] > 0, 1, 0) # 1 if outperformed, 0 if not outperformed

# %% md
# Since the ground value estimate is published at the end of a year, it should
# capture the changes that occured within that year. Since I rely on the difference
# between the ground value of the last and the current year, I need to shift the
# dummy information back by one year. A row with the index 2010 now means that
# the district outperformed other districts in the period of January to December 2010,
# which is the same timeframe that the demographic features correspond to. Without
# shifting the dummy, the outperformance would be accredited to the year 2011 instead.
# %%
unstacked = cm.unstack("district")
unstacked.index = unstacked.index - 1
restacked = unstacked.stack().swaplevel().sort_values(["district", "year"])
restacked.head()


# %% md
# Let's merge the shifted data into the main dataframe. For my logistic regression,
# the dependent variable will be ```outperformed```. Since the model only works
# in the absence of missing data, I will first reduce the main dataframe to those
# columns which have a share of missing values below 5%, of which I then drop
# those rows where data is missing:
# %%
no_missing = dd[missing.loc[missing.share_missing < 0.05].feature].dropna()


# %% md
# Next, I need to merge my features and labels into one dataset. This leaves me with
# 608 district/year combinations to work with:
# %%
ddc = no_missing.merge(restacked, how="inner", left_index=True, right_index=True) # merge the changes into the main dataframe
ddc.dropna(inplace=True)

# %% md
# For the actual regression task, I will rely on the libraries provided by scikit-learn:
# %%
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

y=["outperformed"] # store labels
X=[col for col in ddc.columns[:-8]]

lr = LogisticRegression()
rfe = RFE(lr, 15) # keep the 15 most important features
rfe = rfe.fit(ddc[X], ddc[y].values.ravel())
reduced_feats = [ddc.columns[i] for i in range(len(ddc.columns[:-8])) if rfe.support_[i]]
reduced_feats # reduced set of relevant features

# %% md
# Now that I have identified the 15 most relevant features, tt is time to
# have a look at the regression results:
# %%
import statsmodels.api as sm

ddc_y = ddc[y]
ddc_X = ddc[reduced_feats]

logit_model=sm.Logit(ddc_y,ddc_X)
result=logit_model.fit()
result.summary2()

# %% md
# It seems like only one feature has a statistically significant impact on the
# likelihood of outperformance. This variable is the number of homes completed
# in a certain district in a certain year, which could have the potential to
# drive down real estate prices in the long run.

# %% md
# In order to test if my model actually has any predictive power, I will split
# my data into a training and a test set and check its accuracy across both.
# A lot of this is again handled by scikit-learn libraries:
# %%
from sklearn.model_selection import train_test_split
from sklearn import metrics

X_train, X_test, y_train, y_test = train_test_split(ddc_X, ddc_y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print("Accuracy of logistic regression classifier on test set: {:.2f}".format(logreg.score(X_test, y_test)))

# %% md
# An accuracy of 0.63 is only a little above the 50% random guessing would achieve.
# Let's have a look at the confusion matrix:
# %%
from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
confusion_matrix

# %% md
# It looks like there were 82 true positives and 33 false negatives and thus 115
# correct predictions as well as 21 + 47 false predictions. Let's also have a look
# at the classification report:
# %%
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

# %% md
# Again, the accuracy is not much better than with random guessing. This is also
# clear when considering the ROC curve:
# %%
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label="Logistic Regression (area = %0.2f)" % logit_roc_auc)
plt.plot([0, 1], [0, 1],"r--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.show()

# %% md
# All in all, I can conclude that my model is not sufficient to predict whether
# a certain district will outperform the city-wide average change in median ground
# value based solely on the limited number of demographic features available to me.
# Features such as centrality, quality of life in terms of amenities such as public
# transport, number of parks and green spaces or shopping opportunities are not
# represented in my data. Another important aspect might be instances of autocorrelation,
# for example if a district with a history of outperformance might be likelier
# to outperform in the current period as well.
# All of these aspects could be analyzed as more data is added to the open data
# portal, leaving a lot of room for interesting research opportunities.

# %% md
#### Conclusion
# Across my four notebooks, I have imported, cleaned, analyzed and visualized
# demographic and real estate data. I was able to find
# 1.   that the ground values published by the city are quite good estimates
#      of the actual prices paid in real estate transactions
# 2.   that the general trend in ground value is much flatter than it seems
#      at first glance, while the perceived increase is mostly driven by
#      outliers
# 3.   a few demographic features which were associated with the median ground value
#      in a statistically significant way
# 4.   that without deep insights into the subject, it can be very difficult to
#      properly interpret clustering results
# 5.   that given all the features provided by the district profiles dataset,
#      an accurate prediction of outperformance was still not achievable.
#
# Nevertheless, I really enjoyed working on this project and think that I was
# able to learn quite a lot in the process.
