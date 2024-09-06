from modules.mobile_network_simulation import MobileNetworkSimulation
from modules.sfi2_simulation import SFISimulation


fiveg_simulation = MobileNetworkSimulation("5G Simulation", network_size=80)
fiveg_simulation.network.draw()

# Defaults to dijkstra
# [p for p in nx.all_shortest_paths(fiveg_simulation.network.G, source=4, target=49)]

#    sfi2_simulation = SFISimulation("SFI2 Simulation", network_size=10)
#    sfi2_simulation.network.draw()
