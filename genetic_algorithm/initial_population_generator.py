from typing import List, Tuple, Dict
from random import choices
from statistics import mean, median, stdev
import pprint

from transit_network.transit_network import TransitNetwork
from root_logger import RootLogger
from genetic_algorithm.breeder import breed_networks

class NetworkMetrics:
    def __init__(self, network: TransitNetwork):
        self.network_id = network.id
        self.route_ids = [r.id for r in network.routes]
        self.trip_ids = [t.id for t in network.trips]
        self.stop_ids = [s.id for s in network.stops]
    
    def similarity(self, other) -> Tuple[float, float, float]:
        if self.network_id == other.network_id:
            RootLogger.log_warning('Comparing Networks with identical ids.')

        routes_similarity = (len(set(self.route_ids) & set(other.route_ids)) * 2.0) / (len(self.route_ids) + len(other.route_ids))
        trips_similarity = (len(set(self.trip_ids) & set(other.trip_ids)) * 2.0) / (len(self.trip_ids) + len(other.trip_ids))
        stops_similarity = (len(set(self.stop_ids) & set(other.stop_ids)) * 2.0) / (len(self.stop_ids) + len(other.stop_ids))

        return routes_similarity, trips_similarity, stops_similarity

def generate_population(initial_network: TransitNetwork, population_size: int, do_print_metrics: bool = True) -> List[TransitNetwork]:
    RootLogger.log_debug(f'Generating initial population of size {population_size} from {initial_network.id}')

    current_population = [initial_network]
    RootLogger.log_info('Generating Initial Population...')
    babys_to_breed = population_size - 1.0
    for i in range(int(babys_to_breed/2.0)):
        RootLogger.log_debug(f'Generated {2*i} of {population_size-1}.')

        # Randomly sample two parents from the current population, and do so until we fill population. 
        [parent_a, parent_b] = choices(current_population, k=2)
        baby_network_A, baby_network_B = breed_networks(parent_a, parent_b, str(i))
        # Add babies to new population. 
        current_population.append(baby_network_A)
        current_population.append(baby_network_B)

    if do_print_metrics:
        print_metrics(generate_metrics(initial_network, current_population))
    RootLogger.log_info('Done Generating Initial Population.')
    
    return current_population

def generate_metrics(initial_network: TransitNetwork, final_population: List[TransitNetwork]) -> Dict[str, float]:
    RootLogger.log_debug(f"Generating metrics for initial population generator from network {initial_network.id}.")
    original_metric = NetworkMetrics(initial_network)
    all_metrics = []

    for other_network in final_population:
        if other_network != initial_network: # Don't want this to skew this data. 
            other_net_metric = NetworkMetrics(other_network)
            similarity_scores = original_metric.similarity(other_net_metric)
            all_metrics.append(similarity_scores)
    
    route_similarities = [row[0] for row in all_metrics]
    trip_similarities = [row[1] for row in all_metrics]
    stop_similarities = [row[2] for row in all_metrics]

    metrics = {
        'r_sim_mean': mean(route_similarities), 
        'r_sim_med': median(route_similarities),
        'r_sim_stdev': stdev(route_similarities),
        't_sim_mean': mean(trip_similarities), 
        't_sim_med': median(trip_similarities),
        't_sim_stdev': stdev(trip_similarities),
        's_sim_mean': mean(stop_similarities), 
        's_sim_med': median(stop_similarities),
        's_sim_stdev': stdev(stop_similarities), 
    }
    RootLogger.log_debug("Done generating metrics for network population.")
    return metrics

def print_metrics(metrics: Dict[str, float]) -> None:
    pprint.pprint(metrics)

