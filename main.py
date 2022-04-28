from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from simulations import Simulation
from vaccination_data import omicron_vaccine_data


# asks for input of population size
while True:
    try:
        population_size = int(input("Please enter a population size you would like to sample: "))
        break
    except ValueError:
        print("Please enter only a number for the population size")


# reduce that to make a model (divide by 500, 1000, etc...)
if population_size >= 1 and population_size < 10:
    reduction = population_size * 10**3
    reduction_by = 10**3

elif population_size >= 10 and population_size < 100:
    reduction = population_size * 10**2
    reduction_by = 10 // 10**2

elif population_size >= 100 and population_size < 1000:
    reduction = population_size * 10
    reduction_by = 10 // 10

elif population_size >= 1000 and population_size < 10000:
    reduction = population_size * 1

elif population_size >= 10000 and population_size < 100000:
    reduction = population_size // 10
    reduction_by = 10*1

elif population_size >= 100000 and population_size < 1000000:
    reduction = population_size // 10**2
    reduction_by = 10**2

elif population_size >= 1000000 and population_size < 10000000:
    reduction = population_size // 10**3
    reduction_by = 10**3

elif population_size >= 10000000 and population_size <= 68000000:  # should not exceed 68m is Uk population
    reduction = population_size // 10**4
    reduction_by = 10**4
else:
    if population_size > 68000000:
        print("Please do not exceed the Uk Population of 68 million.")


while True:
    try:
        days = int(input("How many days do you want to simulate for?"))
        break
    except ValueError:
        print("Please enter a number only")


# variant option for different infection and removal rates
while True:
    variant_choice = input("Please choose what variant you would like to simulate: (N) for Normal; Pre-Alpha Variant, (D) for Delta or (O) for Omicron")
    if variant_choice in ("N", "D", "O"):
        break
    else:
        print("Error: Please pick one of the variant options only")

if variant_choice == "N":
    infection_rate = 0.08
    removal_rate = 0.01
elif variant_choice == "D":
    infection_rate = 0.11
    removal_rate = 0.001
elif variant_choice == "O":
    infection_rate = 0.3
    removal_rate = 0.02


while True:
    print(list(omicron_vaccine_data.keys()))
    vaccine_choice = input("Please choose what vaccine you would like to tackle the chosen variant")
    if vaccine_choice in omicron_vaccine_data.keys():
        break
    else:
        print("Please choose a correct vaccine")


# diplay results
model, trends = Simulation(reduction, infection_rate, removal_rate, time_simulated=days).SimpleSEIR()
viz = DiffusionTrend(model, trends)
viz.plot()

####################################################
# What's left?
# Model Comparison https://ndlib.readthedocs.io/en/latest/reference/viz/mpl/TrendComparison.html
