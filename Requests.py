import requests
import pandas as pd 
data = requests.get('https://pomber.github.io/covid19/timeseries.json') 
print(type(data)) 
json_data = data.json() 
print(json_data['United Kingdom'][1])