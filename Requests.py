import requests  
from  requests import get, request  
import json  
import pandas as pd  
parameters=("location_key":"UK")
#we need to fix this url because this data set is to large we need to parse for info we care about 
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url,parameters) #get reponse data  
json_data = result.json()#json_data is now a dictionary   
d=pd.read_json(json_data) 
print(d)
#we just need to find a way through our code and systematically on print Bristol ISO Codes and  
# respective columns  
