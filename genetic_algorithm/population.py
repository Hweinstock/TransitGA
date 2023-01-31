from typing import List, Tuple
import numpy as np
from statistics import mean, median, stdev

from genetic_algorithm.chromosome import Chromosome
from root_logger import RootLogger
from utility import pickle_object

def scale_to_prob_dist(weights: List[float]) -> List[float]:
    s = sum(weights)
    return [w / s for w in weights]

class Population:

    mutation_rate = 0.1
    elitist_cutoff = 0.5

    def __init__(self, networks: List[Chromosome], fitness_function, breeding_function):
        self.population = networks
        self.population_size = len(networks)
        self.fitness_function = fitness_function
        self.breeding_function = breeding_function
        self.iteration_number = 1
        self.performance_dict = {}
        self.per_round_metrics = []
        self.write_to_pickle = pickle_object
    
    def evaluate_population(self):
        for index, member in enumerate(self.population):
            # Assign the member a unique_id equal to index. 
            member.unique_id = index
            score = self.fitness_function(member.obj)

            # Check that this is the first time we see this id. 
            if member.unique_id in self.performance_dict:
                RootLogger.log_warning(f'Population members with duplicate ids found in population. Overwriting fitness.')
            self.performance_dict[member.unique_id] = score 
        
        self.set_performance_metrics()
    
    def select_parents(self, pool: List[Chromosome]) -> Tuple[Chromosome, Chromosome]:
        weights = scale_to_prob_dist([self.performance_dict[m.unique_id] for m in pool])

        [parent_1, parent_2] = np.random.choice(pool, 
                                                     size=2, replace=False, 
                                                     p=weights)
        return parent_1, parent_2
    
    def breed_children(self, pool_of_parents: List[Chromosome]) -> Tuple[Chromosome, Chromosome]:
        parent_1, parent_2 = self.select_parents(pool_of_parents)

        # Tracking number of times they have been parent. 
        parent_1.num_times_parent += 1
        parent_2.num_times_parent += 1
        
        # Extract out the objects from the chromosomes. 
        new_child_A, new_child_B = self.breeding_function(parent_1.obj, parent_2.obj)
        new_member_A = Chromosome(new_child_A, parent_A_id=parent_1.get_family_history(), parent_B_id=parent_2.get_family_history())
        new_member_B = Chromosome(new_child_B, parent_A_id=parent_1.get_family_history(), parent_B_id=parent_2.get_family_history())
        return new_member_A, new_member_B
    
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
        self.performance_dict = {}
        RootLogger.log_debug('New population updated successfully.')
        self.iteration_number += 1

    def get_next_population(self):
        RootLogger.log_info(f'Generating next Population...')
        new_population = []
        self.evaluate_population()

        # Select best performing networks
        RootLogger.log_debug(f'Performing Elitist Selection on population.')
        elitist_num = int(self.elitist_cutoff*self.population_size)
        top_performers = sorted(self.population, key=lambda mem: self.performance_dict[mem.unique_id], reverse=True)[:elitist_num]
        new_population += top_performers

        # Compute Children
        children_needed = self.population_size - elitist_num 
        RootLogger.log_info(f'Producing {children_needed} to fill out population.')
        while children_needed > 0:
            RootLogger.log_debug(f'{children_needed} more children to go.')
            new_child_A, new_child_B = self.breed_children(top_performers)
            new_population.append(new_child_A)
            new_population.append(new_child_B)
            children_needed -= 2

        RootLogger.log_info(f'Done generating next Population...')
        return new_population

    def set_performance_metrics(self):
        metrics = self.generate_metrics()
        self.per_round_metrics.append(metrics)

    def generate_metrics(self):
        if self.performance_dict == {}:
            print('it is empty')
        best_performer = max(self.performance_dict, key=self.performance_dict.get)
        best_score = max(self.performance_dict.values()) 

        avg_score = mean(self.performance_dict.values())
        med_score = median(self.performance_dict.values())

        stdev_score = stdev(self.performance_dict.values())

        return {
            'best_performer': best_performer, 
            'best_fitness': best_score, 
            'avg_score': avg_score, 
            'med_score': med_score,
            'stdev': stdev_score
        }
    def run(self, max_iteration: int):
        RootLogger.log_info(f'Running population for {max_iteration} iterations.')
        while self.iteration_number <= max_iteration:
            RootLogger.log_info(f'On iteration {self.iteration_number} of {max_iteration}.')
            self.update_population()
            self.iteration_number += 1
        RootLogger.log_info(f'Done running population for {max_iteration} iterations. Returning Metrics.')
        return self.per_round_metrics
    
    

    


        
                


