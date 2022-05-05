#we got to do this for each variant like its a diffrent data set every time ref jpeg  

#make a dictionary where you have the probabilities of infection and the diffrent covid variants  
from logging import exception


omicron_vaccine_data = { 
        "Astrazeneca":0.36, 
        "CanSino":0.32, 
        "CoronaVac":0.24, 
        "Covaxin":0.38, 
        "JohnsonJohnson":0.33,
        "Moderna":0.48, 
        "Novavax":0.43, 
        "Pfizer":0.44 ,
        "Other_mrna":0.45 , 
        "SinoPharm":0.35 ,
        "Sputnik_V":0.44 ,
    } 
def get_key(val):
    for key, value in omicron_vaccine_data.items():
         if val == value:
             return key
 
    return "There is no such value"

#Problem is when you get two Vaccines with the same infection rate it only outputs one
print(get_key(0.36))

