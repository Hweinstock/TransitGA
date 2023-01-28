from transit_network.transit_network import TransitNetwork, create_network_from_trips
from transit_network.trips import common_transfer_point, SimpleTrip
from root_logger import RootLogger
import random 

from typing import List, Tuple

def get_trip_by_id(collection: List[SimpleTrip], target_id: str) -> SimpleTrip or None:
    filter_results = [t for t in collection if t.id == target_id]
    num_results = len(filter_results)
    if num_results == 0:
        RootLogger.log_error(f'Unable to find trip with target_id {target_id}. Returning None.')
        return None
    if num_results > 1:
        RootLogger.log_warning(f'{num_results} trips found with target_id {target_id}, returning one arbitrarily.')
    return filter_results[0]

def determine_parent_order(Net_A: TransitNetwork, Net_B: TransitNetwork):
    """
    No longer using because we breed two children. 
    """
    rand_value = random.uniform(0, 1)
    if rand_value > 0.5:
        return Net_A, Net_B
    else:
        return Net_B, Net_A

def produce_child_trip(first_trip: SimpleTrip, second_trip: SimpleTrip, shared_stop: str) -> SimpleTrip:
    RootLogger.log_debug(f'Producing child trip for trip {first_trip.id} and {second_trip.id}.')
    first_index = first_trip.get_index_of_stop_id(shared_stop)
    second_index = second_trip.get_index_of_stop_id(shared_stop)

    new_stops = first_trip.stops[:first_index] + second_trip.stops[second_index:]
    new_shapes = first_trip.shape_points[:first_index] + second_trip.shape_points[second_index:]
    new_route = ':'.join([first_trip.route_id, second_trip.route_id])
    new_id = ':'.join([first_trip.id, second_trip.id])
    new_message = ':'.join([first_trip.id, second_trip.id])

    new_trip = SimpleTrip(trip_id=new_id, route_id=new_route, message=new_message, 
                          direction=first_trip.direction, stops=new_stops, shape_points=new_shapes)
    RootLogger.log_debug(f'Successfuly created child trip {new_id} on new troute {new_route}')
    return new_trip

def get_child_trips(parent_A_trips: List[SimpleTrip], parent_B_trips: List[SimpleTrip]) -> Tuple[SimpleTrip, SimpleTrip, SimpleTrip, SimpleTrip] or None:
   
    all_shared_stops = [] # [(A_trip.id, B_trip.id, stop.id)]
    for A_trip in parent_A_trips:
        for B_trip in parent_B_trips:
            if A_trip != B_trip: # Don't want to breed the same trip with eachother. 
                shared_stop_id = common_transfer_point(A_trip, B_trip)
                if shared_stop_id is not None:
                    all_shared_stops.append((A_trip.id, B_trip.id, shared_stop_id))

    if all_shared_stops == []:
        return None
    # Randomly select one of the shared stops and breed off that one. 
    trip_A_id, trip_B_id, stop_id = random.choices(all_shared_stops, k=1)[0]
    
    RootLogger.log_info((f'Found {len(all_shared_stops)} shared stops for trips {trip_A_id} and {trip_B_id} at stop {stop_id}'))
    # Go from ids -> trip obj so that we can mark which trips to remove. 
    parent_trip_A = get_trip_by_id(parent_A_trips, trip_A_id)
    parent_trip_B = get_trip_by_id(parent_B_trips, trip_B_id)
    parent_trip_A.dead = True 
    parent_trip_B.dead = True

    child_trip_A = produce_child_trip(parent_trip_A, parent_trip_B, stop_id) 
    child_trip_B = produce_child_trip(parent_trip_B, parent_trip_A, stop_id)

    return child_trip_A, child_trip_B

def breed_networks(Net_A: TransitNetwork, Net_B: TransitNetwork, 
                   new_id_A: str = None, new_id_B: str = None) -> Tuple[TransitNetwork, TransitNetwork]:
    
    RootLogger.log_debug(f'Breeding networks {Net_A.id} and {Net_B.id}')

    # Randomly choose one them to be the first parent. (i.e. which route starts in the crossover)

    net_A_trips = Net_A.trips 
    net_B_trips = Net_B.trips

    children = get_child_trips(net_A_trips, net_B_trips)
    
    if children is None:
        RootLogger.log_error((f'Failed to breed networks {Net_A.id} and {Net_B.id}, no common stops found among trips.'
                              f' Returning the first parent instead.'))
        return Net_A 

    else:
        child_trip_A, child_trip_B  = children 
        new_trips_A = [t if not t.dead else child_trip_A for t in net_A_trips]
        new_trips_B = [t if not t.dead else child_trip_B for t in net_B_trips]
        

        # Generate 'breeded' ids if none provided. 
        if new_id_A is None:
            new_id_A = ':'.join([Net_A.id, Net_B.id])
        if new_id_B is None:
            new_id_B = ':'.join([Net_B.id, Net_A.id])
            
        RootLogger.log_debug(f'Successfully breeded networks {Net_A.id} and {Net_B.id}')
        child_network_A = create_network_from_trips(new_trips_A, new_id_A)
        child_network_B = create_network_from_trips(new_trips_B, new_id_B)
        return child_network_A, child_network_B




