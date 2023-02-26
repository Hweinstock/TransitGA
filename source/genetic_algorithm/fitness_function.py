from transit_network.transit_network import TransitNetwork
import genetic_algorithm.params as params
from genetic_algorithm.network_metrics import NetworkMetrics
from genetic_algorithm.zone_evaluator import ZoneEvaluator

class Fitness:

    def __init__(self, zone_val: float, 
                       coverage_val: float, 
                       ridership_density_val: float, 
                       fitness: float):
        self.coverage_val = coverage_val / (params.sum_of_fitness_coefficients())
        self.ridership_density_val = ridership_density_val / (params.sum_of_fitness_coefficients())
        self.zone_val = zone_val / (params.sum_of_fitness_coefficients())
        self.fitness = fitness
    
    def to_dict(self):
        return {
            'coverage_val': self.coverage_val, 
            'ridership_density_val': self.ridership_density_val, 
            'zone_val': self.zone_val,
            'fitness': self.fitness
        }
    
    def get_metrics_list(self):
        return list(self.to_dict().keys())

def evaluate_network_new(net: TransitNetwork, initial_metrics: NetworkMetrics, ZoneEvaluator: ZoneEvaluator):
    coverage_val = (net.coverage / initial_metrics.coverage) * params.COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / initial_metrics.ridership_density_score) * params.RIDERSHIP_DENSITY_LAMBDA
    zone_score = ZoneEvaluator.evaluate_network(net) * params.ZONE_LAMBDA
    fitness = (coverage_val + ridership_density_val + zone_score)/(params.sum_of_fitness_coefficients())

    FitnessObj = Fitness(zone_val=zone_score, 
                         coverage_val=coverage_val, 
                         ridership_density_val=ridership_density_val,
                         fitness=fitness)
    
    return FitnessObj