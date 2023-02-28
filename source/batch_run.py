
import os 

from visuals.graph_metrics import graph_all_metrics
from utility.pickle import read_object_from_file
from genetic_algorithm.initial_population_generator import initiate_population_from_network
from genetic_algorithm.params import overwrite_lambdas
from utility.root_logger import RootLogger
from utility.args_parser import batch_run_args
from main import examine_best_performer

def try_different_lambdas(args):
    RootLogger.log_info(f'Running batch with different lambda with {args.population_size} size and {args.num_generations} generations.')

    Network = read_object_from_file(args.initial_network)

    batches = [(2, 2, 1), (2, 4, 1), (4, 2, 1), 
               (3, 3, 1), (6, 3, 1), (3, 6, 1),
               (1, 1, 1), (1, 10, 1), (10, 1, 1)]
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    for index, batch in enumerate(batches):
        RootLogger.log_info(f'On batch {index + 1} of {len(batches)}')
        ridership_density_lambda, zone_lambda, extreme_trip_lambda = batch 
        InitialPopulation = initiate_population_from_network(Network, args.population_size)
        res = InitialPopulation.run(args.num_generations)
        valid_params = overwrite_lambdas(coverage_lambda=0, ridership_density_lambda=ridership_density_lambda, 
                        zone_lambda=zone_lambda, extreme_trip_lambda=-1*extreme_trip_lambda)
        
        if not valid_params:
            RootLogger.log_warning(f'Skipping batch {index +1} due to invalid parameters.')
            continue

        cur_output = os.path.join(args.output, f'rd{ridership_density_lambda}z{zone_lambda}et{extreme_trip_lambda}-{args.num_generations}i{args.population_size}p')

        if not os.path.exists(cur_output):
            os.makedirs(cur_output)
        results_filename = InitialPopulation.export_metrics(output_directory=cur_output)
        RootLogger.log_info(f'Graphing all metrics for batch {index + 1}')
        graph_all_metrics(Population=InitialPopulation, results_csv=results_filename, output_folder=cur_output)

        if args.best_performer:
            try:
                RootLogger.log_info(f'Graphing best performer for batch {index + 1}')
                examine_best_performer(cur_output)
            except ValueError:
                RootLogger.log_error(f'Failed to generate diagram for batch run to {cur_output}')

if __name__ == '__main__':
    args = batch_run_args()
    
    RootLogger.initialize(args.output, args.verbosity, args.file_verbosity)
    try_different_lambdas(args)
        
