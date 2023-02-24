from typing import List, Tuple, Dict
import random
from statistics import mean, median, stdev
import pprint
from math import ceil

from transit_network.transit_network import TransitNetwork
from root_logger import RootLogger
from genetic_algorithm.population import Population
from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.fitness_function import evaluate_network, evaluate_network_new
from genetic_algorithm.breeder import breed_networks
from genetic_algorithm.network_metrics import NetworkMetrics
from genetic_algorithm.zone_evaluator import ZoneEvaluator
    
def generate_population(initial_network: TransitNetwork, population_size: int, do_print_metrics: bool = True) -> List[TransitNetwork]:
    RootLogger.log_debug(f'Generating initial population of size {population_size} from {initial_network.id}')

    current_population = [initial_network]
    RootLogger.log_info('Generating Initial Population...')
    babys_to_breed = population_size - 1.0
    for i in range(ceil(babys_to_breed)):

        RootLogger.log_debug(f'Generated {i} of {population_size-1}.')

        # Randomly sample two parents from the current population, and do so until we fill population. 
        [parent_a, parent_b] = random.choices(current_population, k=2)
        
        baby_network = breed_networks(parent_a, parent_b, str(i))

        # Add babies to new population. 
        current_population.append(baby_network)

    if len(current_population) != population_size:
        if len(current_population) == population_size + 1:
            # Remove last generated child network. 
            current_population.pop(-1)
        else:
            RootLogger.log_error(f'Wanted population of size {population_size}, got one of size {len(current_population)}.')


    if do_print_metrics:
        if len(current_population) <= 2:
            RootLogger.log_warning(f'Population size of {len(current_population)} to small to generate metrics.')
        else:
            metrics = generate_metrics(initial_network, current_population)
            RootLogger.log_info(f'Initial Population Metrics: {metrics}')

    RootLogger.log_info('Done Generating Initial Population.')
    return current_population

def generate_metrics(initial_network: TransitNetwork, final_population: List[TransitNetwork]) -> Dict[str, float]:
    RootLogger.log_debug(f"Generating metrics for initial population generator from network {initial_network.id}.")
    original_metric = NetworkMetrics(initial_network)
    all_metrics = []
    fitness_scores = []
    ZE = ZoneEvaluator(initial_network)
    ZE.sample_stops()
    original_fitness = evaluate_network_new(initial_network, original_metric, ZE).fitness

    for other_network in final_population:

        if other_network != initial_network: # Don't want this to skew this data. 
            other_net_metric = NetworkMetrics(other_network)
            similarity_scores = original_metric.similarity(other_net_metric)
            all_metrics.append(similarity_scores)
            other_fitness = evaluate_network_new(other_network, original_metric, ZE).fitness
            fitness_scores.append(other_fitness)
    
    route_similarities = [row[0] for row in all_metrics]
    trip_similarities = [row[1] for row in all_metrics]
    stop_similarities = [row[2] for row in all_metrics]
    fitness_ratios = [f/original_fitness for f in fitness_scores]

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
        'fit_sim_mean': mean(fitness_ratios), 
        'fit_sim_med': median(fitness_ratios),
        'fit_sim_stdev': stdev(fitness_ratios),
    }
    RootLogger.log_debug("Done generating metrics for network population.")
    return metrics

def print_metrics(metrics: Dict[str, float]) -> None:
    pprint.pprint(metrics)

def initiate_population_from_network(network: TransitNetwork, size: int) -> Population:
    initial_networks = generate_population(network, size)
    init_network_metrics = NetworkMetrics(network)
    initial_population = [Chromosome(net) for net in initial_networks]
    ZoneEV = ZoneEvaluator(network)
    return Population(initial_population, init_network_metrics, ZoneEV, evaluate_network_new, breed_networks)
