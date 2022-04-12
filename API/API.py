# API
import json
import pandas as pd
import requests
import time

tic = time.perf_counter()
    # Key = 32c0d6-dbc517
    # Key2 = 23bd52-8dbdd9 -> Used in this code

def retrieve_IATA_dep(FN_IATA, FN):
    global dep_code_iata
    payload = ({"airlineIata":FN_IATA, "flightNumber": FN})
    answer = requests.get(
        'http://aviation-edge.com/v2/public/routes?key=23bd52-8dbdd9',
        params=payload)

    print(answer.text)
    try:
        dep_code_iata = json.loads(answer.text)[0]["departureIata"]

    except json.JSONDecodeError:
        print("Error decoding JSON")

    except KeyError:
        dep_code_iata = "MISSING"

    return dep_code_iata

def retrieve_IATA_arr(FN_IATA, FN):
    global arr_code_iata
    payload = ({"airlineIata":FN_IATA, "flightNumber": FN})
    answer = requests.get(
        'http://aviation-edge.com/v2/public/routes?key=23bd52-8dbdd9',
        params=payload)

    print(answer.text)
    try:
        arr_code_iata = json.loads(answer.text)[0]["arrivalIata"]
    
    except json.JSONDecodeError:
        print("Error decoding JSON")

    except KeyError:
        arr_code_iata = "MISSING"

    return arr_code_iata

def column_change(file):
    file.DEPARTURE_AIRPORT.fillna(file.IATA_CODE_DEP,inplace=True)
    file.ARRIVAL_AIRPORT.fillna(file.IATA_CODE_ARR,inplace=True)
    return 

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
        footprint = "MISSING"

    return footprint

amm = pd.read_csv("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_incomplete.csv")

amm["IATA_CODE_DEP"] = amm.apply(lambda x: retrieve_IATA_dep(FN_IATA = x.fn_code, FN=x.fn_number), axis=1) 
amm.to_csv(r"/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_complete.csv", index=False)


amm["IATA_CODE_ARR"] = amm.apply(lambda x: retrieve_IATA_arr(FN_IATA = x.fn_code, FN=x.fn_number), axis=1) 
amm.to_csv(r"/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_complete.csv", index=False)


column_change(amm) #Transfers all values from the API column to the missing NA values in the columns DEPARTURE_AIRPORT and ARRIVAL_AIRPORT
amm.to_csv(r"/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_complete.csv", index=False)


amm['EMISSIONS_KGCO2EQ'] = amm.apply(lambda x: retrieve_emissions(origin=x.DEPARTURE_AIRPORT,
                                                                  destination=x.ARRIVAL_AIRPORT,
                                                                  cabin_class=x.cabin_class,
                                                                  currencies=x.currencies), axis=1)

amm.to_csv(r"/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_complete.csv", index=False)
print(amm)

toc = time.perf_counter()
print(f'- time to calculate: {toc - tic:0.4f} seconds')
