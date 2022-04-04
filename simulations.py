# Roadmap 1
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
# Roadmap 2
import dynetx as dn
import ndlib.models.dynamic as dm

class Simulation():
    def __init__(self, node_number, infection_rate: int = 0.001, removal_rate: int = 0.01, fraction_infected: int = 0.05, time_simulated: int = 365):
        self.node_number = node_number
        self.infection_rate = infection_rate  # beta
        self.removal_rate = removal_rate  # gamma
        self.fraction_infected = fraction_infected
        self.time_simulated = time_simulated

    ## RoadMap 1
    def SimpleSEIR(self, latent_period: int = 0.33):
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
        print(f"Running sim with {self.node_number} nodes for {self.time_simulated} days")

        # Network topology
        g = nx.erdos_renyi_graph(self.node_number, 0.01)  # (n, p) - nodes, probabilty for edge creation

        # Model selection
        model = ep.SEIRModel(g)

        # Model Configuration
        cfg = mc.Configuration()
        cfg.add_model_parameter('beta', self.infection_rate)  # Infection probability, between 0-1
        cfg.add_model_parameter('gamma', self.removal_rate)  # Removal probabilty, between 0-1
        cfg.add_model_parameter('alpha', latent_period)  # Latent period (1/duration), between 0-1
        cfg.add_model_parameter("fraction_infected", self.fraction_infected)
        model.set_initial_status(cfg)

        # Simulation execution
        iterations = model.iteration_bunch(self.time_simulated)

        # Display
        trends = model.build_trends(iterations)

        return model, trends

    def DynamicSIR(self):
        """Simple Dynamic SIR model simulation function. Requires no additional inputs besides beta and gamma entered into Simulation class.

        Returns:
            ndlib.models.dynamic.SIRModel.SIRModel: Type of model used.
            list: list of trends
        """
        print(f"Running Dynamic SIR simulation for {self.time_simulated} days over {self.node_number} nodes...")

        # Dynamic Network topology
        dg = dn.DynGraph()

        # Naive synthetic dynamic graph 
        # At each timestep t a new graph having the same set of node ids is created
        print("Begin creating graph")
        for t in range(0, self.time_simulated):
            g = nx.erdos_renyi_graph(self.node_number, 0.01)
            dg.add_interactions_from(g.edges(), t)
        print("Completed generating graph")

        # Model selection
        model = dm.DynSIRModel(dg)

        # Model Configuration
        config = mc.Configuration()
        config.add_model_parameter('beta', self.infection_rate)
        config.add_model_parameter('gamma', self.removal_rate)
        config.add_model_parameter("fraction_infected", self.fraction_infected)
        model.set_initial_status(config)

        # Simulate snapshot based execution
        print("Begin simulating snapshots")
        iterations = model.execute_snapshots()
        trends = model.build_trends(iterations)
        print("Competed simulating snapshots")

        return model, trends

if __name__ == "__main__":
    from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
    model, trends = Simulation(1000).SimpleSEIR()
    viz = DiffusionTrend(model, trends)
    viz.plot("result_SEIR.pdf")