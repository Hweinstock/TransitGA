from utility import read_object_from_file
from genetic_algorithm.initial_population_generator import initiate_population_from_network 
from visuals.graph_metrics import graph_all_metrics
from root_logger import RootLogger

import os


def run_from_network(num_generations: int, population_size: int, initial_network_path: str or None = None, output_dir: str or None = None):
    if output_dir is None:
        output_dir = f'./output/{num_generations}i{population_size}p'

    if initial_network_path is None:
        initial_network_path = 'data/new_initial_net/new_initial_net.pkl'

    RootLogger.log_info(f'Running network {initial_network_path} for {num_generations} with size {population_size}. Sending results to {output_dir}.')

    Network = read_object_from_file(initial_network_path)
    Pop = initiate_population_from_network(Network, 10)
    res = Pop.run(num_generations)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    results_filename = Pop.export_metrics(output_directory=output_dir)
    graph_all_metrics(Population=Pop, results_csv=results_filename, output_folder=output_dir)



if __name__ == '__main__':
    run_from_network(500, 10, initial_network_path='./output/new_initial_net.pkl')