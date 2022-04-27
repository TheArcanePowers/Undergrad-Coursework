from tkinter import N
import requests  
from  requests import get  
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np  
import json 
#try  
header = {}
url = "https://coronavirus.data.gov.uk/downloads/ondemand/easy_read/2022-04-26/ltla/ER_Bristol--City-of_2022-04-26.pdf" 
#execept so it doesnt break on this line of code
results = requests.get(url)  
soup = results.text 
soup = BeautifulSoup(soup,features="html.parser") 
soup.prettify() 
print(soup)

#right now we can get the java script data from a given website and it will turn it into a a python object SO "text" 
#would be out python object in this case

#first thing is we need to make a request then set parameters of that request so we can only get:Omicron,Normal,Delta infection and recovey and mortarilty statisics then we slap that in the simulation and boom done.
#Beautiful soup is for html 
#requests is for python objects 
#we want python objects 
#however we get alot unneccsary stuff 
#we need to filter through the json and then load 
#into python objects that we can use 
