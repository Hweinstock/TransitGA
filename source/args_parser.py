import sys
import argparse

def cmdline_args():
        # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("required_positional_arg",
                   help="desc")
    p.add_argument("required_int", type=int,
                   help="req number")
    p.add_argument("--on", action="store_true",
                   help="include to enable")
    p.add_argument("-v", "--verbosity", type=int, choices=[0,1,2], default=0,
                   help="increase output verbosity (default: %(default)s)")
                   
    group1 = p.add_mutually_exclusive_group(required=True)
    group1.add_argument('--enable',action="store_true")
    group1.add_argument('--disable',action="store_false")

    return(p.parse_args())


# Try running with these args
#
# "Hello" 123 --enable
if __name__ == '__main__':
    
    if sys.version_info<(3,5,0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)
        
    try:
        args = cmdline_args()
        print(args)
    except:
        print('Try $python <script_name> "Hello" 123 --enable')

    print()