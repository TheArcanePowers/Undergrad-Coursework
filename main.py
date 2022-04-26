## ROAD MAP 1
# 1. SIR Model Funciton with varying population sizes and probabilities
# Roadmap 1: create model with function 1, then feed that and data into function 2 and get output from function 2

# RoadMap 1
from re import T
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from numpy import var 
from simulations import Simulation
from vaccination_data import omicron_vaccine_data




# asks for input of population size
while True:
    try:
        population_size = int(input("Please enter a population size you would like to sample:"))
        break 
    except ValueError:
        print("Please enter only a number for the population size")


# reduce that to make a model (divide by 500, 1000, etc...)
if population_size >=1 and population_size < 10:
    reduction = population_size * 10**3
    reduction_by = 10**3
    
elif population_size >=10 and population_size < 100:
    reduction = population_size * 10**2
    reduction_by = 10 //10**2
    
elif population_size >=100 and population_size < 1000:
    reduction = population_size * 10
    reduction_by = 10 // 10
    
elif population_size >=1000 and population_size < 10000:
    reduction = population_size * 1

elif population_size >=10000 and population_size < 100000:
    reduction = population_size // 10
    reduction_by = 10*1
   
elif population_size >=100000 and population_size < 1000000:
    reduction = population_size // 10**2
    reduction_by = 10**2
    
elif population_size >=1000000 and population_size < 10000000:
    reduction = population_size // 10**3
    reduction_by = 10**3
    
elif population_size >=10000000 and population_size <= 68000000: #should not exceed 68m is Uk population
    reduction = population_size // 10**4
    reduction_by = 10**4
else:
   if population_size >68000000:
       print("Please do not exceed the Uk Population of 68 million")
while True:
    try:
        days= int(input("How many days do you want to simulate for?"))
        break
    except ValueError:
        print("Please enter a number only")
       
# run the simulation
# variant option for different infection and removal rates
while True:
    variant_choice= input("Please choose what variant you would like to simulate: (N) for Normal; Pre-Alpha Variant, (D) for Delta or (O) for Omicron")
    if variant_choice in ("N", "D", "O"):
        break
    else:
        print("Error: Please pick one of the variant options only")

if variant_choice == "N":
    infection_rate = 0.08 
    removal_rate = 0.01


elif variant_choice == "D":
    infection_rate= 0.11
    removal_rate= 0.001

elif variant_choice == "O":
    infection_rate= 0.3
    removal_rate= 0.02

while True:
    print(list(omicron_vaccine_data.keys()))
    vaccine_choice = input("Please choose what vaccine you would like to tackle the chosen variant")
    if vaccine_choice in omicron_vaccine_data.keys():
        break
    else:
        print("Please choose a correct vaccine")


    

# recieve results

# diplay results
model, trends = Simulation(reduction, infection_rate, removal_rate, time_simulated= days).SimpleSEIR()
viz = DiffusionTrend(model, trends)
viz.plot("Simple_SEIR_MODEL.pdf")

#p = viz.plot("Simple_SEIR_MODEL.pdf")
#show(p)

############################################################################################################ ROADMAP 2
# Turn STATIC MODEL INTO DYNAMIC MODEL

## ROADMAP 2
# 1. compares model to real world data (takes input the model object)
# DIFFUSION ON DYNAMIC NETWORKS - DO A SIR DYNAMIC MODEL 

# ROADMAP 3
# 1. Function that reads vaccination data - MAKE IT INTO UTLDR
# 2. ROADMAP 1 & 2 SIR Model, addapted with vaccination data

# ROADMAP 4
# Model Comparison https://ndlib.readthedocs.io/en/latest/reference/viz/mpl/TrendComparison.html