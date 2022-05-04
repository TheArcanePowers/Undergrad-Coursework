#%%
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from assets.simulations import Simulation
from assets.vaccination_data import omicron_vaccine_data
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison

# Asks for input of population size
while True:
    try:
        population_size = int(input("Please enter a population size you would like to sample: "))
        break
    except ValueError:
        print("Error: Please enter only a number for the population size.")


# Reduce that to make a model (divide by 500, 1000, etc...)
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

elif population_size >= 10000000 and population_size <= 68000000:  # Should not exceed 68m (Uk population).
    reduction = population_size // 10**4
    reduction_by = 10**4
else:
    if population_size > 68000000:
        print("Error: Please do not exceed the Uk Population of 68 million.")

while True:
    try:
        fraction_infected= float(input("What percentage of the chosen population do you want to start as infected?"))
        if fraction_infected > 1:
            print("Error: Please choose a percentage value between 0-1")
        else:
            break
    except ValueError:
        print("Error: Please enter a number only")
    



while True:
    try:
        days = int(input("How many days do you want to simulate for?"))
        break
    except ValueError:
        print("Error: Please enter a number only.")


# Variant option for different infection and removal rates.
while True:
    variant_choice = input("Please choose what variant you would like to simulate: (N) for Normal; Pre-Alpha Variant, (D) for Delta or (O) for Omicron.")
    if variant_choice in ("N", "D", "O"):
        break
    else:
        print("Error: Please pick one of the variant options only.")

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
    vaccine_choice = input("Please choose what vaccine you would like to tackle the chosen variant: ")
    if vaccine_choice in omicron_vaccine_data.keys():
        break
    else:
        print("Error: Please choose a correct vaccine listed.")

Sim = Simulation(node_number=reduction,infection_rate=infection_rate, removal_rate=removal_rate, fraction_infected= fraction_infected, time_simulated=days)

while True:
    model_choice= input("Finally, what model would you like to use to display the data: (S) for Simple Seir or (C) for Custom Model")
    if model_choice in ("S", "C"):
        break
    else:
        print("Error: Please choose only the two options listed.")
if model_choice == "S":
    model, trends = Sim.SimpleSEIR()
elif model_choice == "C":
    vaccination_rate = input("Vaccination rate: ")
    model, trends = Sim.CustomVaccineModel(vaccination_rate=vaccination_rate)


# Diplay results
viz = DiffusionTrend(model, trends)
viz.plot("GRAPH OUT")
print(trends[0]["trends"]["node_count"])
for i in trends[0]["trends"]["node_count"]:
   print("Value:", trends[0]["trends"]["node_count"][i][-1])


# Model comparison
model, trends = Sim.SimpleSEIR() # Simple Seir
vaccination_rate = input("Vaccination rate: ")
model1, trends1 = Sim.CustomVaccineModel(vaccination_rate=vaccination_rate) # Custom Model





####################################################
# What's left?
# Model Comparison https://ndlib.readthedocs.io/en/latest/reference/viz/mpl/TrendComparison.html

# %%
