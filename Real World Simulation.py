#simulation for the United Kingdom 
#Start date is 2020-1-22 
from cmath import log
import requests
import pandas as pd   
import matplotlib.pyplot as plt 
import numpy as np
confirmed_cases=[] 
Deaths=[]  
Recovered=[] 
N=[]
data = requests.get('https://pomber.github.io/covid19/timeseries.json') 
json_data = data.json()   
#So we can set the argument of the range to however many data sets we want  
for n in range(600):#number of days from intial starting date. 
    Dictionary = json_data['United Kingdom'][n] 
    confirmed= Dictionary['confirmed'] 
    deaths=Dictionary['deaths'] 
    recovered=Dictionary['recovered']  
    Recovered.append(recovered)  
    confirmed_cases.append(confirmed)  
    Deaths.append(deaths) 
    N.append(n)
x=np.array(N) 
y=np.array(confirmed_cases)  
d=np.array(Deaths) 
c=np.array(Recovered)  
plt.plot(x,y,color='r', label='Confirmed_Cases') 
plt.plot(x,c,color='g', label='Recovered') 
plt.plot(x,d,color='b', label='Deaths')
plt.xlabel("Time(Days)")  
plt.ylabel("No.people")  
plt.legend() 
plt.show()   
