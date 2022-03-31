# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:13:31 2022

@author: Mike Werfeli and Peter Ranacher
"""
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


fln_no = ["LX4425", "OS420", "OS553", "0S763"]
# prepare new list

updated_flight_list = []


for flight_no in fln_no:
    print('working on ' + flight_no)
    
    # prepare request to be sent to flightradar24.com
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url='https://www.flightradar24.com/data/flights/' + flight_no, headers = header)
    html = urlopen(req).read()
    
    # convert to readable string
    #text = str(html)
    print(html.text)
    
    # extract origin of flight number in html which was converted to str
    idx_start = text.find("FROM</label> <span class=\"details\"> ")
    rest_text = text[(idx_start + 36):]
    idx_end = rest_text.find("<a href")
    origin = rest_text[1:(idx_end - 1)]
    
    # extract destination of flight number in html which was converted to str
    text = str(html)
    idx_start = text.find("TO</label> <span class=\"details\"> ")
    rest_text = text[(idx_start + 34):]
    idx_end = rest_text.find("<a href")
    destination = rest_text[1:(idx_end - 1)]
    
    # store information in new csv
    temp = []
    temp.append(flight_no)
    temp.append(origin)
    temp.append(destination)
    updated_flight_list.append(temp)    
    
    time.sleep(5)

print(updated_flight_list)
