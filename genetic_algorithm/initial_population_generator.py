from typing import List
from random import choices

from transit_network.transit_network import TransitNetwork
from root_logger import RootLogger
from genetic_algorithm.breeder import breed_networks

def generate_population(initial_network: TransitNetwork, population_size: int) -> List[TransitNetwork]:
    RootLogger.log_debug(f'Generating initial population of size {population_size} from {initial_network.id}')

    current_population = [initial_network]
    for i in range(population_size-1):
        # Randomly sample two parents from the current population, and do so until we fill population. 
        [parent_a, parent_b] = choices(current_population, k=2)
        baby_network = breed_networks(parent_a, parent_b, i)
        current_population.append(baby_network)
    
    return current_population

