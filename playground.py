from simplify_gtfs import create_simplified_gtfs_SFMTA
from transit_network.transit_network import read_network_from_pickle
from genetic_algorithm.breeder import breed_networks
"""
This script is purely for informal testing and 'playing' with new code. 
"""

#create_simplified_gtfs_SFMTA()

Network = read_network_from_pickle('test')
Network2 = Network.get_copy()

Network3 = breed_networks(Network, Network2)



