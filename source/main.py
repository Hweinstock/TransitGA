from utility.pickle import read_object_from_file
from utility.args_parser import model_run_args
from genetic_algorithm.initial_population_generator import initiate_population_from_network 
from genetic_algorithm.population import Population
from visuals.graph_metrics import graph_all_metrics
from visuals.graph_gtfs import generate_diagram
from utility.root_logger import RootLogger
from genetic_algorithm.params import overwrite_lambdas

import os
import pandas as pd
import logging


def run_from_network(num_generations: int, 
                     population_size: int, 
                     initial_network_path: str or None = None, 
                     output_dir: str or None = None, 
                     do_output: bool=True) -> Population:
    """Generate network and run for specified number of iterations

    Args:
        num_generations (int): num generations to run model
        population_size (int): how many networks to generate
        initial_network_path (strorNone, optional): path to initial network pickle file. Defaults to 'data/new_initial_net/new_initial_net.pkl'.
        output_dir (strorNone, optional): where to dump metrics. Defaults to './output/{num_generations}i{population_size}p'.

    Returns:
        Population: Final population of the run. 
    """
    if output_dir is None:
        output_dir = f'./output/{num_generations}i{population_size}p'
    else:
        output_dir = f'{output_dir}/{num_generations}i{population_size}p'

    if initial_network_path is None:
        initial_network_path = 'data/new_initial_net/new_initial_net.pkl'

    RootLogger.log_info(f'Running network {initial_network_path} for {num_generations} with size {population_size}. Sending results to {output_dir}.')

    Network = read_object_from_file(initial_network_path)
    Pop = initiate_population_from_network(Network, population_size)
    res = Pop.run(num_generations)
    if do_output:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        results_filename = Pop.export_metrics(output_directory=output_dir)
        graph_all_metrics(Population=Pop, results_csv=results_filename, output_folder=output_dir)
    return Pop

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

def main(args) -> None:
    RootLogger.initialize(args.output, args.verbosity, args.file_verbosity)
    overwrite_lambdas(coverage_lambda=args.coverage_lambda, ridership_density_lambda=args.ridership_density_lambda, 
                      zone_lambda=args.zone_lambda, extreme_trip_lambda=args.extreme_trip_lambda)
    
    if args.time_estimate != 0:
        from statistics import mean 

        RootLogger.log_info(f'Producing time estimate of running {args.num_generations} of {args.population_size} networks based on {args.time_estimate} runs.')
        FinalPop = run_from_network(args.time_estimate+1, args.population_size, initial_network_path=args.initial_network, do_output=False)
       
        avg_time = mean([x['time'] for x in FinalPop.per_round_metrics[1:]])
        estimate = avg_time * args.num_generations
        RootLogger.log_info(f'Time estimate complete with time of {estimate}.')
    else:
        FinalPop = run_from_network(args.num_generations, args.population_size, 
                                    initial_network_path=args.initial_network, 
                                    output_dir=args.output)
        RootLogger.log_info(f'Run Complete with time of {FinalPop.running_time}.')
    if args.best_performer:
        examine_best_performer(f'{args.output}{args.num_generations}i{args.population_size}p')

if __name__ == '__main__':
   args = model_run_args()
   main(args)