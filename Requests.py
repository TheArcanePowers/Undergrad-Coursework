import requests
import pandas as pd   
import matplotlib.pyplot as plt 
import numpy as np
confirmed_cases=[] 
N=[]
data = requests.get('https://pomber.github.io/covid19/timeseries.json') 
json_data = data.json()   
#Start date is 2020-1-22 
#So we can set the argument of the range to however many data sets we want  
for n in range(100):#number of days from intial starting date. 
    Dictionary = json_data['United Kingdom'][n] 
    confirmed= Dictionary['confirmed'] 
    confirmed_cases.append(confirmed) 
    N.append(n)
x=np.array(N) 
y=np.array(confirmed_cases)   
plt.plot(x,y)
plt.xlabel("Time") 
plt.ylabel("Confirmed Cases") 
plt.show()  