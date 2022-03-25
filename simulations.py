import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend


def SimpleSIER(node_number: int, recovery_rate: int = 0.01, infection_rate: int = 0.005, recovery_time: int = 0.05, fraction_infected: int = 0.05, time_simulated: int = 365):

    # Network topology
    g = nx.erdos_renyi_graph(node_number, 0.1)  # (n, p) - nodes, probabilty for edge creation

    # Model selection
    model = ep.SEIRModel(g)

    # Model Configuration
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', recovery_rate)  # Recovery rate, between 0-1
    cfg.add_model_parameter('gamma', infection_rate)  # Infection rate, between 0-1
    cfg.add_model_parameter('alpha', recovery_time)  # Recovery time (1/alpha), between 0-1 
    cfg.add_model_parameter("fraction_infected", fraction_infected)
    model.set_initial_status(cfg)

    # Simulation execution
    iterations = model.iteration_bunch(time_simulated)

    # Display
    trends = model.build_trends(iterations)

    return DiffusionTrend(model, trends)

viz = SimpleSIER(365)
viz.plot("diffusion1.pdf")