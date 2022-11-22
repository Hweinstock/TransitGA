from typing import List 
from transit_network.routes import SimpleRoute, GTFSRoute, simplify_route

from root_logger import RootLogger

def create_network_from_GTFSRoutes(routes: List[GTFSRoute]):

    # Determine Transfers for each route
    all_stop_transfers = {}
    for route in routes:
        route_stops = route.get_all_stops()
        for stop in route_stops:
            stop_id = stop.get_id()
            # Already seen this stop
            if stop_id in all_stop_transfers:
                stop_obj = all_stop_transfers[stop_id]
                # noticed that stop_id were duplicated. 
                # Wnder if this is because routes in two directions repeat stops on way back?
                if stop_id not in stop_obj.routes:
                    RootLogger.log_info(f'Found transfer at stop {stop_id} on route {route.id}.')
                    stop_obj.add_transfer_route(route.id)
            else:
                all_stop_transfers[stop.id] = stop
                stop.add_transfer_route(route.id)

    # Update stop objects so that they all have transfer points set. 
    simple_routes = []
    for route in routes:
        RootLogger.log_info(f'Simplifying trips for route {route.id}')

        for trip in route.trips:
            new_stops = [all_stop_transfers[stop[0].get_id()] for stop in trip.stops if all_stop_transfers[stop[0].get_id()].is_transfer()]
            new_stop_ids = [s.get_id() for s in new_stops]
            first_stop = trip.stops[0][0].get_id()
            last_stop = trip.stops[-1][0].get_id()

            # We check if the id is in the stops because id accounts for parent stops
            if first_stop not in new_stop_ids:
                new_stops = [first_stop] + new_stops
            
            if last_stop not in new_stop_ids:
                new_stops += [last_stop]
            
            num_stops = len(trip.stops)
            num_new_stops = len(new_stops)

            if num_new_stops > num_stops:
                RootLogger.log_warning(f'Simplifying trip {trip.id} increased # of stops from {num_stops} to {num_new_stops}')
            else:
                RootLogger.log_debug(f'Trip {trip.id} reduced number of stops from {num_stops} to {num_new_stops}')

            trip.stops = new_stops 

        simple_route = simplify_route(route)
        simple_routes.append(simple_route)
    return simple_routes 
    

class TransitNetwork:

    def __init__(self, routes: List[SimpleRoute]):
        self.routes = routes
