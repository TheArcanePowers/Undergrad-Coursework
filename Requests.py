import requests  
from  requests import get, request  
import json  
import pandas as pd
#load url into a json object   
#print out headers
#convert json to dictionary 
#find key values for cumulative cases recovered etc.. vacciantion possibly
url="https://storage.googleapis.com/covid19-open-data/v3/epidemiology.json" #request epidemology.json 
result = requests.get(url) #get reponse data  
json_data = result.json()#we want it in json form 
python_result=json.loads(json_data) 
dframe = pd.DataFrame()#turn it into pandas data frame 
#if dframe['UKK11']: #filter for key with bristol
  #print cumulative recover,deceased,tested,confirmed key  
columns = dframe['columns'] 
print(columns)
