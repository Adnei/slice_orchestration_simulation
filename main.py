from modules.mobile_network_simulation import MobileNetworkSimulation
from modules.sfi2_simulation import SFISimulation


def main():
    fiveg_simulation = MobileNetworkSimulation("5G Simulation", network_size=50)
    fiveg_simulation.network.draw()


#    sfi2_simulation = SFISimulation("SFI2 Simulation", network_size=10)
#    sfi2_simulation.network.draw()


if __name__ == "__main__":
    main()
