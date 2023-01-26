from transit_network.transit_network import TransitNetwork, create_network_from_trips
from transit_network.trips import common_transfer_point, SimpleTrip
from root_logger import RootLogger
import random 

from typing import List, Tuple

def determine_parent_order(Net_A: TransitNetwork, Net_B: TransitNetwork):
    rand_value = random.uniform(0, 1)
    if rand_value > 0.5:
        return Net_A, Net_B
    else:
        return Net_B, Net_A

def produce_child_trip(first_trip: SimpleTrip, second_trip: SimpleTrip, shared_stop: str) -> SimpleTrip:
    
    first_index = first_trip.get_index_of_stop_id(shared_stop)
    second_index = second_trip.get_index_of_stop_id(shared_stop)

    new_stops = first_trip.stops[:first_index] + second_trip.stops[second_index:]
    new_shapes = first_trip.shape_points[:first_index] + second_trip.shape_points[second_index:]
    new_route = ':'.join([first_trip.route_id, second_trip.route_id])
    new_id = ':'.join([first_trip.id, second_trip.id])
    new_message = ':'.join([first_trip.id, second_trip.id])
    
    new_trip = SimpleTrip(trip_id=new_id, route_id=new_route, message=new_message, 
                          direction=first_trip.direction, stops=new_stops, shape_points=new_shapes)

    return new_trip

def get_child_trip(parent_A_trips: List[SimpleTrip], parent_B_trips: List[SimpleTrip]) -> Tuple[int, SimpleTrip]:
    all_shared_stops = []
    for A_index, A_trip in enumerate(parent_A_trips):
        for B_index, B_trip in enumerate(parent_B_trips):
            shared_stop = common_transfer_point(A_trip, B_trip)
            if shared_stop is not None:
                all_shared_stops.append((A_index, B_index, shared_stop))


    # Randomly select one of the shared stops and breed off that one. 
    sel_A_index, sel_B_index, sel_stop_id = random.choices(all_shared_stops, k=1)[0]
    sel_A_trip, sel_B_trip = (parent_A_trips[sel_A_index], parent_B_trips[sel_B_index])
    RootLogger.log_info((f'Found {len(all_shared_stops)} shared stops for trips {sel_A_trip.id} and {sel_B_trip.id} at stop {sel_stop_id}'))
    child_trip = produce_child_trip(sel_A_trip, sel_B_trip, sel_stop_id) 
    return sel_A_index, child_trip

def breed_networks(Net_A: TransitNetwork, Net_B: TransitNetwork, new_id: None or str = None) -> TransitNetwork:
    RootLogger.log_debug(f'Breeding networks {Net_A.id} and {Net_B.id}')

    # Randomly choose one them to be the first parent. (i.e. which route starts in the crossover)
    first_parent, second_parent = determine_parent_order(Net_A, Net_B)

    first_parent_trips = first_parent.trips 
    second_parent_trips = second_parent.trips

    index, child_trip = get_child_trip(first_parent_trips, second_parent_trips)
    
    if child_trip is None:
        RootLogger.log_error((f'Failed to breed networks {Net_A.id} and {Net_B.id}, no common stops found among trips.'
                              f' Returning the first parent instead.'))
        return Net_A 

    else:
        new_trips = first_parent_trips[:index] + [child_trip] + first_parent_trips[index+1:]

        if new_id is None:
            new_id = ':'.join([Net_A.id, Net_B.id])
            
        RootLogger.log_debug(f'Successfully breeded networks {Net_A.id} and {Net_B.id}')
        return create_network_from_trips(new_trips, new_id)




