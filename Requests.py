import requests  
from  requests import get, request  
import json  
import pandas as pd  
params=("UK") 
#we need to fix this url because this data set is to large we need to parse for info we care about 
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url,params) #get reponse data  
json_data = result.json()#json_data is now a dictionary   
columns = json_data['columns']  
#we just need to find a way through our code and systematically on print Bristol ISO Codes and  
# respective colums  
