from typing import List
from transit_network.transit_network import TransitNetwork

class Population:

    max_iteration = 100 
    mutation_rate = 0.1

    def __init__(self, networks: List[TransitNetwork]):
        self.population = networks
        self.population_size = len(networks)
        self.iteration_number = 1
    
    
        