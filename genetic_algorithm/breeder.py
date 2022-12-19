from transit_network.transit_network import TransitNetwork 
from transit_network.trips import common_transfer_point, SimpleTrip
from root_logger import RootLogger

def produce_child(A_trip: SimpleTrip, B_trip: SimpleTrip, shared_stop: int) -> SimpleTrip:
    pass


def breed_networks(net_A: TransitNetwork, net_B: TransitNetwork):
    net_A_trips = net_A.trips 
    net_B_trips = net_B.trips 
    child = None 
    for A_trip in net_A_trips:
        for B_trip in net_B_trips:
            shared_stop = common_transfer_point(A_trip, B_trip)

            if shared_stop is not None:
                child = produce_child(A_trip, B_trip, shared_stop) 
                break
    
    if child is None:
        RootLogger.log_error(f'Failed to breed networks, no common stops found among trips.')
        return None 
    else:
        pass


