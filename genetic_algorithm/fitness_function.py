from transit_network.transit_network import TransitNetwork
import genetic_algorithm.params as params

def evaluate_network(net: TransitNetwork) -> float:
    # Need to scale these. 
    ridership_val = (net.ridership / params.ORIGINAL_RIDERSHIP) * params.RIDERSHIP_LAMBDA
    routes_val = (len(net.routes) / params.ORIGINAL_ROUTES) * params.NUM_ROUTES_LAMBDA
    coverage_val = (net.coverage / params.ORIGINAL_COVERAGE) * params.COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / params.ORIGINAL_RIDERSHIP_DENSITY) * params.RIDERSHIP_DENSITY_LAMBDA
    
    return ridership_val + routes_val + coverage_val + ridership_density_val

def evaluate_network_new(net: TransitNetwork):

    pass   