# EM212: Applied Datascience

### Introduction

For a detailed introduction to my project, have a look at the [directory containing my introduction and datasheet files](intro_datasheet).

### Project Description
For this course, I will be analyzing district-level data obtained from [Statistik Nord](https://www.statistik-nord.de/), which provides access to public datasets. In particular, I am working with the so-called district profiles (Stadtteilprofile), which are published on a yearly basis. Apart from this dataset, I am also working with
additional data sourced from Hamburg's [Open Data Portal](http://suche.transparenz.hamburg.de/dataset/bodenrichtwerte-fur-hamburg6?forceWeb=true).

### Running the code / notebooks
My code is designed to be run in a specific order. All cleaned datasets will be saved in the data folder, which is already pre-populated. Try following these steps when executing the notebooks if you encounter any problems:
1.   Run the [Ground Values notebook](notebooks/values.ipynb). Downloading the entire dataset from the original source can take a long time, I am using a link to a [compressed version of the CSV files](https://tufts.box.com/shared/static/r9v656dng1b0ncl3vhyc9mgph884aqk5.zip) that I uploaded to Box.
2.   Run the [District Profiles notebook](notebooks/profiles.ipynb).
3.   Run the [Spatial Visualization notebook](notebooks/spatial.ipynb). This will prepare the shapefiles for use in the last notebook.
4.   Run the [Data Analysis notebook](notebooks/analysis.ipynb). This notebook will rely on the datasets prepared by all of the notebooks above and thus needs to be run as the last step.

### Datasets
###### District Profiles
I use two datasets which I downloaded from [Statistik Nord](https://www.statistik-nord.de/):
- [Stadtteilprofile Berichtsjahre 2007-2016](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/Stadtteilprofile-Berichtsjahre-2007-2016.xlsx)
- [Stadtteilprofile Berichtsjahr 2017](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/StadtteilprofileBerichtsjahr2017.xlsx)

###### Ground Values
The ground value data can be downloaded from [here](http://suche.transparenz.hamburg.de/dataset/bodenrichtwerte-fur-hamburg6?forceWeb=true). A [list of direct links to the csv files](code/urls.txt) is available in the ```code```
directory.

### Data License
###### District Profiles
"Für Online-Veröffentlichungen, Online-Datenbanken, interaktive Atlanten, Jahrbücher, Themenbände, Statistische Berichte, Stadtteil- und Kreisprofile sowie kundenspezifische Aufbereitungen ist die auszugsweise Vervielfältigung und Verbreitung mit Quellenangabe gestattet." [Source](https://www.statistik-nord.de/agb/)

###### Ground Values
[Datenlizenz Deutschland - Namensnennung - Version 2.0](https://www.govdata.de/dl-de/by-2-0)
