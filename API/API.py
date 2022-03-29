#API
import json
from typing import Optional
import pandas as pd
import requests
from http.client import HTTPSConnection
from base64 import b64encode

def csv_files(file):  
    with open(file, encoding="utf-8") as csv:
        csv_quake = pd.read_csv(csv)
    print("CSV INFO")
    print(csv_quake.info())
    return csv_quake

# amm = csv_files("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm.csv")

amm_test = csv_files("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/API/TestData.csv")
print(amm_test)

print("Payload ")
def emissions(amm_test):  # Create new dictionary only with necessary values needed, using the template provided by Ross
    test_dic = {} # New dictionary
    for i in range(0, len(amm_test)):
        if amm_test["origin"][i] == "origin":
            print()
            origin = origin
        if amm_test["destination"][i] == "destination":
            destination = destination
        if amm_test["cabin_class"][i] == "cabin_class":
            cabin_class = cabin_class
        test_dic.update({"segments": [{ "origin": origin, "destination": destination}], "cabin_class": cabin_class, "currencies":["USD"]})
    return payload

print(emissions(amm_test))

# def dic(file):
#     segment = file['Segments']  # Create new dictionary only with necessary values needed, using the template provided by Ross
#     gaz = {} # New dictionary
#     for i in segment:
#         origin = i['properties']['place']  # Names
#         destination = i['geometry']['coordinates']  # Coordinates (x,y,z)
#         cabin_class = i['properties']['mag']  # Magnitude
#         gaz.update({"segments": [{ "origin": origin, "destination": destination}], "cabin_class": cabin_class, "currencies":["USD"]})
#         # Furthermore, the z- value from each earthquake is separated from the longitude and latitude
#     return gaz
# gaz = dic(amm_test)

# auth= '464c01f7e53b2a5e6f00d9a1'




data = {
    "segments" : [
        { 
            "origin" : "ABQ",
            "destination" : "LAX"
        },
    ],
    "cabin_class" : "economy",
    "currencies" : [
        "USD"
    ]
}

payload = {}

for index, segment in enumerate(data["segments"]):
    origin = segment["origin"]
    destination = segment["destination"]
    # python 3.6+ needed:
    payload[f"segments[{index}][origin]"] = origin
    payload[f"segments[{index}][destination]"] = destination

payload["cabin_class"] = data["cabin_class"]

# requests can handle repeated parameters with the same name this way:
payload["currencies[]"] = data["currencies"]

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

    amm_test["Emissions"] = convertedDict["footprint"]
    print(amm_test)

update(response)
