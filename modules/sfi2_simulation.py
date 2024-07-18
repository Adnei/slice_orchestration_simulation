from modules.simulation import Simulation
import random


class SFISimulation(Simulation):
    def __init__(self, id, network_size=45, seed=random.randint(1, 10)):
        super().__init__(id, network_size, seed)

    def _node_classify(self):
        """
        Classifies nodes as the following types:
            BS - Base Station in the RAN
            PoP - Point of Presence (provider)
            NET - Network Device (e.g., router, switch)
        """
        print("TODO!! SFI2 Simulation")
        return
