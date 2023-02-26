from typing import List, Tuple
import pandas as pd 
import os
import shutil
from copy import deepcopy
from statistics import mean

from transit_network.routes import SimpleRoute, GTFSRoute, simplify_route
from transit_network.stops import Stop, map_ids_to_obj
from transit_network.trips import GTFSTrip, simplify_trip, SimpleTrip
from transit_network.shapes import get_shapes_from_df
from genetic_algorithm.family import Family
from preprocessing.determine_transfers import new_determine_transfers
import preprocessing.gtfs_data as GTFS
from utility.root_logger import RootLogger

class TransitNetwork:

    def __init__(self, routes: List[SimpleRoute], id : str = '0'):
        self.id = id
        self.routes = routes

        # Pre-compute all of these such that we don't recompute.
        self.trips = self.get_trips()
        self.stops = self.get_stops()
        self.num_routes = self.get_num_routes()
        self.num_trips = self.get_num_trips()
        self.num_stops = self.get_num_stops()
        self.num_trips = self.get_num_trips()
        self.ridership = self.get_ridership()
        self.coverage = self.get_coverage()
        self.ridership_density_score = self.get_ridership_density_score()
        # self.set_transfer_points()

    def get_copy(self):
        # Make this a deepcopy. 
        return deepcopy(self)

    def get_num_stops(self) -> int:
        return len(self.stops)
    
    def get_num_trips(self) -> int:
        return len(self.trips)
    
    def get_num_routes(self) -> int:
        return len(self.routes)

    def get_trips(self) -> List[GTFSTrip]:
        all_trips = []
        for route in self.routes:
            route_trips = route.trips 
            all_trips += route_trips
        
        return all_trips 
    
    def get_stops(self) -> List[Stop]:
        all_stops = {}
        for trip in self.trips:
            for stop in trip.stops:
                if stop.id not in all_stops:
                    all_stops[stop.id] = stop 
        return list(all_stops.values())

    def get_ridership(self) -> float:
        return sum([s.ridership for s in self.stops])
    
    def get_coverage(self) -> int:
        avg_transfers_per_stop = mean([len(s.routes) for s in self.stops])
        return len(self.stops) * avg_transfers_per_stop

    def get_ridership_density_score(self) -> float:
        score = 0
        for trip in self.trips:
            intersections = trip.count_intersections()
            ridership = trip.ridership 

            score += intersections * ridership
        return score 

    def search_for_stop(self, stop_id: str) -> Tuple[SimpleRoute, SimpleTrip]:
        for cur_route in self.routes:
            for cur_trip in cur_route.trips:
                if stop_id in cur_trip.unique_stop_ids:
                    return (cur_route.id, cur_trip.id)
        
        return None, None
    
    def get_stop_transfers(self, target_stop_id: str) -> List[str]:
        stop_matches = [s for s in self.stops if s.id == target_stop_id]
        num_matches = len(stop_matches)
        if num_matches == 0:
            RootLogger.log_error(f'Failed to find stop of id {target_stop_id} in network {self.id}!')
            raise KeyError
        
        if num_matches > 1:
            RootLogger.log_warning(f'Found multiple stops of same id {target_stop_id} in network {self.id}, returning first one.')

        return stop_matches[0].routes

    def has_stop(self, stop_id: str) -> bool:
        all_stops_id = [s.id for s in self.get_stops()]
        return stop_id in all_stops_id

    def set_transfer_points(self) -> None:
        # Reset all transfer routes. 
        for stop in self.stops:
            stop.routes = [] 

        for cur_trip in self.trips:
            for stop in cur_trip.stops:
                stop.add_transfer_routes([cur_trip.route_id])

    def lookup_route_by_id(self, id: str) -> SimpleRoute or None:
        matches = [r for r in self.routes if r.id == id]
        if len(matches) == 0:
            RootLogger.log_error(f'Unable to find route with id {id} in network {self.id}.')
            return None
        if len(matches) > 1:
            RootLogger.log_warning(f'Found duplicate routes with id {id} in network {self.id}. Returning first one. ')
            
        return matches[0]

    def __str__(self):
        num_routes = len(self.routes)
        num_trips = len(self.trips)
        num_stops = len(self.stops)

        # routes_str = "\n".join([str(r) for r in self.routes])
        report_str = f'(TransitNetwork[routes: {num_routes}, trips: {num_trips}, stops: {num_stops}, ridership: {self.ridership}])'
        return report_str

    def write_to_gtfs(self, folder: str):

        def rows_to_file(rows, headers, filename):
            df = pd.DataFrame(rows, columns=headers)
            raw_csv_text = df.to_csv(index=False)
            text_file = os.path.join(folder, filename+'.txt')

            RootLogger.log_debug(f'Outputting gtfs file to {text_file} in directory {folder}.')

            with open(text_file, 'w') as output:
                output.write(raw_csv_text)
        if not os.path.exists(folder):
            os.makedirs(folder)

        route_rows = [r.to_gtfs_row() for r in self.routes]
        rows_to_file(route_rows, GTFS.ROUTE_FILE_HEADERS, 'routes')

        trip_rows = [t.to_gtfs_row() for t in self.trips]
        rows_to_file(trip_rows, GTFS.TRIPS_FILE_HEADERS, 'trips')

        shapes_rows = []
        for trip in self.trips:
            shapes_rows += trip.get_shapes_rows()
        rows_to_file(shapes_rows, GTFS.SHAPES_FILE_HEADERS, 'shapes')

        stop_times_rows = []
        for s in self.stops:
            stop_times_rows += s.to_stop_time_gtfs_rows()
        rows_to_file(stop_times_rows, GTFS.STOP_TIMES_FILE_HEADERS, 'stop_times')

        stop_rows = [s.to_gtfs_row() for s in self.stops]
        rows_to_file(stop_rows, GTFS.STOP_FILE_HEADERS, 'stops')
        RootLogger.log_info(f'Constructed GTFS files, now zipping into {folder}.zip')
        shutil.make_archive(folder, 'zip', folder)

