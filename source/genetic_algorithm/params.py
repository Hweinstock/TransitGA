##  Breeder
MAX_RETRY_COUNT = 100
PROB_MUTATION = 0.01
DELTA_MUTATION = 2

##  Fitness Function
RIDERSHIP_LAMBDA = 0.0
NUM_ROUTES_LAMBDA = 0.0
COVERAGE_LAMBDA = 0.0
RIDERSHIP_DENSITY_LAMBDA = 0.0
ZONE_LAMBDA = 0.5

ZONE_RADIUS = 1000
ZONE_EPSILON = 0.5
DEFAULT_ZONE_DISTANCE = 20

Z1_LAT = 37.780554
Z1_LON = -122.472288
Z1_NAME = "Richmond"

# Downtown
Z2_LAT = 37.792519
Z2_LON = -122.397427
Z2_NAME = "Downtown"

# Mission
Z3_LAT = 37.752252
Z3_LON = -122.418125
Z3_NAME = "Mission"

# West Portal
Z4_LAT = 37.738030
Z4_LON = -122.469079
Z4_NAME = "West Portal"


def sum_of_fitness_coefficients():
    return RIDERSHIP_LAMBDA + NUM_ROUTES_LAMBDA + COVERAGE_LAMBDA + RIDERSHIP_DENSITY_LAMBDA + ZONE_LAMBDA