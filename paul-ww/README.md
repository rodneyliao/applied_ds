# EM212: Applied Datascience

### Project Description
For this course, I will be analyzing district-level data obtained from [Statistik Nord](https://www.statistik-nord.de/), which provides access to public datasets. In particular, I am working with the so-called district profiles (Stadtteilprofile), which are published on a yearly basis. Apart from this dataset, I am also working with
additional data sourced from Hamburg's [Open Data Portal](http://suche.transparenz.hamburg.de/dataset/bodenrichtwerte-fur-hamburg6?forceWeb=true).

### Running the code / notebooks
My code is designed to be run in a specific order. All cleaned datasets will be saved in the data folder, which is already pre-populated. Try following these steps when executing the notebooks if you encounter any problems:
1.   Run the [Ground Values notebook](https://github.com/paul-ww/applied-datascience/blob/master/notebooks/values.ipynb). Downloading the entire dataset could take a long time, so you might want to leave this notebook running in the background. Alternatively, I have uploaded a [compressed version](https://github.com/paul-ww/applied-datascience/blob/master/data/joined_ground_values.pkl.zip) of the cleaned dataset that can be used.
2.   Run the [District Profiles notebook](https://github.com/paul-ww/applied-datascience/blob/master/notebooks/profiles.ipynb).
3.   Run the [Spatial Visualization notebook](https://github.com/paul-ww/applied-datascience/blob/master/notebooks/spatial.ipynb). This will prepare the shapefiles for use in the last notebook.
4.   Run the [Data Analysis notebook](https://github.com/paul-ww/applied-datascience/blob/master/notebooks/analysis.ipynb). This notebook will rely on the datasets prepared by all of the notebooks above and thus needs to be run as the last step.

### Datasets
###### District Profiles
I use two datasets which I downloaded from [Statistik Nord](https://www.statistik-nord.de/):
- [Stadtteilprofile Berichtsjahre 2007-2016](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/Stadtteilprofile-Berichtsjahre-2007-2016.xlsx)
- [Stadtteilprofile Berichtsjahr 2017](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/StadtteilprofileBerichtsjahr2017.xlsx)

###### Ground Values
The ground value data can be downloaded from [here](http://suche.transparenz.hamburg.de/dataset/bodenrichtwerte-fur-hamburg6?forceWeb=true). A [list of direct links to the csv files](https://github.com/paul-ww/applied-datascience/blob/master/code/urls.txt) is available in the ```code```
directory.

### Data License
###### District Profiles
"Für Online-Veröffentlichungen, Online-Datenbanken, interaktive Atlanten, Jahrbücher, Themenbände, Statistische Berichte, Stadtteil- und Kreisprofile sowie kundenspezifische Aufbereitungen ist die auszugsweise Vervielfältigung und Verbreitung mit Quellenangabe gestattet." [Source](https://www.statistik-nord.de/agb/)

###### Ground Values
[Datenlizenz Deutschland - Namensnennung - Version 2.0](https://www.govdata.de/dl-de/by-2-0)
