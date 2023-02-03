from genetic_algorithm.initial_population_generator import initiate_population_from_network
from utility import read_object_from_file
from graph_metrics import plot_per_round_metrics
from genetic_algorithm.breeder import breed_networks
"""
This script is purely for informal testing and 'playing' with new code. 
"""

#create_simplified_gtfs_SFMTA('new_initial_net')
#generate_diagram('new_initial_net.zip', 'test_diagrams/new_net')

Network = read_object_from_file('new_initial_net.pkl')
Network2 = read_object_from_file('new_initial_net.pkl')

# net1, net2 = breed_networks(Network, Network2)
# net3, net4 = breed_networks(net1, net2)
# net5, net6 = breed_networks(net3, net4)
# print(net1, net2, net3, net4, net5, net6)

Pop = initiate_population_from_network(Network, 1000)
# res = Pop.run(50)
# filename = Pop.export_metrics()
# plot_per_round_metrics(filename, 'plot2.png')


# print(Network.ridership_density_score)
# print(Network.ridership_density_score)
# Network2 = Network.get_copy()
# baby1, baby2 = breed_networks(Network, Network2)
# baby1.write_to_gtfs('test_diagrams/baby1GTFS')
# baby2.write_to_gtfs('test_diagrams/baby2GTFS')

# generate_diagram('test_diagrams/baby1GTFS.zip', 'test_diagrams/baby1')
# generate_diagram('test_diagrams/baby2GTFS.zip', 'test_diagrams/baby2', ['14R:48'])

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



