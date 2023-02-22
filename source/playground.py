# from genetic_algorithm.initial_population_generator import initiate_population_from_network
# from utility import read_object_from_file, pickle_object
# from graph_metrics import graph_all_metrics
# from graph_gtfs import generate_diagram
# from genetic_algorithm.breeder import breed_networks
# import os
from simplify_gtfs import create_simplified_gtfs_SFMTA
from utility import read_object_from_file
from genetic_algorithm.zone_evaluator import ZoneEvaluator
from visuals.plot_zones import convert_zones_to_df, next_step
from genetic_algorithm.zone_evaluator import all_zones
"""
This script is purely for informal testing and 'playing' with new code. 
"""
# Network = read_object_from_file('data/new_initial_net/new_initial_net.pkl')
# ZE = ZoneEvaluator(Network)
# ZE.sample_stops()
# score = ZE.evaluate_network(Network)
# print(score)



# create_simplified_gtfs_SFMTA('output/new_initial_net')
#generate_diagram('new_initial_net.zip', 'test_diagrams/new_net')
# print(Network)
#Network2 = read_object_from_file('new_initial_net.pkl')

# net1, net2 = breed_networks(Network, Network2)
# net3, net4 = breed_networks(net1, net2)
# net5, net6 = breed_networks(net3, net4)
# print(net1, net2, net3, net4, net5, net6)


# Population = read_object_from_file('output/100i1000p/population.pkl')
# Population
# net = Population.population[583]
# net.obj.write_to_gtfs('75i1000p/randGTFS')
# generate_diagram('100i1000p/randGTFS.zip', '100i1000p/networkSIMP', route_ids=['45:48:23:91:6:1:91:30:19:48:91:1:91:8:7:91:48:23:91:6:1:91'], include_stops=False)
#generate_diagram('new_initial_net.zip', 'new_initial_net', include_stops=False)

# Pop = read_object_from_file('75i1000p(1)/population.pkl')
# graph_all_metrics(Population=Pop, results_csv='results.csv')


# MyPopulation = read_object_from_file('initial_pop.pkl')
# res = MyPopulation.run(100)
# print(res)

#myPopulation.population[23].write_to_gtfs('random_network')
# generate_diagram('random_network.zip', 'test_diagrams/random')

# Network2 = Network.get_copy()
# Network3 = breed_networks(Network, Network2)
# Network.write_to_gtfs('parentA')
# Network3.write_to_gtfs('childA')

# generate_diagram('parentA.zip', 'test_diagrams/parentA-shape', ['12', '9'])
# generate_diagram('childA.zip', 'test_diagrams/childA-shape', ['12:9'])



