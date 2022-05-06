# EMAT10006
Assignment for Further Computer Programming

Simulation library (assets/simulations.py) offers: Static SEIR, Dynamic SIR, Static Custom COVID model, which can then be called to compare and model a vast variety of models.

main.py is an interactive script that showcases and runs COVID simulations with real-life data on spread and death rate, as well as allowing the user to compare the output of two different models with the same input.

main.py plots and outputs images of simulation with given parameters, as well as printing final state output (numbers of Infected, Dead, etc.). This can then be compared with another model running the same parameters.


## Installation

Clone the repo, install requirements, and main.py is ready for use!

```bash
git clone https://github.com/TheArcanePowers/EMAT10006
```

Install requirements
```bash
pip install -r requirements.txt
```

## Usage

main.py is ready for use right out the box! Script will run on interactive mode, where it will determine the arguments to run simulations for.

```bash
python3 main.py
```
