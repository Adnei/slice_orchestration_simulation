from modules.simulation import Simulation
import random


class MobileNetworkSimulation(Simulation):
    def __init__(self, id, network_size=45, seed=random.randint(1, 10)):
        super().__init__(id, network_size, seed)
        # self._node_classify()

    def _node_classify(self):
        """
        Classifies nodes as the following types:
            BS - Base Station in the RAN
            PoP - Point of Presence (provider)
            NET - Network Device (e.g., router, switch)
        """
        bs_list = [tuple[0] for tuple in self.network.G.degree() if tuple[1] == 1]
        for node in bs_list:
            self.network.G.nodes(data=True)[node]["type"] = "BS"
