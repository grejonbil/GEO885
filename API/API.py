# API
import json
import pandas as pd
import requests
import csv


def retrieve_emissions(origin, destination, cabin_class, currencies):
    data = ({"segments": [{"origin": origin,
                           "destination": destination}, ],
             "cabin_class": cabin_class,
             "currencies": [currencies]})

    # Peter: I am still not sure what the following lines do and why they are necessary
    # Seems you have to get things into a format that go climate understands, but why do you use
    # a for loop here when there is always only one segment per flight? Or is that different in the full data set?

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


# I had problems reading the csv file
# The first column does not have a header, which caused pd.read_csv to miss-align columns and column headers
# e.g. the column with departure airports had the column header "cabin_class"
# "Test_Data_peter.csv" has these issues fixed
# testCSV = pd.read_csv("Test_Data_peter.csv")
amm_test = pd.read_csv("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_test.csv")
# amm_test = pd.read_csv("/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_test.csv")

amm_test['EMISSIONS_KGCO2EQ'] = amm_test.apply(lambda x: retrieve_emissions(origin=x.DEPARTURE_AIRPORT,
                                                                  destination=x.ARRIVAL_AIRPORT,
                                                                  cabin_class=x.cabin_class,
                                                                  currencies=x.currencies), axis=1)
print(amm_test)

amm_test.to_csv(r"/Users/chaualala/Desktop/UZH/MSc Geographie/2. Semester/GEO885 - GIS Science Project/GEO885/R/amm_test_emissions.csv", index=False)