import requests  
from  requests import get, request  
import json  
import pandas as pd  
parameters={'date':"", 
'location_key':"UK",'new_confirmed':"",'new_deceased':"",'new_recovered':"",'new_tested':"",'cumulative_confirmed':"",'cumulative_deceased':"",'cumulative_recovered':"",'cumulative_tested':""}
#we need to fix this url because this data set is to large we need to parse for info we care about 
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url,params=parameters) #get reponse data  
json_data = result.json()#json_data is now a dictionary   
columns = json_data['2020-05-03']  
#we just need to find a way through our code and systematically on print Bristol ISO Codes and  
# respective colums  
