from tkinter import N
import requests  
from  requests import get  
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np  
import json 
#try  
header = {}
url = "https://opendata.bristol.gov.uk/explore/embed/dataset/covid-19-cases/table/?sort=specimen_date?SELECT Bristol,City FROM Area name" 
#execept so it doesnt break on this line of code
results = requests.get(url)  
doc = BeautifulSoup(results.text,"html.parser")  
doc1 = doc.find_all(type = "str") 
print(doc1)
#right now we can get the java script data from a given website and it will turn it into a a python object SO "text" 
#would be out python object in this case

#html parse 