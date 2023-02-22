from transit_network.transit_network import TransitNetwork, create_network_from_trips
from transit_network.trips import common_transfer_point, SimpleTrip
from root_logger import RootLogger
import genetic_algorithm.params as params
from genetic_algorithm.family import Family

from typing import List, Tuple
import uuid
import random 
from copy import deepcopy

def kill_random_trips(trips: List[SimpleTrip]):
    r_val = random.uniform(0, 1)
    if r_val >= params.PROB_MUTATION:
        num_killed = random.choice(range(1, params.DELTA_MUTATION+1))
        dead_trips = random.choices(trips, k=num_killed)

        for trip in dead_trips:
            trip.dead = True 

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

    # We deepcopy because we don't want to be modifying the same stop objects for all of them. 
    RootLogger.log_debug(f'Crafting parameters for new child trip...')
    new_stops = deepcopy(first_trip.stops[:first_index] + second_trip.stops[second_index:])

    # Remove the old routes from the trips.     

    new_shapes = deepcopy(first_trip.shape_points[:first_index] + second_trip.shape_points[second_index:])

    # We generate global unique ids for performance reasons. 
    new_route = str(uuid.uuid4())
    new_id = str(uuid.uuid4())
    new_message = '' # Remove the message for performance reasons. 
    RootLogger.log_debug(f'Parameters complete, new id is {new_id}')

    new_trip = SimpleTrip(trip_id=new_id, route_id=new_route, message=new_message, 
                          direction=first_trip.direction, stops=new_stops, shape_points=new_shapes)

    RootLogger.log_debug(f'Successfuly created child trip {new_id} on new route {new_route}')
    return new_trip

def sample_parent_trips(parent_A_trips: List[SimpleTrip], parent_B_trips: List[SimpleTrip]) -> Tuple[SimpleTrip, SimpleTrip, str]:
    RootLogger.log_debug('Attempting to randomly sample overlapping trips...')
    times_tried = 0
    parent_trip_A = None 
    parent_trip_B = None
    while times_tried < params.MAX_RETRY_COUNT:
        rand_A = random.choice(parent_A_trips)
        rand_B = random.choice(parent_B_trips)
        if rand_A != rand_B:
            shared_stop_id = common_transfer_point(rand_A, rand_B)
            if shared_stop_id is not None:
                RootLogger.log_debug(f'Attempt {times_tried + 1} succeeded to sample overlap!')
                # with open('retry_counts.txt', 'a') as output:
                #     output.write(str(times_tried)+ '\n')
                parent_trip_A = rand_A
                parent_trip_B = rand_B
                break 
        RootLogger.log_debug(f'Attempt {times_tried + 1} failed to sample overlaps.')
        times_tried += 1

    if parent_trip_A is None: 
        RootLogger.log_warning(f'Failed in finding overlap between parents, returning None.')
        return None, None, None
    
    return parent_trip_A, parent_trip_B, shared_stop_id

def get_family(parent_A_trips: List[SimpleTrip], parent_B_trips: List[SimpleTrip]) -> Family or None:
    parent_trip_A, parent_trip_B, shared_stop_id = sample_parent_trips(parent_A_trips, parent_B_trips)

    RootLogger.log_debug(f'Producing child trip for trips {parent_trip_A.id} and {parent_trip_B.id}.')
    child_trip_A = produce_child_trip(parent_trip_A, parent_trip_B, shared_stop_id) 
    child_trip_B = produce_child_trip(parent_trip_B, parent_trip_A, shared_stop_id)

    fam = Family(child_A=child_trip_A,
           child_B=child_trip_B,  
           parent_A=parent_trip_A, 
           parent_B=parent_trip_B)

    return fam

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
    #Randomly select one of the shared stops and breed off that one. 
    trip_A_id, trip_B_id, stop_id = random.choices(all_shared_stops, k=1)[0]
    
    RootLogger.log_info((f'Found {len(all_shared_stops)} shared stops for trips {trip_A_id} and {trip_B_id} at stop {stop_id}'))

    #Go from ids -> trip obj so that we can mark which trips to remove. 
    parent_trip_A = get_trip_by_id(parent_A_trips, trip_A_id)
    parent_trip_B = get_trip_by_id(parent_B_trips, trip_B_id)

    # Children Stops
    child_trip_A = produce_child_trip(parent_trip_A, parent_trip_B, shared_stop_id) 
    child_trip_B = produce_child_trip(parent_trip_B, parent_trip_A, shared_stop_id)

    return child_trip_A, child_trip_B

def breed_networks(Net_A: TransitNetwork, Net_B: TransitNetwork, 
                   new_id: str = None) -> TransitNetwork:
    
    RootLogger.log_debug(f'Breeding networks {Net_A.id} and {Net_B.id}')

    # Randomly choose one them to be the first parent. (i.e. which route starts in the crossover)

    net_A_trips = [t.copy() for t in Net_A.trips]
    net_B_trips = [t.copy() for t in Net_B.trips]

    family = get_family(net_A_trips, net_B_trips)
    
    if family is None:
        RootLogger.log_warning((f'Failed to breed networks {Net_A.id} and {Net_B.id}, no common stops found among trips.'
                              f' Returning first parent.'))
        return Net_A

    else: 
        RootLogger.log_debug(f'Crafting new trips for children networks...')

        child_trips = [t for t in net_A_trips if t not in family.parents] + [family.child_A, family.child_B]
        

        RootLogger.log_debug(f'Done crafting new trips for children networks...')

        # Generate 'breeded' ids if none provided. 
        if new_id is None:
            new_id = ':'.join([Net_A.id, Net_B.id])
            
        RootLogger.log_debug(f'Successfully breeded networks {Net_A.id} and {Net_B.id}')
        child_network = create_network_from_trips(child_trips, new_id)
        return child_network




