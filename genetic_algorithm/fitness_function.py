from transit_network.transit_network import TransitNetwork

RIDERSHIP_LAMBDA = 0.33
NUM_ROUTES_LAMBDA = -0.33
COVERAGE_LAMBDA = 0.33
RIDERSHIP_DENSITY_LAMBDA = 0.33

# SFMTA statistics
ORIGINAL_RIDERSHIP = 72288387.00000007
ORIGINAL_ROUTES = 53.0
ORIGINAL_COVERAGE = 539.0
ORIGINAL_RIDERSHIP_DENSITY = 61361046702.19314

def evaluate_network(net: TransitNetwork):
    # Need to scale these. 
    ridership_val = (net.ridership / ORIGINAL_RIDERSHIP) * RIDERSHIP_LAMBDA
    routes_val = (len(net.routes) / ORIGINAL_ROUTES) * NUM_ROUTES_LAMBDA
    coverage_val = (net.coverage / ORIGINAL_COVERAGE) * COVERAGE_LAMBDA
    ridership_density_val = (net.ridership_density_score / ORIGINAL_RIDERSHIP_DENSITY) * RIDERSHIP_DENSITY_LAMBDA
    
    return ridership_val + routes_val + coverage_val + ridership_density_val


def evaluate_network_new(net: TransitNetwork):

    pass   