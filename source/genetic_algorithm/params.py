##  Breeder
MAX_RETRY_COUNT = 100
PROB_MUTATION = 0.01
DELTA_MUTATION = 2

##  Fitness Function
RIDERSHIP_LAMBDA = 0.33
NUM_ROUTES_LAMBDA = -0.33
COVERAGE_LAMBDA = 0.33
RIDERSHIP_DENSITY_LAMBDA = 0.33

def sum_of_fitness_coefficients():
    return RIDERSHIP_LAMBDA + NUM_ROUTES_LAMBDA + COVERAGE_LAMBDA + RIDERSHIP_DENSITY_LAMBDA