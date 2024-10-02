from modules.graph_generator import GraphGenerator
import abc
import random


class Simulation:
    __metaclass__ = abc.ABCMeta

    def __init__(self, id, network_size=45, seed=random.randint(1, 10)):
        self.core_nodes = None
        self.ran_nodes = None
        self.net_nodes = None
        self.pop_nodes = None
        self.id = id
        self.refresh(network_size, seed)

    @abc.abstractmethod
    def _node_classify(self):
        return

    def refresh(self, network_size=45, seed=random.randint(1, 10)):
        self.seed = seed
        self.network_size = network_size
        self.network = GraphGenerator(self.network_size, self.seed)
        self._node_classify()
