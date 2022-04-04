#we got to do this for each variant like its a diffrent data set every time ref jpeg  
input=("Type in a Vaccine for Omnicron?") 
def vaccination_Omnicron():  
    global input  
#make a dictionary where you have the probabilities of infection and the diffrent covid variants  
    omicron_vaccine_data = dict( 
        Astrazeneca="0.36", 
        CanSino="0.32", 
        CoronaVac="0.24", 
        Covaxin="0.38", 
        JohnsonJohnson="0.33",
        Moderna="0.48", 
        Novavax="0.43", 
        Pfizer="0.44" ,
        Other_mrna="0.45" , 
        SinoPharm="0.35" ,
        Sputnik_V="0.44" ,
    ) 
    for i,k in omicron_vaccine_data.items(): 
        if input == str(i):   
            print(i[k]) 



vaccination_Omnicron()