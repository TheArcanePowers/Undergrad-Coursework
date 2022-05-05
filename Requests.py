import requests
import pandas as pd 
data = requests.get('https://pomber.github.io/covid19/timeseries.json') 
print(type(data)) 
json_data = data.json()  
#Start date is 2020-1-22 
#So we can set the argument of the range to however many data sets we want
for i in range(700):
    print(json_data['United Kingdom'][i]) 

