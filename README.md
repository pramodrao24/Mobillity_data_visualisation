# Mobillity_data_visualisation
Visualises Google's mobility data over the following period: Feb 15th to 7th June

## Steps to run the program:
###### 1. Download the most recent .csv file from the below data source
Google LLC "Google COVID-19 Community Mobility Reports".
https://www.google.com/covid19/mobility/ 
Last accessed: 12 June 2020. (for the program, you will find it in the files on Github)

The data highlights the percent change in visits to places like grocery stores and parks within a geographic area 
over a period of time.

## 2. Run the mobility_build.py to re-write the mobility.json file

The program reads the .csv file. 

The program assumes the .csv file has the below headers (as of the latest data pull on 12th June 2020):
'country_region_code', 'country_region', 'sub_region_1', 'sub_region_2', 'iso_3166_2_code', 'census_fips_code', 'date', 
'retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline', 
'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 
'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'


The program reads and converts the data into a json format like the one below:
'''
{
    "2020-02-15": 
        {"United Arab Emirates": 
            {"retail_and_recreation_percent_change_from_baseline": "0", 
            "grocery_and_pharmacy_percent_change_from_baseline": "4", 
            "parks_percent_change_from_baseline": "5", 
            "transit_stations_percent_change_from_baseline": "0", 
            "workplaces_percent_change_from_baseline": "2", 
            "residential_percent_change_from_baseline": "1"},
        "Afghanistan": {},
        ...
        },
    "2020-02-16":
        {...
        }
'''
and so on.    


###### 3. Run the mobility_visualise.py to see the visualisation. 

It will prompt you to enter a country name e.g. India or United States or United Kingdom

The program assumes that the mobility.json stores values in the format where each date is a dictionary from 
country name to country data. Example below:
'''
{
    "2020-02-15": 
        {"United Arab Emirates": 
            {"retail_and_recreation_percent_change_from_baseline": "0", 
            "grocery_and_pharmacy_percent_change_from_baseline": "4", 
            "parks_percent_change_from_baseline": "5", 
            "transit_stations_percent_change_from_baseline": "0", 
            "workplaces_percent_change_from_baseline": "2", 
            "residential_percent_change_from_baseline": "1"},
        "Afghanistan": {},
        ...
        },
    "2020-02-16":
        {...
        }
'''
and so on.
