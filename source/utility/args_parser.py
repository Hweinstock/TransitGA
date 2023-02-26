import argparse
from argparse import Namespace

def model_run_args() -> Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    model_parameters = parser.add_argument_group('model parameters')
    
    model_parameters.add_argument("-p", "--population_size", type=int,
                   help="size of population.", required=True)
    
    model_parameters.add_argument("-g", "--num_generations", type=int,
                   help="number of generations.", required=True)
    
    model_parameters.add_argument("-in", "--initial_network", 
                   default='../data/new_initial_net.pkl', 
                   type=str,
                   help="initial network to use to generate population. \n defaults to %(default)s")
    
    options = parser.add_argument_group('additional options')
    options.add_argument("-bp", "--best_performer",
                   action='store_true',
                   help="include to enable graphing the best performer after finishing.")

    options.add_argument("-o", "--output", 
                   default="../output/", 
                   type=str,
                   help='path to output directory, defaults to ../output/')
    
    options.add_argument("-te",  "--time_estimate", 
                   type=int,
                   default=0, 
                   help='get an estimate of running with these parameters. Integer passed in serves as number of test runs to estimate. ')
    
    logging_options = parser.add_argument_group('logging options')
    logging_options.add_argument("-v", "--verbosity", type=int, choices=[0,1,2,3], default=0,
                   help="increase output verbosity (default: %(default)s)")
    
    logging_options.add_argument("-fv", "--file_verbosity", type=int, choices=[0, 1, 2, 3], default=3,
                   help="decrease output log file verbosity (default: %(default)s)")
    
    lambda_parameters = parser.add_argument_group('lambda parameters')

    lambda_parameters.add_argument('--coverage_lambda', type=float, default=0, 
                                   help="weight associated with coverage score (default: %(default)s)")
    lambda_parameters.add_argument('--ridership_density_lambda', type=float, default=1, 
                                   help="weight associated with ridership density score (default: %(default)s)")
    lambda_parameters.add_argument('--zone_lambda', type=float, default=1, 
                                   help="weight associated zone lambda score (default: %(default)s)")
    lambda_parameters.add_argument('--extreme_trip_lambda', type=float, default=-1, 
                                   help="weight associated extreme trip lambda score (default: %(default)s)")


    return(parser.parse_args())

def simplify_network_args() -> Namespace:
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("-n", "--name", type=str, 
                   help="name of network", 
                   default="initial_network")
    
    return (p.parse_args())