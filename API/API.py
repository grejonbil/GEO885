#API
from ast import Return
from cgi import test
import json
from tracemalloc import stop
from typing import Dict
import pandas as pd
import requests
import csv

# auth= '464c01f7e53b2a5e6f00d9a1'

def csv_files(file):  
    with open(file, encoding="utf-8") as csv:
        file = pd.read_csv(csv)
    return file

testCSV = csv_files("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/API/Test_Data.csv")
testCSV["emissionsKGCO2"] =""
print(testCSV)

def emissions(dataset):
    # Iterate all rows using DataFrame.itertuples()
    for row in dataset.itertuples(index = False):
        row = (getattr(row, "DEPARTURE_AIRPORT"), getattr(row, "ARRIVAL_AIRPORT"), getattr(row, "cabin_class"), getattr(row, "currencies"))
        print(row)
        j = row.to_dict("series")
        print(j)
        gaz = {}
        origin = j['DEPARTURE_AIRPORT']
        destination = j['ARRIVAL_AIRPORT']
        cabin_class = j['cabin_class']
        currencies = j["currencies"]
        gaz.update({"segments": [{ "origin": origin, "destination": destination},], "cabin_class": cabin_class, "currencies":[currencies]})
        
        data = gaz

        payload = {}

        for index, segment in enumerate(data["segments"]):
            origin = segment["origin"]
            destination = segment["destination"]
            # python 3.6+ needed:
            payload[f"segments[{index}][origin]"] = origin
            payload[f"segments[{index}][destination]"] = destination

        payload["cabin_class"] = data["cabin_class"]
        payload["currencies[]"] = data["currencies"]

        response = requests.get(
            "https://api.goclimate.com/v1/flight_footprint",
            auth=("464c01f7e53b2a5e6f00d9a1", ""),
            params=payload, 
        )

        d = response.text
        convertedDict = json.loads(d)
        footprint = convertedDict["footprint"]

        testCSV.loc[testCSV.index[row], 'emissionsKGCO2'] = footprint
    
print(emissions(testCSV))


# print("CSV TO DICTIONARY")
# with open("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/API/Test_Data.csv", newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             print(row['DEPARTURE_AIRPORT'], row['ARRIVAL_AIRPORT'], row["cabin_class"], row["currencies"])
            



