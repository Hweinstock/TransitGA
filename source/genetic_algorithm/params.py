##  Breeder
MAX_RETRY_COUNT = 100
PROB_MUTATION = 0.01
DELTA_MUTATION = 2

##  Fitness Function
COVERAGE_LAMBDA = 0
RIDERSHIP_DENSITY_LAMBDA = 1
ZONE_LAMBDA = 3
EXTREME_TRIP_LAMBDA = 2

ZONE_RADIUS = 900
ZONE_EPSILON = 0.5
DEFAULT_ZONE_DISTANCE = 40
ZONE_SAMPLE_NUM = 3

MIN_NUM_STOPS = 5 
MAX_NUM_STOPS = 90

ZONE_FILE = '../data/zone_file.csv'
# Can use to draw: https://www.calcmaps.com/map-radius/
Z1_LAT = 37.780554
Z1_LON = -122.472288
Z1_NAME = "Inner Richmond"
Z1_COLOR = "blue"

# Downtown
Z2_LAT = 37.779743
Z2_LON = -122.413583
Z2_NAME = "Downtown"
Z2_COLOR = "red"

# Mission
Z3_LAT = 37.752252
Z3_LON = -122.418125
Z3_NAME = "Mission"
Z3_COLOR = "green"

# West Portal
Z4_LAT = 37.738030
Z4_LON = -122.469079
Z4_NAME = "West Portal"
Z4_COLOR = "purple"

Z5_LAT = 37.792728
Z5_LON = -122.397015
Z5_NAME = "Embarcadero"
Z5_COLOR = "pink"

Z6_LAT = 37.794521
Z6_LON = -122.404864
Z6_NAME = "Chinatown"
Z6_COLOR = "orange"

Z7_LAT = 37.784542
Z7_LON = -122.431252
Z7_NAME = "Pacific Heights/Japantown"
Z7_COLOR = "cyan"

Z8_LAT = 37.757698
Z8_LON =  -122.392687
Z8_NAME = "Dogpatch"
Z8_COLOR = "lime"

Z9_LAT = 37.770224
Z9_LON = -122.445421
Z9_NAME = "Haight and Ashbury"
Z9_COLOR = "grey"

Z10_LAT = 37.775891
Z10_LON = -122.496533
Z10_NAME = "Outer Richmond"
Z10_COLOR = "teal"

Z11_LAT = 37.761713
Z11_LON = -122.477040
Z11_NAME = "Irving/Judah-Sunset"
Z11_COLOR = "tomato"

Z12_LAT = 37.799901
Z12_LON = -122.436089
Z12_NAME = "Marina District"
Z12_COLOR = "olive"

def cutoff_by_round(iteration: int, max_iteration: int) -> float:
    # From [1, max_iteration] -> 0.1 to 0.9
    max_cutoff = 0.9 
    min_cutoff = 0.1

    val = (iteration-1)/(max_iteration-1) * (max_cutoff-min_cutoff) + min_cutoff
    return val

def sum_of_fitness_coefficients():
    return COVERAGE_LAMBDA + RIDERSHIP_DENSITY_LAMBDA + ZONE_LAMBDA + EXTREME_TRIP_LAMBDA