import requests  
from  requests import get, request  
import json  
import pandas as pd 
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url) #get reponse data  
json_data = result.json()#json_data is now a dictionary   


colums = json_data['columns'])
#we just need to find a way through our code and systematically on print Bristol ISO Codes and  
# respective colums  
