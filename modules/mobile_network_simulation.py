from modules.simulation import Simulation
import random


class MobileNetworkSimulation(Simulation):
    def __init__(self, id, network_size=45, seed=random.randint(1, 10)):
        super().__init__(id, network_size, seed)
        # self._node_classify()

    def _node_classify(self):
        """
        Classifies nodes as the following types:
            RAN - Base Station in the RAN (can be a C-RAN, etc)
            Core - Point of Presence (PoP - provider)
            NET - Network Device (e.g., router, switch, border gateway) [Transport Network]
        """
        node_data = self.network.G.nodes(data=True)
        bs_list = [tuple[0] for tuple in self.network.G.degree() if tuple[1] == 1]
        dg_three = [tuple[0] for tuple in self.network.G.degree() if tuple[1] >= 3]
        for node in bs_list:
            node_data[node]["type"] = "RAN"
        for node in dg_three:
            if any(ran in self.network.G.adj[node] for ran in bs_list):
                node_data[node]["type"] = "NET"
            else:
                node_data[node]["type"] = "Core"
        empty_type = [tuple[0] for tuple in node_data if tuple[1]["type"] == ""]
        for node in empty_type:
            node_data[node]["type"] = "NET"


#        for node in self.network.G.nodes(data=True) if node["type"] == "":
#            node["type"] = "NET"


# Para cada node type BS, adicionar um nó "edge"
# para cada node type PoP, adicionar uma fat tree
