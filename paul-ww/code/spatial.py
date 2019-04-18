# %% md
#### Spatial Visualization
# Since I am dealing with geographic instances (districts of Hamburg),
# it would be neat to be able to visualize my findings on a map of the city.
# In order to do this, I need to import Geopandas, which is meant to extend
# pandas' capabilities to geo-data. The shapefiles that I'm using can be
# downloaded from [here](https://opendata.arcgis.com/datasets/8437e52c5e2d4963b6098accf571a891_0.zip)
# and the data is described [here](https://opendata-esri-de.opendata.arcgis.com/datasets/8437e52c5e2d4963b6098accf571a891_0)
# %%
import geopandas as gpd
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# %% md
# I first have to import the cleaned final dataset:
# %%
dd = pd.read_pickle("../data/final_dataset.pkl")

# %% md
# Next, I also need to import the shapefiles into a Geopandas DataFrame. This
# is the map of Hamburg that I would like to use for my project:
# %%
gdf = gpd.read_file("../data/shapefiles/Stadtteile__Hamburg.shp") # import shapefiles
gdf.columns = ["OBJECTID", "district", "ward", "Shape__Are", "Shape__Len", "Shape__A_1", "Shape__L_1", "geometry"]
gdf.crs # extracts the projection used
gdf.loc[gdf.district != "Neuwerk"].plot(figsize=(15, 15)) # plot excludes exclave Neuwerk to show maps as large as possible


# %% md
# There seem to be some wrongly encoded Umlauts in the shapefile, I will manually fix the
# encoding:
# %%
changes = { "Allermà§¼he":"Allermöhe",
            "Eimsbbttel":"Eimsbüttel",
            "Eimendorf":"Eißendorf",
            "Barmbek-Sod":"Barmbek-Süd",
            "Fuhlsbgttel":"Fuhlsbüttel",
            "Grob Borstel":"Groß Borstel",
            "Grob Flottbek":"Groß Flottbek",
            "HummelsbMttel":"Hummelsbüttel",
            "Neuallerm":"Neuallermöhe",
            "Lohbrbgge":"Lohbrügge",
            "Poppenbnttel":"Poppenbüttel",
            "Rlnneburg":"Rönneburg",
            "Sllldorf":"Sülldorf",
            "St.Pauli":"St. Pauli",
            "St.Georg":"St. Georg",
            "Wellingsbittel":"Wellingsbüttel",
            }


for key in changes:
    gdf["district"].replace(key, changes[key], inplace=True)


# %% md
# Merge individual districts present in the shapefile so that aggregates from
# the profiles can be represented. The pairs of aggregated districts have
# can be extracted by comparing the district names in the final dataset and
# those found in the shapefile:
# %%
check_districts = gdf.merge(        dd,
                                    on="district",
                                    indicator=True,
                                    how="outer")
unmatched = check_districts[check_districts["district"].str.contains("und")]
means_needed = {item.split(" und ")[0]:item.split(" und ")[1] for item in unmatched["district"][:-1]}
means_needed

# %% md
# I will [dissolve](http://geopandas.org/aggregation_with_dissolve.html) the corresponding districts. In order to do this, I need to create a new
# column holding the name of the new aggregated districts. Geopandas will then merge the
# polygons included in these merge names into a new, aggregated polygon encompassing both
# districts:
# %%
gdf["merge_name"] = ""
for key in means_needed:
    district_1 = key
    district_2 = means_needed[key]
    new_name = district_1 + " und " + district_2
    gdf["merge_name"].where(gdf.district != district_1, new_name, inplace=True)
    gdf["merge_name"].where(gdf.district != district_2, new_name, inplace=True)

dissolved = gdf.dissolve(by="merge_name")
dissolved.drop(index="", inplace=True)
dissolved = dissolved.reset_index()[["merge_name", "geometry", "OBJECTID"]]
dissolved.columns = ["district", "geometry", "OBJECTID"]
gdf = gdf.append(dissolved, sort=False)
gdf.OBJECTID = range(1, len(gdf) + 1)
gdf = gdf[["district", "geometry", "OBJECTID"]]
gdf.reset_index(drop=True, inplace=True)
gdf[gdf["district"].str.contains("und")].head()


# %% md
# The geodataframe now includes the aggregated districts found in the district profiles.
# Because of this, the generated map has slightly changed:
# %%
gdf.loc[gdf.district != "Neuwerk"].plot(figsize=(15, 15)) # plot excludes exclave Neuwerk to show maps as large as possible


# %% md
# I will save the cleaned dataset for now:
# %%
gdf.to_pickle("../data/geodata.pkl")


# %% md
# In order to be able to plot any feature of my main dataset, I need to merge it
# into the GeoDataFrame:
# %%
dd_geo = gdf.merge(     dd.reset_index(),
                        on="district",
                        how="right") # keep only those tiles that are contained in the district profiles
dd_geo.set_index(["district", "year"])


# %% md
# In order to make mapping a specific variable easier, I have created function that
# has many options already preset. It allows me to map a column simply by calling its
# name and the corresponding year, if applicable
# %%
def map_data(col, year, suffix="", colmap="Dark2", year_col="year", df=dd_geo, size=(16, 8)):
    '''Plots a column for a specified year (if applicable)'''
    # figure settings
    fig, ax = plt.subplots(1, figsize=size)
    ax.axis("off") # disable axes
    ax.set_title(   col, # set title
                    fontdict={"fontsize":"25", "fontweight":"3"})

    # function logic
    cols = [col]
    cols.append("geometry")
    params = {  "column":col, # column(s) to use
                "legend":True, # print legend
                "linewidth":0.8, # thickness of the boundaries
                "edgecolor":"0.8", # color of the edges
                "ax":ax, # define axes
                "vmin":0,
                "vmax":15,
                #"cmap":"Blues", # colormap
                }
    if not bool(year): # if year is not required (e.g. historical data, use year=False)
        df[cols].dropna().plot(**params)
    else:
        df[cols].loc[df[year_col] == year].dropna().plot(**params)

    if suffix != "":
        ax.annotate(suffix,
            xy=(0.1, .15), xycoords="figure fraction",
            horizontalalignment="left", verticalalignment="top",
            fontsize=20)
        fig.savefig("map_" + col + "_" + str(suffix) + ".png", dpi=300) # export figure to file


# %% md
# Here is some example usage:
# %%
map_data("unemp_rel", 2016)
map_data("GV_median", 2017)


# %% md
# This cell will save multiple figures which can easily be turned into GIF:
# %%
for year in range(2010, 2018):
    map_data("BRW_median", year, suffix=year)

# %% md
# With the exported images, I used [this tutorial](https://towardsdatascience.com/how-to-make-a-gif-map-using-python-geopandas-and-matplotlib-cd8827cefbc8) to merge them together into a GIF
