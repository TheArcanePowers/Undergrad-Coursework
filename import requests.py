import requests  
from  requests import get  
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np  
import json 
#try  
header = 
url = "https://coronavirus.data.gov.uk/downloads/ondemand/easy_read/2022-04-26/ltla/ER_Bristol--City-of_2022-04-26.pdf" 
#execept so it doesnt break on this line of code
results = requests.get(url) 
def pyprint(obj):
    # create a formatted string of the Python JSON object
    text = json.loads(obj, sort_keys=True, indent=4)
    print(text)

pyprint(results.json())  

#right now we can get the java script data from a given website and it will turn it into a a python object SO "text" 
#would be out python object in this case


