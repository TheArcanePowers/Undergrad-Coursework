import datetime
import networkx as nx

timings = {}
for i in (10**i for i in range(1,4)):
    for j in range(1,10,2):
        start_time = datetime.datetime.now()
        nx.erdos_renyi_graph(i*j, 0.1)
        timings[i*j] = datetime.datetime.now() - start_time

print(timings)