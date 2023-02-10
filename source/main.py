from utility import read_object_from_file
from genetic_algorithm.initial_population_generator import initiate_population_from_network 
from visuals.graph_metrics import graph_all_metrics
from root_logger import RootLogger

import os


def run_from_default(num_generations: int, population_size: int, output_dir: str or None = None):
    if output_dir is None:
        output_dir = f'./output/{num_generations}i{population_size}p'
    RootLogger.log_info(f'Running default for {num_generations} with size {population_size}. Sending results to {output_dir}.')
    Network = read_object_from_file('data/new_initial_net/new_initial_net.pkl')
    Pop = initiate_population_from_network(Network, 10)
    res = Pop.run(num_generations)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    results_filename = Pop.export_metrics(output_directory=output_dir)
    graph_all_metrics(Population=Pop, results_csv=results_filename, output_folder=output_dir)



if __name__ == '__main__':
    run_from_default(500, 10)