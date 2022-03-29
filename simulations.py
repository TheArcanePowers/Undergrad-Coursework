# Roadmap 1
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
# Roadmap 2
import dynetx as dn
import ndlib.models.dynamic as dm

class Simulation():
    def __init__(self):
        pass

    ## RoadMap 1
    def SimpleSEIR(self, node_number: int, removal_rate: int = 0.05, infection_rate: int = 0.9, latent_period: int = 0.33, fraction_infected: int = 0.05, time_simulated: int = 365):
        """Simple SIER model function, requires input of erdos renyi graph's node numbers. Allows for custom rates, defaults are explained in Project Report.

        Args:
            node_number (int): Number of nodes in Erdos Renyi graph
            removal_rate (int, optional): Probability of nodes removal (E->R). Defaults to 0.05.
            infection_rate (int, optional): Probability of infection when exposed (S->E). Defaults to 0.9.
            latent_period (int, optional): Period (1/latent_period) before becoming infectious (E->I). Defaults to 0.33.
            fraction_infected (int, optional): Fraction of initially infected nodes. Defaults to 0.05.
            time_simulated (int, optional): Iterations (days) simulation runs for. Defaults to 365.

        Returns:
            ndlib.models.epidemics.SEIRModel.SEIRModel: Type of model used.
            list: list of trends

        """

        # Network topology
        g = nx.erdos_renyi_graph(node_number, 0.003)  # (n, p) - nodes, probabilty for edge creation

        # Model selection
        model = ep.SEIRModel(g)

        # Model Configuration
        cfg = mc.Configuration()
        cfg.add_model_parameter('beta', infection_rate)  # Infection probability, between 0-1
        cfg.add_model_parameter('gamma', removal_rate)  # Removal probabilty, between 0-1
        cfg.add_model_parameter('alpha', latent_period)  # Latent period (1/duration), between 0-1
        cfg.add_model_parameter("fraction_infected", fraction_infected)
        model.set_initial_status(cfg)

        # Simulation execution
        iterations = model.iteration_bunch(time_simulated)

        # Display
        trends = model.build_trends(iterations)

        return model, trends

    def DynamicSIR():
        # Dynamic Network topology
        dg = dn.DynGraph()

        # for i in ...

        # Model selection
        model = dm.DynSIRModel(dg)

        # Model Configuration
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.01)
        config.add_model_parameter('gamma', 0.01)
        config.add_model_parameter("fraction_infected", 0.1)
        model.set_initial_status(config)

        return