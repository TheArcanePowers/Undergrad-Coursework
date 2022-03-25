## ROAD MAP 1
# 1. SIR Model Funciton with varying population sizes and probabilities
# Roadmap 1: create model with function 1, then feed that and data into function 2 and get output from function 2

# RoadMap 1

from re import A
import re
from simulations import SimpleSIER

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
    print(reduction)
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
elif population_size >=10000000 and population_size < 68000000: #should not exceed 68m is Uk population
    reduction = population_size // 10**4
    reduction_by = 10**4
    print(reduction)
else:
    print("Please do not exceed the Uk Population of 68 million")
    


# find the size -> 0.5 x 10^6, so it does 0.5 x 10^3 and then remembers to multiply resilts by 10^3

# run the simulation

# recieve results

# diplay results

viz = SimpleSIER(365)
viz.plot("diffusion1.pdf")

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