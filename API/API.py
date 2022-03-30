#API
from ast import Return
from cgi import test
import json
from tracemalloc import stop
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

def emissions(file):
    for i in range(0, len(file)):
        print("DATA")
        def dic(file):
            gaz = {}
            origin = file['DEPARTURE_AIRPORT']
            destination = file['ARRIVAL_AIRPORT']
            cabin_class = file['cabin_class']
            currencies = file["currencies"]
            gaz.update({"segments": [{ "origin": origin, "destination": destination},], "cabin_class": cabin_class, "currencies":[currencies]})
            return gaz
        data = dic(file)
        print(data)

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

        testCSV.loc[testCSV.index[i], 'emissionsKGCO2'] = footprint
        print(testCSV)

print("CSV TO DICTIONARY")
with open("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/API/Test_Data.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['DEPARTURE_AIRPORT'], row['ARRIVAL_AIRPORT'], row["cabin_class"], row["currencies"])
            print(emissions(row))



