from modules.simulation import Simulation
import networkx as nx
import functools
import random
import numpy as np


class MobileNetworkSimulation(Simulation):
    def __init__(self, id, network_size=45, seed=random.randint(1, 10)):
        self.pop_depth = 4
        super().__init__(id, network_size, seed)
        # self._node_classify()

    def _node_classify(self):
        """
        Classifies nodes as the following types:
            RAN - Base Station in the RAN (can be a C-RAN, etc)
            Core - Core network
            TODO -> PoP - Point of Presence (PoP - provider) (compute resource for VNFs)
                    --> 5 hop neighbor (K-th order neighbor [from Core nodes]. K = 5)
            NET - Network Device (e.g., router, switch, border gateway) [Transport Network]
        """
        node_data = self.network.G.nodes(data=True)
        bs_list = [tuple[0] for tuple in self.network.G.degree() if tuple[1] == 1]
        # not degree three anymore...
        # TODO: Find a logic to identify Core nodes
        #       - Graph might not have any node with degree >= 4 ...
        #         - Just call refresh (but careful... it might increase execution time)

        centralities = np.array(
            list({j for _, j in nx.katz_centrality(self.network.G).items()})
        )
        centralities.sort()
        node_centrality = nx.katz_centrality(self.network.G)

        # The node with the max centrality score is selected as "core node".
        # --> Maybe create a TOP 5 "core nodes" (?)
        # max_centrality_degree = functools.reduce(
        #    lambda a, b: a if a > b else b, centralities
        # )
        # @FIXME -> Fixed 5 top centralities... Should change based on the number of the network size
        top_centralities = (centralities[::-1])[0:5]
        max_centrality_nodes = list(
            filter(lambda i: node_centrality[i] in top_centralities, node_centrality)
        )

        print("Got ", len(max_centrality_nodes), " possible core nodes! \n")

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

        pop_nodes = []
        for core_node in self.core_nodes:
            pop_candidates = nx.single_source_shortest_path_length(
                self.network.G, core_node, cutoff=self.pop_depth
            )
            # N-th (self.pop_depth-th) order neighbor from a core node
            pop_candidates = list(
                filter(
                    lambda el: el[1] == self.pop_depth
                    and self.network.G.nodes[el[0]]["type"] == "NET",
                    list(pop_candidates.items()),
                )
            )
            pop_candidates = [tuple[0] for tuple in pop_candidates]
            pop_nodes += pop_candidates
            # pop_candidates = [
            #     tuple[0]
            #     for tuple in list(
            #         filter(lambda el: el[1] == self.pop_depth, list(pop_candidates.items()))
            #     )
            # ]

            # pop_nodes += list(
            #     filter(
            #         lambda candidate: self.network.G.nodes[candidate]["type"] == "NET",
            #         pop_candidates,
            #     )
            # )
        for pop_node in set(pop_nodes):
            node_data[pop_node]["type"] = "PoP"

        self.net_nodes = [tuple[0] for tuple in node_data if tuple[1]["type"] == "NET"]
        self.pop_nodes = [tuple[0] for tuple in node_data if tuple[1]["type"] == "PoP"]

        # max centrality degree --> small number of nodes!
        # should work with closeness... https://en.wikipedia.org/wiki/Centrality
        # closeness leads to the same problem... back to degree with a top 5, maybe?
        if len(self.core_nodes) == 0:
            print("No Core node found. Refreshing with new seed...")
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
