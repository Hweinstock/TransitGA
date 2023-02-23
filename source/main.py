from utility import read_object_from_file
from genetic_algorithm.initial_population_generator import initiate_population_from_network 
from visuals.graph_metrics import graph_all_metrics
from visuals.graph_gtfs import generate_diagram
from visuals.plot_zones import plot_zones
from root_logger import RootLogger
from simplify_gtfs import create_simplified_gtfs_SFMTA
from genetic_algorithm.zone_evaluator import all_zones

import os
import pandas as pd


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

def examine_best_performer(output_dir: str):
    RootLogger.log_info(f'Examining best performer...')
    population_path = os.path.join(output_dir, 'population.pkl')
    results_path = os.path.join(output_dir, 'results.csv')
    gtfs_dir = os.path.join(output_dir, 'gtfs/')

    df = pd.read_csv(results_path)
    id = df['best_performer'].iloc[-1]

    RootLogger.log_info(f'Exporting best performer...')
    pop = read_object_from_file(population_path)
    best_performer = pop.population[id].obj
    best_performer.write_to_gtfs(gtfs_dir)
    zip_path = os.path.join(output_dir, 'gtfs.zip')

    RootLogger.log_info(f'Graphing best performer...')
    generate_diagram(zip_path, os.path.join(output_dir, "best performer"), include_stops=False)
    RootLogger.log_info(f'Done!')


if __name__ == '__main__':
    plot_zones(all_zones)
    # num_generations = 750
    # population_size = 100
    # initial_network_path_input = './data/new_initial_net.pkl'
    # run_from_network(num_generations, population_size, initial_network_path=initial_network_path_input)
    #examine_best_performer('output/1000i500p')
    #create_simplified_gtfs_SFMTA('data/new_initial_net')