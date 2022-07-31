import requests
data = requests.get('https://pomber.github.io/covid19/timeseries.json') 
json_data = data.json()   
  
Dictionary = json_data['United Kingdom']  
print(len(Dictionary))
