import argparse

def cmdline_args():
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("-p", "--population_size", type=int,
                   help="size of population.", required=True)
    
    p.add_argument("-g", "--num_generations", type=int,
                   help="number of generations.", required=True)
    
    p.add_argument("-bp", "-best_performer",
                   action="store_true",
                   help="include to enable graphing the best performer after finishing.")
    
    p.add_argument("-in", "--initial_network", 
                   default='../data/new_initial_net.pkl', 
                   type=str,
                   help="initial network to use to generate population.")
    
    p.add_argument("-v", "--verbosity", type=int, choices=[0,1,2], default=0,
                   help="increase output verbosity (default: %(default)s)")

    return(p.parse_args())


# Try running with these args
#
# "Hello" 123 --enable
if __name__ == '__main__':
    
    args = cmdline_args()
    print(args)