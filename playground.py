from simplify_gtfs import create_simplified_gtfs_SFMTA
from transit_network.transit_network import read_network_from_pickle
from genetic_algorithm.breeder import breed_networks
from graph_gtfs import generate_diagram
"""
This script is purely for informal testing and 'playing' with new code. 
"""

#create_simplified_gtfs_SFMTA()

Network = read_network_from_pickle('test')
Network2 = Network.get_copy()
Network3 = breed_networks(Network, Network2)
#Network.to_gtfs('parentA')
#Network3.to_gtfs('childA')

#generate_diagram('parentA.zip', 'parentA')
#generate_diagram('childA.zip', 'childA')



