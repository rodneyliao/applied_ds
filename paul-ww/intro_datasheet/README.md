# Predicting Ground Value Performance based on District Demographics

## Introduction

For my term project, I have analyzed data about my hometown Hamburg in Germany. Using data from the town's open data portal, I focus on the relationship between district characteristics and estimated real estate prices. To do this, I rely on two different datasets:

##### Estimated Real Estate Prices
 In the state of Hamburg, the regional government estimates prices per $m^2$ for various properties and publishes the results in regular intervals. The so-called *Bodenrichtwert* (standard ground value) estimates the price of a property per $m^2$ according to features such as location, area, zoning and stage of development. I have data from 1964 to 2017 to work with, making up more than 2,000,000 rows with about 10 to 15 usable columns containing feature data. Since my second dataset only has data from 2007 onwards, I mostly rely on the time period from 2007 to 2017.

##### District Profiles
 My second dataset are the so-called *Stadtteilprofile* (district profiles), which contain socio-economic and demographic data on a district level. Unfortunately, these are only available for the years 2007 until 2017. The profiles, once put together, will contain about approx. 100 districts with approx. 60 columns of feature data as yearly snapshots, making up a total of about 1000 rows.

## Project Question
By combining both datasets, I analyze the predictive power of district characteristics on real estate price development. While I could make use of the ground value data for the years 1964 to 2017, I decided to reduce the scope of my analysis to the time frame of 2007 to 2017, for which my data is the most complete. My work on this project centers around three questions:
1. *How well do the real estate price estimates issued by the city compare to the actual real estate prices in terms of accuracy?*
2. *How are district features and estimated ground values per district related?*
3. *Can average property prices in a district be predicted by the district's socio-economic or demographic profile?*

To answer the first question, I analyze the relationship between estimated ground values and actual prices paid by comparing the estimates from the ground value data and the real estate prices from the district profiles dataset. Since the estimates are generated from past prices paid, I expect these two variables to be closely related.

In order to answer the second question, I have a look at the features the correlate most strongly with the ground value estimates. I also check for cross-correlations among the variables thus identified.

I then try to answer the third question by first identifying those districts which outperformed the city-wide average growth in ground value and then constructing a logistic regression classifier that tries to predict outperformance based on a district's demographic features.

My results could be relevant in the real estate business, where finding or even predicting trends in property prices is vital. It could also be helpful for the regional government, as it could identify cases of public expenditure leading to higher property prices or rents or if public investment should go to one district or to another.

## Data Provenence

##### Estimated Real Estate Prices
Each year, the *Gutachterausschuss für Grundstückswerte* (committe for the assessment of real estate value) publishes its estimates of what one $m^2$ of a any particular property in the city might cost. These estimates are based on the record of actual real estate prices paid for comparable properties in the vicinity. The official document describing the legal framework for the aggregation of the dataset can be found in the file ```BRW-Erkaeuterungen2017.pdf``` in this directory.

