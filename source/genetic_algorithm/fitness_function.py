from transit_network.transit_network import TransitNetwork
import genetic_algorithm.params as params
from genetic_algorithm.network_metrics import NetworkMetrics
from genetic_algorithm.zone_evaluator import ZoneEvaluator

class Fitness:

    def __init__(self, zone_val: float, ridership_val: float, routes_val: float, coverage_val: float, ridership_density_val: float, fitness: float):
        self.ridership_val = ridership_val / (params.sum_of_fitness_coefficients())
        self.routes_val = routes_val / (params.sum_of_fitness_coefficients())
        self.coverage_val = coverage_val / (params.sum_of_fitness_coefficients())
        self.ridership_density_val = ridership_density_val / (params.sum_of_fitness_coefficients())
        self.zone_val = zone_val / (params.sum_of_fitness_coefficients())
        self.fitness = fitness
    
    def to_dict(self):
        return {
            'ridership_val': self.ridership_val, 
            'routes_val': self.routes_val, 
            'coverage_val': self.coverage_val, 
            'ridership_density_val': self.ridership_density_val, 
            'zone': self.zone_val,
            'fitness': self.fitness
        }
    
    def get_metrics_list(self):
        return list(self.to_dict().keys())

def evaluate_network(net: TransitNetwork, initial_metrics: NetworkMetrics) -> float:
    ridership_val = (net.ridership / initial_metrics.ridership) * params.RIDERSHIP_LAMBDA
    routes_val = (len(net.routes) / initial_metrics.num_routes) * params.NUM_ROUTES_LAMBDA
    coverage_val = (net.coverage / initial_metrics.coverage) * params.COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / initial_metrics.ridership_density_score) * params.RIDERSHIP_DENSITY_LAMBDA
    fitness = (ridership_val + routes_val + coverage_val + ridership_density_val)/(params.sum_of_fitness_coefficients())
    FitnessObj = Fitness(ridership_val, routes_val, coverage_val, ridership_density_val, fitness)
    return FitnessObj

def evaluate_network_new(net: TransitNetwork, initial_metrics: NetworkMetrics, ZoneEvaluator: ZoneEvaluator):
    ridership_val = (net.ridership / initial_metrics.ridership) * params.RIDERSHIP_LAMBDA
    routes_val = (len(net.routes) / initial_metrics.num_routes) * params.NUM_ROUTES_LAMBDA
    coverage_val = (net.coverage / initial_metrics.coverage) * params.COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / initial_metrics.ridership_density_score) * params.RIDERSHIP_DENSITY_LAMBDA
    zone_score = ZoneEvaluator.evaluate_network(net) * params.ZONE_LAMBDA
    fitness = (ridership_val + routes_val + coverage_val + ridership_density_val + zone_score)/(params.sum_of_fitness_coefficients())

    FitnessObj = Fitness(zone_val=zone_score, 
                         ridership_val=0, 
                         routes_val=0, 
                         coverage_val=0, 
                         ridership_density_val=0,
                         fitness=fitness)
    
    return FitnessObj