from modules.simulation import Simulation
import networkx as nx
import functools
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
        # not degree three anymore...
        # TODO: Find a logic to identify Core nodes
        #       - Graph might not have any node with degree >= 4 ...
        #         - Just call refresh (but careful... it might increase execution time)

        centralities = list(
            {j for _, j in nx.degree_centrality(self.network.G).items()}
        )
        node_centrality = nx.degree_centrality(self.network.G)
        max_centrality_degree = functools.reduce(
            lambda a, b: a if a > b else b, centralities
        )
        max_centrality_nodes = list(
            filter(
                lambda i: node_centrality[i] == max_centrality_degree, node_centrality
            )
        )

        for node in bs_list:
            node_data[node]["type"] = "RAN"
        for node in max_centrality_nodes:
            if any(ran in self.network.G.adj[node] for ran in bs_list):
                node_data[node]["type"] = "NET"
            else:
                node_data[node]["type"] = "Core"
        empty_type = [tuple[0] for tuple in node_data if tuple[1]["type"] == ""]
        for node in empty_type:
            node_data[node]["type"] = "NET"

        self.ran_nodes = [tuple[0] for tuple in node_data if tuple[1]["type"] == "RAN"]
        self.core_nodes = [
            tuple[0] for tuple in node_data if tuple[1]["type"] == "Core"
        ]
        self.net_nodes = [tuple[0] for tuple in node_data if tuple[1]["type"] == "NET"]

        # max centrality degree --> small number of nodes!
        # should work with closeness... https://en.wikipedia.org/wiki/Centrality
        if len(self.core_nodes) == 0:
            print("No node with degree >= 4. Refreshing")
            self.refresh(self.network_size)
            return

        # if len(self.core_nodes) <= 3 ... add more manually ? --> add one more with dg 3?

    def start(self, seed=random.randint(1, 10)):
        return
        # @TODO -> Create UE (User Equipment) and associate it to a random RAN-BS.
        #       -> We must provide VNFs hosted in Core nodes... which Core node is better? avoid energy wastes...


#        for node in self.network.G.nodes(data=True) if node["type"] == "":
#            node["type"] = "NET"


# Para cada node type BS, adicionar um nó "edge"
# para cada node type PoP, adicionar uma fat tree
