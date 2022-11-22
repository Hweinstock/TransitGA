from typing import List 

from transit_network.routes import SimpleRoute, GTFSRoute, simplify_route
from transit_network.stops import Stop 
from transit_network.trips import Trip 

from root_logger import RootLogger

def assign_ridership_to_stops(StopList: List[Stop], route_ridership: int):
    num_of_stops = len(StopList)

    # We incremement since transfer stops will naturally occur multiple times. 
    # This rewards transfer stops by counting them on each route they transfer for. 
    for stop in StopList:
        stop.ridership += route_ridership / num_of_stops


class TransitNetwork:

    def __init__(self, routes: List[SimpleRoute]):
        self.routes = routes

    @property
    def trips(self) -> List[Trip]:
        all_trips = []
        for route in self.routes:
            route_trips = route.trips 
            all_trips += route_trips
        
        return all_trips 
    
    @property
    def stops(self) -> List[Stop]:
        all_stops = {}
        for trip in self.trips:
            for stop in trip.stops:
                if stop not in all_stops:
                    all_stops[stop] = True 
        
        return list(all_stops.keys())

    @property 
    def ridership(self):
        #413064996.3834995
        #144576773
        return sum([s.ridership for s in self.stops])

def create_network_from_GTFSRoutes(routes: List[GTFSRoute]) -> TransitNetwork:

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
        route_ridership = route.ridership 

        for trip in route.trips:
            new_stops = [all_stop_transfers[stop[0].get_id()] for stop in trip.stops if all_stop_transfers[stop[0].get_id()].is_transfer()]
            new_stop_ids = [s.get_id() for s in new_stops]

            first_stop = trip.stops[0][0]
            first_stop_id = first_stop.get_id()
            last_stop = trip.stops[-1][0]
            last_stop_id = last_stop.get_id()

            # We check if the id is in the stops because id accounts for parent stops
            if first_stop_id not in new_stop_ids:
                new_stops = [first_stop] + new_stops
            
            if last_stop_id not in new_stop_ids:
                new_stops += [last_stop]
            
            num_stops = len(trip.stops)
            num_new_stops = len(new_stops)

            if num_new_stops > num_stops:
                RootLogger.log_warning(f'Simplifying trip {trip.id} increased # of stops from {num_stops} to {num_new_stops}')
            else:
                RootLogger.log_debug(f'Trip {trip.id} reduced number of stops from {num_stops} to {num_new_stops}')

            assign_ridership_to_stops(new_stops, route_ridership)
            trip.stops = new_stops 

        simple_route = simplify_route(route)
        simple_routes.append(simple_route)
    return TransitNetwork(simple_routes) 

