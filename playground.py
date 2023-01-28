from simplify_gtfs import create_simplified_gtfs_SFMTA
from transit_network.transit_network import TransitNetwork
from genetic_algorithm.breeder import breed_networks
from graph_gtfs import generate_diagram
from genetic_algorithm.initial_population_generator import generate_population
from genetic_algorithm.fitness_function import evaluate_network
from genetic_algorithm.breeder import breed_networks
from genetic_algorithm.population import Population
from utility import read_object_from_file, pickle_object
"""
This script is purely for informal testing and 'playing' with new code. 
"""

#create_simplified_gtfs_SFMTA()

Network = read_object_from_file('initial_network.pkl')
Network2 = Network.get_copy()
baby1, baby2 = breed_networks(Network, Network2)
baby1.write_to_gtfs('test_diagrams/baby1GTFS')
baby2.write_to_gtfs('test_diagrams/baby2GTFS')

# generate_diagram('test_diagrams/baby1GTFS.zip', 'test_diagrams/baby1')
# generate_diagram('test_diagrams/baby2GTFS.zip', 'test_diagrams/baby2', ['14R:48'])
# MyPopulation = read_object_from_file('test3')
# initial_pop = generate_population(Network, 100)
# MyPopulation = Population(initial_pop, evaluate_network, breed_networks)
#pickle_object(MyPopulation, 'initial_pop')
#res = MyPopulation.run(10)
#print(res)

#myPopulation.population[23].write_to_gtfs('random_network')
# generate_diagram('random_network.zip', 'test_diagrams/random')

# Network2 = Network.get_copy()
# Network3 = breed_networks(Network, Network2)
# Network.write_to_gtfs('parentA')
# Network3.write_to_gtfs('childA')

# generate_diagram('parentA.zip', 'test_diagrams/parentA-shape', ['12', '9'])
# generate_diagram('childA.zip', 'test_diagrams/childA-shape', ['12:9'])



