from typing import List 
import pandas as pd 
import os
import shutil
from copy import deepcopy
import pickle

from transit_network.routes import SimpleRoute, GTFSRoute, simplify_route
from transit_network.stops import Stop, map_ids_to_obj
from transit_network.trips import GTFSTrip, simplify_trip, SimpleTrip
from transit_network.shapes import ShapePoint, get_shapes_from_df
from preprocessing.determine_transfers import new_determine_transfers

from root_logger import RootLogger

ROUTE_FILE_HEADERS = ['route_id' ,'route_short_name', 'route_long_name', 'route_type']
TRIPS_FILE_HEADERS = ['route_id', 'service_id', 'trip_id', 'direction_id', 'shape_id', 'trip_headsign']
STOP_TIMES_FILE_HEADERS = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence']
STOP_FILE_HEADERS = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'parent_station']
SHAPES_FILE_HEADERS = ['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']

class TransitNetwork:

    def __init__(self, routes: List[SimpleRoute], id : str = '0'):
        self.id = id
        self.routes = routes

    def get_copy(self):
        # Make this a deepcopy. 
        return deepcopy(self)

    @property
    def num_stops(self):
        return len(self.stops)
    
    @property
    def num_trips(self):
        return len(self.trips)
    
    @property
    def num_routes(self):
        return len(self.routes)

    @property
    def trips(self) -> List[GTFSTrip]:
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
        return sum([s.ridership for s in self.stops])
    
    @property
    def coverage(self):
        return len(self.stops)
    
    def __str__(self):
        num_routes = len(self.routes)
        num_trips = len(self.trips)
        num_stops = len(self.stops)

        routes_str = "\n".join([str(r) for r in self.routes])
        report_str = f'(TransitNetwork[routes: {num_routes}, trips: {num_trips}, stops: {num_stops}, ridership: {self.ridership}])'
        return routes_str + report_str

    def write_to_pickle(self, filename=id):
        with open(filename, 'wb') as output:
            pickle.dump(self, output)

    def write_to_gtfs(self, folder='output_gtfs'):

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
        rows_to_file(route_rows, ROUTE_FILE_HEADERS, 'routes')

        trip_rows = [t.to_gtfs_row() for t in self.trips]
        rows_to_file(trip_rows, TRIPS_FILE_HEADERS, 'trips')

        shapes_rows = []
        for trip in self.trips:
            shapes_rows += trip.get_shapes_rows()
        rows_to_file(shapes_rows, SHAPES_FILE_HEADERS, 'shapes')

        stop_times_rows = []
        for s in self.stops:
            stop_times_rows += s.to_stop_time_gtfs_rows()
        rows_to_file(stop_times_rows, STOP_TIMES_FILE_HEADERS, 'stop_times')

        stop_rows = [s.to_gtfs_row() for s in self.stops]
        rows_to_file(stop_rows, STOP_FILE_HEADERS, 'stops')
        RootLogger.log_info(f'Constructed GTFS files, now zipping into {folder}.zip')
        shutil.make_archive(folder, 'zip', folder)

def create_network_from_GTFSRoutes(routes: List[GTFSRoute], shapes_df: pd.DataFrame) -> TransitNetwork:

    transfer_stops_obj = new_determine_transfers(routes)
    print('# of transfer stops', len(transfer_stops_obj))
    id_to_obj_map = map_ids_to_obj(transfer_stops_obj)
    unique_shapes = {}
    # Update stop objects so that they all have transfer points set. 
    simple_routes = []
    for route in routes:
        RootLogger.log_info(f'Simplifying trips for route {route.id}')
        new_trips = []
        for trip in route.trips:
            # Currently not using. 
            # if trip.shape_id in unique_shapes:
            #     RootLogger.log_warning(f'Found duplicate shaped trip {trip.id} on route {route.id}. Dropping this trip.')
            #     continue 
            # else:
            #     unique_shapes[trip.shape_id] = True

            new_stops = [] 

            for stop in trip.stops:
                stop_id = stop[0].get_id()
                cur_stop = id_to_obj_map[stop_id]
                if cur_stop.is_transfer(): 
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

    return TransitNetwork(simple_routes, id='0') 

def create_network_from_trips(trips: List[SimpleTrip], id: str):
    routes_dict = {} # maps route-ids to the trips referencing them
    for trip in trips:
        route_id = trip.route_id
        if route_id in routes_dict:
            routes_dict[route_id].append(trip)
        else:
            routes_dict[route_id] = [trip]
    
    new_routes = []
    for route_id in routes_dict:
        new_route = SimpleRoute(route_id, None)
        new_route.add_trips(routes_dict[route_id])
        new_routes.append(new_route)
        
    return TransitNetwork(new_routes, id)

def read_network_from_pickle(filename: str) -> TransitNetwork:
    with open(filename, 'rb') as input_file:
        obj = pickle.load(input_file)

    return obj
    

