#API
from cgi import test
import json
from typing import Optional
import pandas as pd
import requests
from http.client import HTTPSConnection
from base64 import b64encode
import csv
from urllib.request import Request, urlopen
import time
from collections import defaultdict


# auth= '464c01f7e53b2a5e6f00d9a1'

def csv_files(file):  
    with open(file, encoding="utf-8") as csv:
        csv_quake = pd.read_csv(csv)
    print("CSV INFO")
    print(csv_quake.info())
    return csv_quake

testCSV = csv_files("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/API/Test_Data.csv")
print(testCSV)

# testdata = {'DEPARTURE_AIRPORT': ['CGN', 'CDG', 'VIE', 'VIE', "VAR"],
# "ARRIVAL_AIRPORT": ["ZRH", "VIE", "ZRH", "VAR", "VIE"] , 
# 'cabin_class': ["economy","economy","economy","economy","economy"], 
# "currencies":["USD","USD","USD","USD","USD"]}  
# print(testdata)

print("Payload ")
def emissions(testCSV):
    result = defaultdict(list)
    for org, arr, abc, cur in zip(*testCSV.values()):
        result["segments"].append({
                "origin": org,
                "destination": arr})
        result["cabin_class"].append(abc)
        result["currencies"].append(cur)
    return dict(result)
print(emissions(test))


data = {"segments" : [{"origin" : "CGN","destination" : "ZRH"},],"cabin_class" : "economy","currencies" : ["USD"]}
def co2(n):
    payload = {}

    for index, segment in enumerate(n["segments"]):
        origin = segment["origin"]
        destination = segment["destination"]
        # python 3.6+ needed:
        payload[f"segments[{index}][origin]"] = origin
        payload[f"segments[{index}][destination]"] = destination

    payload["cabin_class"] = n["cabin_class"]

    # requests can handle repeated parameters with the same name this way:
    payload["currencies[]"] = n["currencies"]
    print(payload)

    response = requests.get(
        "https://api.goclimate.com/v1/flight_footprint",
        auth=("464c01f7e53b2a5e6f00d9a1", ""),
        params=payload, 
    )

    def update(response):
        print("API")
        print(response.content)
        d = response.text
        convertedDict = json.loads(d)
        print(convertedDict["footprint"])
        # print(convertedDict["offset_prices"]["amount"])

        test["Emissions"] = convertedDict["footprint"]
        #test["Price USD"] = convertedDict["offset_prices"]["amount"]
        print(testCSV)

    update(response)

print(co2(data))
