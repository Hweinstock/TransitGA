from typing import List, Tuple
import numpy as np
import pandas as pd
from statistics import mean, median, stdev
import time
import os

from genetic_algorithm.zone_evaluator import ZoneEvaluator
from genetic_algorithm.chromosome import Chromosome
from genetic_algorithm.network_metrics import NetworkMetrics
from root_logger import RootLogger
from utility import pickle_object

def scale_to_prob_dist(weights: List[float]) -> List[float]:
    s = sum(weights)
    return [w / s for w in weights]

class Population:

    mutation_rate = 0.1

    def __init__(self, networks: List[Chromosome], 
                       initial_metrics: NetworkMetrics, 
                       ZoneEvaluator: ZoneEvaluator, 
                       fitness_function, 
                       breeding_function, 
                       elitist_cutoff):
        
        self.population = networks
        self.population_size = len(networks)
        self.fitness_function = fitness_function
        self.breeding_function = breeding_function
        self.elitist_cutoff = elitist_cutoff
        self.iteration_number = 1
        self.performance_dict = {}
        self.per_round_metrics = []
        self.write_to_pickle = pickle_object
        self.initial_metrics = initial_metrics
        self.ZoneEvaluator = ZoneEvaluator
        self.done_running = False
        self.running_time = 0.0

        self.max_iteration = None
    
    def evaluate_population(self):
        RootLogger.log_debug('Evaluating population...')
        self.performance_dict = {}
        #self.ZoneEvaluator.sample_stops()
        for index, member in enumerate(self.population):
            # Assign the member a unique_id equal to index. 
            member.unique_id = index

            # If we haven't evaluated this chromosome yet, evaluate, otherwise use old score. 
            if member.FitnessObj is not None: 
                FitnessObj = member.FitnessObj
            else:
                FitnessObj = self.fitness_function(member.obj, self.initial_metrics, self.ZoneEvaluator)
                member.FitnessObj = FitnessObj

            # Check that this is the first time we see this id. 
            if member.unique_id in self.performance_dict:
                RootLogger.log_warning(f'Population members with duplicate ids found in population. Overwriting fitness.')
            self.performance_dict[member.unique_id] = FitnessObj
        
        # Update metrics
        self.set_performance_metrics(self.performance_dict)
        RootLogger.log_debug('Done evaluating population!')
    
    def select_parents(self, pool: List[Chromosome]) -> Tuple[Chromosome, Chromosome]:
        weights = scale_to_prob_dist([self.performance_dict[m.unique_id].fitness for m in pool])
        
        if len(pool) == 0:
            RootLogger.log_error(f'Attempt to sample parent network from empty pool!')
            raise ValueError
        if len(pool) < 2:
            [parent_1, parent_2] = [pool[0], pool[0]]
        else:
            [parent_1, parent_2] = np.random.choice(pool, size=2, replace=False, p=weights)
            
        return parent_1, parent_2
    
    def breed_children(self, pool_of_parents: List[Chromosome], child_num: int) -> Chromosome:
        parent_1, parent_2 = self.select_parents(pool_of_parents)

        # Tracking number of times they have been parent. 
        parent_1.num_times_parent += 1
        parent_2.num_times_parent += 1

        new_id = f'{self.iteration_number}:{child_num}'
        
        # Extract out the objects from the chromosomes. 
        new_child = self.breeding_function(parent_1.obj, parent_2.obj, new_id=new_id)
        new_member = Chromosome(new_child, parent_A_id=parent_1.unique_id, parent_B_id=parent_2.unique_id)
        return new_member
    
    def get_member_by_id(self, sel_id: str) -> Chromosome or None:
        matching_members = [m for m in self.population if m.unique_id == sel_id]
        if len(matching_members) > 1:
            RootLogger.log_error(f'Multiple Networks found with the same id {sel_id}. Selecting randomly.')
        
        if len(matching_members) == 0:
            RootLogger.log_error(f'Unable to find network with id {sel_id}.')
            return
        return matching_members[0]
    
    def update_population(self):
        new_population = self.get_next_population()
        self.population = new_population
        RootLogger.log_debug('New population updated successfully.')
        self.iteration_number += 1

    def dispose_of_dead_chromosomes(self, dead_chromosomes: List[Chromosome]):
        for chrom in dead_chromosomes:
            del chrom

    def get_next_population(self):
        RootLogger.log_info(f'Generating next Population...')
        new_population = []
        self.evaluate_population()

        # Select best performing networks
        RootLogger.log_debug(f'Performing Elitist Selection on population.')
        percent_cutoff = self.elitist_cutoff(self.iteration_number, self.max_iteration)
        elitist_num = int(percent_cutoff*self.population_size)
        sorted_by_performance = sorted(self.population, key=lambda mem: self.performance_dict[mem.unique_id].fitness, reverse=True)

        top_performers = sorted_by_performance[:elitist_num]
        bot_performers = sorted_by_performance[elitist_num:]

        self.dispose_of_dead_chromosomes(bot_performers)

        new_population += top_performers

        # Compute Children
        children_needed = self.population_size - elitist_num 
        RootLogger.log_info(f'Producing {children_needed} to fill out population.')
        while children_needed > 0:
            RootLogger.log_debug(f'{children_needed} more children to go.')
            new_child =  self.breed_children(top_performers, children_needed)
            new_population.append(new_child)
            children_needed -= 1

        RootLogger.log_info(f'Done generating next Population...')
        return new_population

    def set_performance_metrics(self, current_fitness_metrics):
        metrics = self.generate_metrics(current_fitness_metrics)
        self.per_round_metrics.append(metrics)

    def generate_metrics(self, current_fitness_metrics) -> str:
        
        result = {}
        best_performer = max(current_fitness_metrics, key=lambda iter: current_fitness_metrics[iter].fitness)
        best_score = current_fitness_metrics[best_performer].fitness
        result['best_performer'] = best_performer
        result['best_fitness'] = best_score

        tracking_metrics = current_fitness_metrics[0].get_metrics_list()

        metric_dicts = [f.to_dict() for f in current_fitness_metrics.values()]
        for metric in tracking_metrics:
            metric_values = [d[metric] for d in metric_dicts]
            avg_metric, med_metric, stdev_metric = mean(metric_values), median(metric_values), stdev(metric_values)
            result[f'avg_{metric}'] = avg_metric
            result[f'med_{metric}'] = med_metric
            result[f'stddev_{metric}'] = stdev_metric

        return result

    def run(self, max_iteration: int):
        RootLogger.log_info(f'Running population for {max_iteration} iterations.')
        self.max_iteration = max_iteration
        while self.iteration_number <= max_iteration:
            start_time = time.time()
            RootLogger.log_info(f'On iteration {self.iteration_number} of {max_iteration}.')
            self.update_population()
            end_time = time.time()
            # Append time to metrics
            self.running_time += (end_time - start_time)
            self.per_round_metrics[-1]['time'] = end_time - start_time

            RootLogger.log_info(f'Iteration complete, took {end_time - start_time}s')
            time_est = (self.running_time / self.iteration_number) * (max_iteration - self.iteration_number)
            RootLogger.log_info(f'Estimated {time_est}s remaining for {(max_iteration - self.iteration_number)} rounds.')
        
        RootLogger.log_info(f'Done running population for {max_iteration} iterations. Returning Metrics.')
        self.done_running = True
        return self.per_round_metrics
    
    def export_metrics(self, metrics_filename='results.csv', output_directory='') -> Tuple[str, str]:
        output_file = os.path.join(output_directory, metrics_filename)
        if not self.done_running:
            RootLogger.log_warning(f'Generating Metrics for unfinished population object...')
        RootLogger.log_info(f'Outputting metrics to {output_file}...')

        df = pd.DataFrame(self.per_round_metrics)
        df.to_csv(output_file, index_label='iteration')

        RootLogger.log_info(f'Done outputting metrics to {output_file}!')

        return output_file
        
            
    
    

    


        
                


