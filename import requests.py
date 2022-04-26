import requests  
from  requests import get  
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np  
import json 
#try 
url = "https://opendata.bristol.gov.uk/api/v2/console/catalog/datasets/covid-19-cases/export/json/api_key = test;" 
#execept so it doesnt break on this line of code
results = requests.get(url) 
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(results.json())

