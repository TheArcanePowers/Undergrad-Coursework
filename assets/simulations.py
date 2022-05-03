# Roadmap 1
import networkx as nx
import ndlib.models.ModelConfig as mc  # noqa: N813
import ndlib.models.epidemics as ep
# Roadmap 2
import dynetx as dn
import ndlib.models.dynamic as dm
# Roadmap 3
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm


class Simulation():
    """Main Simulation class, used for running all simulations by main program."""

    def __init__(self, node_number, infection_rate: int = 0.01, removal_rate: int = 0.01, fraction_infected: int = 0.05, time_simulated: int = 365):
        """Initialize shared variables used by all simulation models.

        Args:
            node_number (int): Number of nodes in Erdos Renyi graph.
            infection_rate (int, optional): Probability of infection when exposed (S->E). Defaults to 0.5.
            removal_rate (int, optional): Probability of nodes removal (E->R). Defaults to 0.01.
            fraction_infected (int, optional): Fraction of initially infected nodes. Defaults to 0.05.
            time_simulated (int, optional): Iterations (days) simulation runs for. Defaults to 365.
        """
        self.node_number = node_number
        self.infection_rate = infection_rate  # beta
        self.removal_rate = removal_rate  # gamma
        self.fraction_infected = fraction_infected
        self.time_simulated = time_simulated

    # RoadMap 1
    def SimpleSEIR(self, latent_period: int = 0.33):
        """SIER model function, requires input of erdos renyi graph's node numbers. Allows for custom rates, defaults are explained in Project Report.

        Args:
            latent_period (int, optional): Period (1/latent_period) before becoming infectious (E->I). Defaults to 0.33.

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
        """Dynamic SIR model simulation function. Requires no additional inputs besides beta and gamma entered into Simulation class.

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

    def CustomVaccineModel(self):
        """Custom simulation model based of SEIR incorporating deaths, incubation periods, and vaccination.

        Returns:
            ndlib.models.CompositeModel.CompositeModel: Type of model used.
            list: list of trends
        """
        # This model has a lot of possibilities (lockdowns, etc., but we'll be focussing on vaccination)
        # Susceptible -> Exposed -> Infectious -> Dead or Recover -> Susceptible (after 3 months)
        # Susceptible -> Vaccinatied -> susceptible (after 3 months)
        ##
        # Susceptible -> Exposed - Edge Stochastic
        # Exposed -> Infectious - Count Down
        # Infectious -> Recover - Count Down
        # Infectious -> Dead - categorical attribute
        # Recovered to Susceptible - Count Down

        # Get original information for variants, and subtract the percentage decreased from vaccination.

        # Network generation
        g = nx.erdos_renyi_graph(self.node_number, 0.01)  # (n, p) - nodes, probabilty for edge creation

        # Composite Model instantiation
        model = gc.CompositeModel(g)

        # Model statuses
        model.add_status("Susceptible")
        model.add_status("Exposed")
        model.add_status("Infected")
        model.add_status("Recovered")
        model.add_status("Dead")
        model.add_status("Vaccinated")

        # Compartment definition
        c1 = cpm.NodeStochastic(self.infection_rate, triggering_status="Infected")  # Susceptible -> Exposed - Node Stochastic
        c2 = cpm.NodeStochastic(0.35)  # 95% probability after 7 iterations # Exposed -> Infectious - Count Down
        c3 = cpm.NodeStochastic(0.2)  # 95% after 14 iterations)  # Infectious -> Recover - Count Down
        c4 = cpm.NodeStochastic(self.removal_rate)  # Infectious -> Dead - Node Stochastic
        c5 = cpm.CountDown("susceptibility", iterations=84)  # Recovered, Vaccinated -> Susceptible - Count Down
        c6 = cpm.NodeStochastic(0.001)  # Susceptible -> Vaccinated - Node Stochastic

        # Rule definition
        model.add_rule("Susceptible", "Exposed", c1)
        model.add_rule("Exposed", "Infected", c2)
        model.add_rule("Infected", "Recovered", c3)
        model.add_rule("Infected", "Dead", c4)
        model.add_rule("Recovered", "Susceptible", c5)
        model.add_rule("Vaccinated", "Susceptible", c5)
        model.add_rule("Susceptible", "Vaccinated", c6)

        # Model initial status configuration
        config = mc.Configuration()
        config.add_model_parameter('fraction_infected', self.fraction_infected)

        # Simulation execution
        model.set_initial_status(config)
        iterations = model.iteration_bunch(self.time_simulated)

        # Display
        trends = model.build_trends(iterations)

        return model, trends


# for debugging
if __name__ == "__main__":
    from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
    model, trends = Simulation(node_number=1000, time_simulated=40).CustomVaccineModel()
    print(type(model))
    viz = DiffusionTrend(model, trends)
    viz.plot("new_results.pdf")
