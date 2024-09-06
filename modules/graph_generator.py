import random
from itertools import combinations, groupby, count
import networkx as nx
from matplotlib import pyplot as plt


# @TODO: Should deal with a list of Node and Edge attributes
class GraphGenerator:
    def __init__(self, size, seed):
        self.size = size
        self.seed = seed
        self.probability = 0.001
        self.G = self._random_connected_graph()

    # based on https://stackoverflow.com/questions/61958360/how-to-create-random-graph-where-each-node-has-at-least-1-edge-using-networkx
    # Be careful with super and hyper connected graphs!!!
    #   --> Super- and hyper-connectivity
    #   --> https://en.wikipedia.org/wiki/Connectivity_(graph_theory)
    def _random_connected_graph(self):
        """
        Generates a random undirected graph, similarly to an Erdős-Rényi
        graph, but enforcing that the resulting graph is conneted
        """
        edges = combinations(range(self.size), 2)
        G = nx.Graph()
        G.add_nodes_from(range(self.size), type="")
        if self.probability <= 0:
            return G
        if self.probability >= 1:
            return nx.complete_graph(self.size, create_using=G)
        for _, node_edges in groupby(edges, key=lambda x: x[0]):
            node_edges = list(node_edges)
            random_edge = random.choice(node_edges)
            G.add_edge(*random_edge, weight=0.5)
            for e in node_edges:
                if random.random() < self.probability:
                    G.add_edge(*e, weight=0.9)
        return G

    # @FIXME --> This is a mess D:
    def draw(self, file="", show=True):
        """
        Draws the graph with colors based on node type
        """
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.G, seed=self.seed)
        weight_label = nx.get_edge_attributes(self.G, "weight")
        groups = set(nx.get_node_attributes(self.G, "type").values())
        mapping = dict(zip(sorted(groups), count()))
        nodes = self.G.nodes()
        colors = [mapping[self.G.nodes[n]["type"]] for n in nodes]
        # node_labels = nx.get_node_attributes(self.G, "type")
        draw_edges = nx.draw_networkx_edges(self.G, pos, alpha=1)
        draw_nodes = nx.draw_networkx_nodes(
            self.G,
            pos,
            nodelist=nodes,
            node_color=colors,
            node_size=500,
            cmap=plt.cm.jet,
        )
        draw_edge_labels = nx.draw_networkx_edge_labels(
            self.G, pos=pos, edge_labels=weight_label
        )
        draw_node_labels = nx.draw_networkx_labels(self.G, pos, font_color="white")
        colorbar = plt.colorbar(draw_nodes)
        # @FIXME --> static labels... Gotta fix it
        colorbar.set_ticklabels(["Core", "", "", "", "NET", "", "", "", "RAN"])
        # colorbar.set_ticklabels(["RAN", "NET", "Core"])
        plt.axis("off")
        # plt.legend(scatterpoints=1)
        # @TODO: File export!!
        if show:
            plt.show()
