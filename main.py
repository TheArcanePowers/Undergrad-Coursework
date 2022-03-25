## ROAD MAP 1
# 1. SIR Model Funciton with varying population sizes and probabilities
# Roadmap 1: create model with function 1, then feed that and data into function 2 and get output from function 2

# RoadMap 1

from simulations import SimpleSIER

# asks for input of population size
# reduce that to make a model (divide by 500, 1000, etc...)
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