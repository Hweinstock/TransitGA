import argparse
from argparse import Namespace

def model_run_args() -> Namespace:
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("-p", "--population_size", type=int,
                   help="size of population.", required=True)
    
    p.add_argument("-g", "--num_generations", type=int,
                   help="number of generations.", required=True)
    
    p.add_argument("-bp", "--best_performer",
                   action='store_true',
                   help="include to enable graphing the best performer after finishing.")
    
    p.add_argument("-in", "--initial_network", 
                   default='../data/new_initial_net.pkl', 
                   type=str,
                   help="initial network to use to generate population.")
    
    p.add_argument("-te",  "--time_estimate", 
                   type=int,
                   default=0, 
                   help='get an estimate of running with these parameters. Integer passed in serves as number of test runs to estimate. ')
    
    p.add_argument("-v", "--verbosity", type=int, choices=[0,1,2,3], default=0,
                   help="increase output verbosity (default: %(default)s)")
    

    return(p.parse_args())

def simplify_network_args() -> Namespace:
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("-n", "--name", type=str, 
                   help="name of network", 
                   default="initial_network")
    
    return (p.parse_args())