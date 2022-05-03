import requests  
from  requests import get, request  
import json  
import pandas as pd 
# Query form location key equal = 
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url) #get reponse data  
json_data = result.json()#we want it in json form 
dframe = pd.DataFrame(json_data)#turn it into pandas data frame 
#if dframe['UKK11']: #filter for key with bristol
  #print cumulative recover,deceased,tested,confirmed key  
columns = dframe['columns'] 
print(columns)