def create_network_from_GTFSRoutes(routes: List[GTFSRoute], shapes_df: pd.DataFrame) -> TransitNetwork:

    transfer_stops_obj = new_determine_transfers(routes)
    id_to_obj_map = map_ids_to_obj(transfer_stops_obj)
    # Update stop objects so that they all have transfer points set. 
    simple_routes = []
    for route in routes:
        RootLogger.log_info(f'Simplifying trips for route {route.id}')
        new_trips = []
        for trip in route.trips:
            new_stops = [] 

            for stop in trip.stops:
                stop_id = stop[0].get_id()
                cur_stop = id_to_obj_map[stop_id]
                if cur_stop.is_transfer(): 
                    RootLogger.log_debug(f'Identified transfer stop {cur_stop.id} with {len(cur_stop.routes)} transfers.')
                    new_stops.append(cur_stop)
            
            # We want to add endpoint to the trips
            first_stop = trip.stops[0][0]
            first_stop_id = first_stop.get_id()
            last_stop = trip.stops[-1][0]
            last_stop_id = last_stop.get_id()

            # We check if the id is in the stops because id accounts for parent stops
            if first_stop_id not in id_to_obj_map:
                new_stops = [first_stop] + new_stops
            
            if last_stop_id not in id_to_obj_map:
                new_stops += [last_stop]

            # Debugging Information
            num_stops = len(trip.stops)
            num_new_stops = len(new_stops)

            if num_new_stops > num_stops:
                RootLogger.log_warning(f'Simplifying trip {trip.id} increased # of stops from {num_stops} to {num_new_stops}')
            else:
                RootLogger.log_info(f'Trip {trip.id} reduced number of stops from {num_stops} to {num_new_stops}')

            # Shape Information for each trip. 
            shape_id = trip.shape_id
            shape_points = get_shapes_from_df(shapes_df.loc[shapes_df['shape_id'] == shape_id])
            
            RootLogger.log_info(f'Identified {len(shape_points)} shape points for trip {trip.id}.')

            new_trip = simplify_trip(trip, new_stops, route.ridership, shape_points)
            new_trips.append(new_trip)

        simple_route = simplify_route(route, new_trips)
        simple_routes.append(simple_route)

    return TransitNetwork(simple_routes, id='-1') 

def create_network_from_trips(trips: List[SimpleTrip], id: str):
    routes_dict = {} # maps route-ids to the trips referencing them

    for trip in trips:
        route_id = trip.route_id
        if route_id in routes_dict:
            routes_dict[route_id].append(trip)
        else:
            routes_dict[route_id] = [trip]
        
        for stop in trip.stops:
            stop.routes = [] # Reset transfer points to none
    
    new_routes = []
    for route_id in routes_dict:
        new_route = SimpleRoute(route_id, None)
        route_trips = routes_dict[route_id]

        # Set transfer points
        for trip in route_trips:
            trip.set_stop_transfer_points()

        new_route.add_trips(routes_dict[route_id])
        new_routes.append(new_route)
        
    return TransitNetwork(new_routes, id)
    

