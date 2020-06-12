import json
import csv
"""
The program reads the .csv file from the following data source: 
Google LLC "Google COVID-19 Community Mobility Reports".
https://www.google.com/covid19/mobility/ Accessed: 11 June 2020.
The data highlights the percent change in visits to places like grocery stores and parks within a geographic area 
over a period of time.

The .csv file has the below headers:
country_region_code, country_region, sub_region_1, sub_region_2, date, 
retail_and_recreation_percent_change_from_baseline, grocery_and_pharmacy_percent_change_from_baseline, 
parks_percent_change_from_baseline, transit_stations_percent_change_from_baseline, 
workplaces_percent_change_from_baseline,residential_percent_change_from_baseline

The program reads and converts the data into a json format like the one below:
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
and so on.    
"""


def main():
    data = {}
    filename = 'Global_Mobility_Report.csv'
    add_data(data, filename)
    json.dump(data, open('mobility.json', 'w'))


def add_data(data, filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            if i == 0:
                keys = line
                i += 1
            else:
                values = line
                dict_values = {keys[j]: values[j] for j in range(len(values))}

                if dict_values['sub_region_1'] == '':
                    date = dict_values['date']
                    country = dict_values['country_region']

                    if not date in data:
                        data[date] = {}

                    if not country in data:
                        data[date][country] = {}

                    for count in range(5, len(dict_values)):
                        key = list(dict_values.keys())[count]
                        value = dict_values[key]
                        data[date][country][key] = value
                i += 1


if __name__ == '__main__':
    main()
