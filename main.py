from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from assets.simulations import Simulation
from assets.vaccination_data import Omicron_vaccine_data, Normal_vaccine_data, Delta_vaccine_data
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
import os

# Fix script working dir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print("  _________.__              .__          __                \n\
 /   _____/|__| _____  __ __|  | _____ _/  |_  ___________ \n\
 \\_____  \\ |  |/     \\|  |  \\  | \\__  \\   _ _\\/  _ \\_  __ \\ \n\
 /        \\|  |  Y Y  \\  |  /  |__/ __ \\|  | (  <_> )  | \\/ \n\
/_______  /|__|__|_|  /____/|____(____  /__|  \\____/|__|   \n\
        \\/          \\/                \\/                   ")

def choose_vaccine():
    while True:
        print()
        print(list(vaccine_data.keys()))
        vaccine_choice = input("Please choose what vaccine you would like to tackle the chosen variant (case-sensitive): ")
        if vaccine_choice in vaccine_data.keys():
            return vaccine_choice
        else:
            print("Error: Please choose a correct vaccine listed.")

# Asks for input of population size
while True:
    try:
        population_size = int(input("Please enter a population size you would like to sample: "))
        if population_size > 68000000 or population_size < 1:
            print("Error: Please use values between 1 and Uk Population of 68 million.")
        else:
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
    reduction_by = 1

elif population_size >= 10000 and population_size < 100000:
    reduction = population_size // 10
    reduction_by = 10*1

elif population_size >= 100000 and population_size < 1000000:
    reduction = population_size // 10**2
    reduction_by = 10**2

elif population_size >= 1000000 and population_size < 10000000:
    reduction = population_size // 10**3
    reduction_by = 10**3

elif population_size >= 10000000 and population_size <= 10000000:  # Should not exceed 68m (Uk population).
    reduction = population_size // 10**4
    reduction_by = 10**4

while True:
    try:
        fraction_infected = float(input("\nWhat percentage of the chosen population do you want to start as infected? (0-1, >0.1 recommended): "))
        if fraction_infected > 1:
            print("Error: Please choose a percentage value between 0-1.")
        else:
            break
    except ValueError:
        print("Error: Please enter a number only.")


while True:
    try:
        days = int(input("\nHow many days do you want to simulate for? (1-180 recommended): "))
        break
    except ValueError:
        print("Error: Please enter a number only.")


# Variant option for different infection and removal rates.
while True:
    variant_choice = input("\nPlease choose what variant you would like to simulate: (N) for Normal/Pre-Alpha Variant, (D) for Delta or (O) for Omicron: ").upper()
    if variant_choice in ("N", "D", "O"):
        break
    else:
        print("Error: Please pick one of the variant options only.")

# TODO: Add to Project Report
if variant_choice == "N":
    infection_rate = 0.08
    removal_rate = 0.01
    vaccine_data = Normal_vaccine_data
elif variant_choice == "D":
    infection_rate = 0.11
    removal_rate = 0.001
    vaccine_data = Delta_vaccine_data
elif variant_choice == "O":
    infection_rate = 0.3
    removal_rate = 0.02
    vaccine_data = Omicron_vaccine_data

# Simulation
while True:
    model_choice = input("\nFinally, what model would you like to use to display the data: (S) for Simple Seir, (D) for Dynamic SIR (VERY long runtime), or (C) for Custom Model: ").strip().upper()
    if model_choice in {"S", "D", "C"}:
        break
    else:
        print("Error: Please choose only the three options listed.")

Sim = Simulation(node_number=reduction, infection_rate=infection_rate, removal_rate=removal_rate, fraction_infected=fraction_infected, time_simulated=days)
if model_choice == "S":
    latent_days = float(input("Latent period (in days): ").strip())
    latent_period = 1/latent_days  # Since latent period is = 1/latent_input
    model, trends = Sim.SimpleSEIR(latent_period=latent_period)

elif model_choice == "D":
    model, trends = Sim.DynamicSIR()

elif model_choice == "C":
    vaccine_choice = choose_vaccine()
    infection_rate
    vaccination_rate = float(input("Vaccination rate (0-1, recommend >0.2): ").strip())
    # vaccine data set is percentage decrease of infection with vaccine. E.g Astazeneca on Ancestral has a reduction of 60% infection rate, 90% death rate.
    # TODO: Add death rate to this to show vaccine's impact on reducing deaths
    model, trends = Sim.CustomVaccineModel(vaccination_rate=vaccination_rate, vaccination_infection_rate=infection_rate*vaccine_data[vaccine_choice])


# Diplay results
viz = DiffusionTrend(model, trends)
viz.plot("output")

values = {
    "S": ["Susceptible", "Exposed", "Infected", "Recovered"],
    "D": ["Susceptible", "Infected", "Recovered"],
    "C": ["Susceptible", "Exposed", "Infected", "Recovered", "Dead", "Vaccinated"]
}
print()
print(f"### Final values after {days} days simulated: ###")
for i in trends[0]["trends"]["node_count"]:
    print(values[model_choice][i], ":", trends[0]["trends"]["node_count"][i][-1]*reduction_by)

try:
    print("Opening output image...")
    os.startfile("output.png")
except:
    print("Error in opening output file. Please find manually")


# Model comparison
# TODO: Could extend this to run simulations with different inputs (different variants)
if input("\nRun Model comparison? (y/n): ").strip().lower() == "y":
    if model_choice == "S":
        vaccine_choice = choose_vaccine()
        vaccination_rate = float(input("Vaccination rate: ").strip())
        model1, trends1 = Sim.CustomVaccineModel(vaccination_rate=vaccination_rate, vaccination_infection_rate=infection_rate*vaccine_data[vaccine_choice])  # Custom Model
        comparison_model_choice = "C"
    else:  # model_choice being custom or dyamic
        model1, trends1 = Sim.SimpleSEIR()  # Simple Seir
        comparison_model_choice = "s"

viz2 = DiffusionTrend(model1, trends1)
viz2.plot("output_2")
comparative_viz = DiffusionTrendComparison([model, model1], [trends, trends1], ["Susceptible","Infected", "Recovered"])
comparative_viz.plot("comparative_output")
try:
    print("Opening output images...")
    os.startfile("comparative_output.png")
    os.startfile("output_2.png")
except:
    print("Error in opening output file. Please find manually")

print()
print("### Comparative model output###")
for i in trends1[0]["trends"]["node_count"]:
    print(values[comparison_model_choice][i], ":", trends1[0]["trends"]["node_count"][i][-1]*reduction_by)
