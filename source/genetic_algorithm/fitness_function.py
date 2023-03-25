from transit_network.transit_network import TransitNetwork
import genetic_algorithm.params as params
from genetic_algorithm.network_metrics import NetworkMetrics
from genetic_algorithm.zone_evaluator import ZoneEvaluator

class Fitness:

    def __init__(self, zone_val: float, 
                       coverage_val: float, 
                       ridership_density_val: float, 
                       extreme_trips: float,
                       fitness: float):
        self.coverage_val = coverage_val / (params.sum_of_fitness_coefficients())
        self.ridership_density_val = ridership_density_val / (params.sum_of_fitness_coefficients())
        self.zone_val = zone_val / (params.sum_of_fitness_coefficients())
        self.extreme_trips = extreme_trips / (params.sum_of_fitness_coefficients())
        self.fitness = fitness
    
    def to_dict(self):
        return {
            'coverage_val': self.coverage_val, 
            'ridership_density_val': self.ridership_density_val, 
            'extreme_trips_val': self.extreme_trips,
            'zone_val': self.zone_val,
            'fitness': self.fitness
        }
    
    def get_metrics_list(self):
        return list(self.to_dict().keys())

def evaluate_network_new(net: TransitNetwork, initial_metrics: NetworkMetrics, ZoneEvaluator: ZoneEvaluator):
    coverage_val = (net.coverage / initial_metrics.coverage) * params.COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / initial_metrics.ridership_density_score) * params.RIDERSHIP_DENSITY_LAMBDA
    zone_score = ZoneEvaluator.evaluate_network(net) * params.ZONE_LAMBDA
    extreme_trips = (net.count_extreme_routes(params.MIN_NUM_STOPS, params.MAX_NUM_STOPS) / initial_metrics.extreme_routes) * params.EXTREME_TRIP_LAMBDA
    fitness = (coverage_val + ridership_density_val + zone_score + extreme_trips)/(params.sum_of_fitness_coefficients())

    FitnessObj = Fitness(zone_val=zone_score, 
                         coverage_val=coverage_val, 
                         ridership_density_val=ridership_density_val,
                         extreme_trips=extreme_trips,
                         fitness=fitness)
    
    return FitnessObj