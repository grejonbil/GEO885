# API
from curses import ERR
import json
from typing import List
import pandas as pd
import requests
import csv
import time
import re

tic = time.perf_counter()

def retrieve_IATA(FN_IATA, FN):
    # Key = 32c0d6-dbc517
    # Key2 = 23bd52-8dbdd9
    payload = ({"airlineIata":FN_IATA, "flightNumber": FN})

    # https://aviation-edge.com/v2/public/routes?key=23bd52-8dbdd9&airlineIata=LX&flightNumber=15 -> EXAMPLE

    answer = requests.get(
        'http://aviation-edge.com/v2/public/routes?key=23bd52-8dbdd9',
        params=payload,
    )

    print(answer.text)
    try:
        dep_code = json.loads(answer.text)[0]["departureIata"]
        arr_code = json.loads(answer.text)[0]["arrivalIata"]

    except KeyError:
        dep_code = None
        arr_code = None

    return dep_code, arr_code


def column_change(file):
    code_list = []
    code_list = pd.DataFrame(file['IATA_CODE'].tolist()).add_prefix("col")

    # file['IATA_CODE'] = pd.Series(file['IATA_CODE'], dtype="string")
    # file['IATA_CODE'] = str(file['IATA_CODE']).replace('(','').replace(')','')

    # file["DEPARTURE_AIRPORT_CODE"], file["ARRIVAL_AIRPORT_CODE"] = file['IATA_CODE'].str.split(',', 1).str
    print(code_list)
    return code_list

def retrieve_emissions(origin, destination, cabin_class, currencies):
    data = ({"segments": [{"origin": origin,
                           "destination": destination}, ],
             "cabin_class": cabin_class,
             "currencies": [currencies]})

    payload = {}
    for index, segment in enumerate(data["segments"]):
        origin = segment["origin"]
        destination = segment["destination"]
        payload[f"segments[{index}][origin]"] = origin
        payload[f"segments[{index}][destination]"] = destination

    payload["cabin_class"] = data["cabin_class"]
    payload["currencies[]"] = data["currencies"]

    response = requests.get(
        "https://api.goclimate.com/v1/flight_footprint",
        auth=("464c01f7e53b2a5e6f00d9a1", ""),
        params=payload,
    )
    # I added the exception here for flights with NA origin or destination, for which footprint is of course undefined
    try:
        footprint = json.loads(response.text)["footprint"]
    except KeyError:
        footprint = None

    return footprint

# testCSV = pd.read_csv("Test_Data_peter.csv")
amm_test = pd.read_csv("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_test.csv")
# amm = pd.read_csv("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm.csv")

amm_test["IATA_CODE"] = amm_test.apply(lambda x: retrieve_IATA(FN_IATA = x.fn_code, FN=x.fn_number), axis=1) 

column_change(amm_test)

# amm_test['EMISSIONS_KGCO2EQ'] = amm_test.apply(lambda x: retrieve_emissions(origin=x.DEPARTURE_AIRPORT,
#                                                                   destination=x.ARRIVAL_AIRPORT,
#                                                                   cabin_class=x.cabin_class,
#                                                                   currencies=x.currencies), axis=1)

print(amm_test)

print(amm_test["IATA_CODE"]. value_counts())

amm_test.to_csv(r"/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_test_emissions.csv", index=False)

toc = time.perf_counter()
print(f'- time to calculate: {toc - tic:0.4f} seconds')
