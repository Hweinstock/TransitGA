from transit_network.transit_network import TransitNetwork, create_network_from_trips
from transit_network.trips import common_transfer_point, SimpleTrip
from root_logger import RootLogger
import random 

def determine_parent_order(Net_A: TransitNetwork, Net_B: TransitNetwork):
    rand_value = random.uniform(0, 1)
    if rand_value > 0.5:
        return Net_A, Net_B
    else:
        return Net_B, Net_A

def produce_child_trip(first_trip: SimpleTrip, second_trip: SimpleTrip, shared_stop: int) -> SimpleTrip:
    
    first_index = first_trip.get_index_of_stop_id(shared_stop)
    second_index = second_trip.get_index_of_stop_id(shared_stop)

    new_stops = first_trip.stops[:first_index] + second_trip.stops[first_index:]
    new_shapes = first_trip.shape_points[:first_index] + second_trip.shape_points[second_index:]
    new_route = '-'.join(first_trip.route_id, second_trip.route_id)
    new_id = '-'.join(first_trip.id, second_trip.id)
    new_message = '-'.join(first_trip.id, second_trip.id)
    
    new_trip = SimpleTrip(trip_id=new_id, route_id=new_route, message=new_message, 
                          direction=first_trip.direction, stops=new_stops, shape_points=new_shapes, 
                          ridership=0)

    
    return new_trip

        

def breed_networks(Net_A: TransitNetwork, Net_B: TransitNetwork, inc_id: bool = False) -> TransitNetwork or None:

    first_parent, second_parent = determine_parent_order(Net_A, Net_B)

    first_parent_trips = first_parent.trips 
    second_parent_trips = second_parent.trips
    child_trip = None

    for A_trip, index in enumerate(first_parent_trips):
        for B_trip in second_parent_trips:
            shared_stop = common_transfer_point(A_trip, B_trip)

            if shared_stop is not None:
                child_trip = produce_child_trip(A_trip, B_trip, shared_stop) 
                break
    
    if child_trip is None:
        RootLogger.log_error(f'Failed to breed networks {Net_A.id} and {Net_B.id}, no common stops found among trips.')
        return None 

    else:
        new_trips = first_parent_trips[:index] + child_trip + first_parent_trips[index+1:]

        if inc_id:
            new_id = str(int(Net_A.id) + 1)
        else:
            new_id = '-'.join(Net_A.id, Net_B.id)

        return create_network_from_trips(new_trips, new_id)




