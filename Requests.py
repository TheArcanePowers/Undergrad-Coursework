import requests  
from  requests import get, request  
import json  
import pandas as pd 
# Query form location key equal = 
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url) #get reponse data  
json_data = result.json()#json_data is now a dictionary 

print(json_data.items())