The dataset is only available year by year and is thus split up into multiple source files. In my note ground value notebook, I have therefore included a cell which will download the data for all available years from [Hamburg's open data portal](http://suche.transparenz.hamburg.de/dataset/bodenrichtwerte-fur-hamburg6?forceWeb=true), which requires space for about 4GB of ```.csv``` files. Links to all the individual files can be found in the ```urls.txt``` file in the ```code``` directory. The files contain the following columns of data relevant to my analysis:


| Variable Name | Variable Label                              |
| :------------ | :------------------------------------------ |
| ORTSN         | district                                    |
| WNUM          | unique identifier for property              |
| BRW           | estimated property price in EUR per \(m^2\) |
| STAG          | date of estimate                            |
| PLZ           | zip code                                    |
| YWERT         | y-coordinate (GIS)                          |
| XWERT         | x-coordinate (GIS                           |
| NUTA          | current development / kind of usage         |
| WGFZ          | floor to area ratio                         |
| FLAE          | area                                        |
| BEM           | views, special locations                    |

For a full list list of variables contained in the ```.csv``` files, have a look at my ground value notebook in which I clean the downloaded data. A description of each of the variables and their data types can be found in the file ```d-vboris-modellbeschreibung.pdf``` inside this directory.

##### District Profiles
The district profiles for the years 2007 to 2016 are available from the website of [Statistikamt Nord](https://www.statistik-nord.de/fileadmin/Dokumente/Datenbanken_und_Karten/Stadtteilprofile/Stadtteilprofile-Berichtsjahre-2007-2016.xlsx), which provides access to data collected by the state of Hamburg. The data provider only aggregates and distributes the data in this case, as the district profiles are reported to Statistik Nord by the individual administrative units. These local government centers are in possession of demographic data of their particular area as residents are required to register themselves with a local the administration when permanently moving there. By registering, individuals also consent to having their data published as part of aggregate statistics that do not contain any personally identifiable information.

I have included a table showing all of the variables occurring in the district profiles. Some are only present for one or two years, but quite a few occur over the entire 10-year period, depending on the scope of the report prepared by Statistik Nord for a particular year. Although the data seems pretty clean, combining the data into one large set will be difficult, as the column titles differ across all sheets of the Excel file, making it difficult to merge the data. I think that the task of combining the yearly datasets into one large file will take the largest amount of time. I have tried to come up with translations for the variable names, as the original is in German:

|Variable Name|Variable Label|
|--- |--- |
|population|district population|
|u18|individuals <18|
|u18_rel|individuals <18, share of pop|
|o64|individuals >64|
|o64_rel|individuals >64, share of pop|
|for|foreigners|
|for_rel|foreigners, share of total|
|migr|2nd gen immigrants|
|migr_rel|2nd gen immigrants, share of pop|
|migr_u18_rel|2nd gen immigrants <18, share of pop|
|migr_u18_rel_u18|2nd gen immigrants <18, share of migr_rel|
|hholds|households|
|hholds_mean_size|mean individuals per household|
|hholds_single|single households|
|hholds_single_rel|single households, share of all|
|hholds_kids|households with children|
|hholds_kids_rel|households with children, share of all|
|hholds_single_parent|households with single parents|
|hholds_single_parent_rel|households with single parents, share of all|
|area|district area in km2|
|density|district population density|
|births|number of births|
|deaths|number of deaths|
|influx|people moving into the district|
|influx_regional|people moving into the district from the surrounding regions|
|outflux|people moving out of the district|
|outflux_regional|people moving out of the district into surrounding regions|
|in_out_diff|difference between people moving in and out|
|in_out_diff_rel|difference between people moving in and out, share of population|
|emp_ins|individuals employed with full social insurance benefits|
|emp_ins_rel|individuals employed with full social insurance benefits, share of 15-65|
|emp_ins_f|female individuals employed with full social insurance benefits|
|unemp|unemployed individuals|
|unemp_rel|unemployed individuals, share of 15-65|
|unemp_15_25|unemployed between 15 and 25|
|unemp_15_25_rel|unemployed between 15 and 25, share of 15-25|
|unemp_55_65|unemployed between 55 and 65|
|unemp_55_65_rel|unemployed between 55 and 65, share of 55-65|
|unemp_sgb2|long-term unemployed|
|unemp_sgb2_rel|long-term unemployed, share of 15-65|
|rec_sgb2|individuals receiving SGB2|
|rec_sgb2_rel|individuals receiving SGB2, share of pop|
|rec_sgb2_u15|individuals receiving SGB2 < 15|
|rec_sgb2_u15_rel|individuals receiving SGB2 < 15, share of pop < 15|
|hholds_shared|shared households because of SGB2|
|tax_pop|population paying income and wage tax|
|tax_revenue|revenue from income and wage tax|
|voters|eligible voters|
|turnout|voter turnout in most recent election|
|cdu|vote share for CDU party in most recent election|
|spd|vote share for SPD party in most recent election|
|greens|vote share for Green party in most recent election|
|left|vote share for Left party in most recent election|
|fdp|vote share for FDP party in most recent election|
|res_buildings|residential buildings|
|homes|homes (condos, apt, houses)|
|homes_completed|newly completed homes in year|
|homes_in_houses|homes in houses|
|homes_in_houses_rel|homes in house, share of all homes|
|homes_mean_size|mean home size in m2|
|homes_mean_living_area|mean home living area in m2|
|social_housing|social housing units|
|social_housing_rel|social housing units, share of all units|
|social_housing_rentcontr_6y|units leaving rent control in 6y|
|social_housing_rentcontr_6y_rel|units leaving rent control in 6y, share of all units|
|real_estate_price_mean|mean real estate price per m2 in EUR|
|house_price_mean|mean house price per m2 in EUR|
|condo_price_mean|mean condo price per m2 in EUR|
|kinder_pre|number of kindergardens and preschools|
|pri_schools|primary schools|
|sec_schools|secondary schools|
|students_sek1|students on A-level track|
|students_not_gym|students enrolled in school with focus on vocational track|
|students_gym|students enrolled in Gymnasium (high school w/ academic focus)|
|students|number of students|
|students_for|number of foreign students|
|students_for_rel|number of foreign students, share of all|
|handicraft|handicraft businesses|
|doctors_resident|resident doctors|
|doctors_gp|general practitioners|
|doctors_dentist|dentists|
|pharmacies|pharmacies|
|cars_priv_business|number of privately used and business cars|
|cars_private|number of private cars|
|cars_priv_business_per_1000|number of privately used and business cars, per 1000 inhabitants|
|cars_private_per_1000|number of private cars, per 1000 inhabitants|
|cars_priv_business_ssk4|number of privately used and business cars, conforming to emission standard 4|
|cars_private_ssk4|number of private cars, conforming to emission standard 4|
|cars_priv_business_ssk4_rel|number of privately used and business cars, conforming to emission standard 4, share of all|
|accidents|traffic accidents|
|accidents_people|traffic accidents involving people being injured|
|accidents_expensive|traffic accidents with high damages|
|crime|crimes committed|
|crime_per_1000|crimes committed per 1000 inhabitants|
|crime_violent|violent crimes committed|
|crime_violent_per_1000|violent crimes committed per 1000 inhabitants|
|crime_theft|thefts|
|crime_theft_per_1000|thefts per 1000 inhabitants|

For further information on the particularities of the data, please also see the corresponding Datasheet inside this directory.

## Literature Review
The data that I am working with have not been used in many publications. Two examples that cite usage of the district profile data include [Melchert (2012) an analysis of rent and property prices in the newly developed district of *Hafencity*](https://books.google.de/books?hl=de&lr=&id=6Y5kAQAAQBAJ&oi=fnd&pg=PR3&ots=ct07AtwPIX&sig=Pln_wq-dWbmpbYjrFY6ZZMoA4oA&redir_esc=y#v=onepage&q&f=false) and [Schlünzen and Linde (2014), a work on the expected impact of climate change on a certain district](https://pure.mpg.de/rest/items/item_2148697/component/file_2465323/content).
The ground value data provided by the city of Hamburg is frequently used in news publications to estimate the real estate price changes over time. Furthermore, the data is often used and cited in documents published by the city. One example for such a case is the [official presentation of the home construction program of 2012 in the district of Altona](http://epub.sub.uni-hamburg.de/epub/volltexte/2016/50182/pdf/wohnungsbauprogramm_altona_2012_.pdf). Outside the local administration, I was not able to find publications citing usage of Hamburg's ground value data, however. Nevertheless, there are a few publications that make use of ground value data provided by other German communities, such as Arndt (2014) or Andrae (2009), which point out some use cases for the data.
One current topic involving the topic of estimated ground values is the planned overhaul of the property tax system across Germany. One example of the role of ground values in this question is provided by Henger and Schaefer (2015).


##### References
Melchert, Isabella. Die immobilienwirtschaftliche Entwicklung im neuen Hamburger Stadtteil HafenCity. Eine Bestandsanalyse unter besonderer Berücksichtigung der Immobilienleerstände. diplom.de, 2012.

Schlünzen, Heinke, and Marita Linde. Wilhelmsburg im Klimawandel: Ist-Situation und mögliche Veränderungen. TuTech Verlag, 2014.

Altona, Bezirksamt. "Wohnungsbauprogramm Altona 2012."

Arndt, Christina. Bodenrichtwerte in kaufpreisarmen Gebieten: Untersuchungen über die Struktur in Goslar/Harz. Igel Verlag RWS, 2014.

Andrae, Michael. "Web-Plattform für das Rating und Benchmarking von Immobilien und Portfolioanalysen." Rating von Einzelhandelsimmobilien. Gabler, 2009. 297-315.

Henger, Ralph, and Thilo Schaefer. Mehr Boden für die Grundsteuer: Eine Simulationsanalyse verschiedener Grundsteuermodelle. No. 32/2015. IW policy paper, 2015.
