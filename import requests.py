from tkinter import N
import requests  
from  requests import get, request  
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np  
import json 

parameters="fields": {"area_name": "Bath and North East Somerset", "specimen_date": "2020-10-20", "daily_lab_confirmed_cases": 71, "cumulative_lab_confirmed_cases": 1393, "cumulative_lab_confirmed_cases_rate": 720.7, "geo_shape" 
url="https://opendata.bristol.gov.uk/api/v2/catalog/datasets/covid-19-cases/records?text=%22Somerset%22" 
result = request.get(url)  
jspn.dump(results)