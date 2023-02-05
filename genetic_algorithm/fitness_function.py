from transit_network.transit_network import TransitNetwork
import genetic_algorithm.params as params
from genetic_algorithm.network_metrics import NetworkMetrics

def evaluate_network(net: TransitNetwork, initial_metrics: NetworkMetrics) -> float:
    # Need to scale these. 
    ridership_val = (net.ridership / initial_metrics.ridership) * params.RIDERSHIP_LAMBDA
    routes_val = (len(net.routes) / initial_metrics.num_routes) * params.NUM_ROUTES_LAMBDA
    coverage_val = (net.coverage / initial_metrics.coverage) * params.COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / initial_metrics.ridership_density_score) * params.RIDERSHIP_DENSITY_LAMBDA
    
    return (ridership_val + routes_val + coverage_val + ridership_density_val)/(params.sum_of_fitness_coefficients())

def evaluate_network_new(net: TransitNetwork):

    pass   