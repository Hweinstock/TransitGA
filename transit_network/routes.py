from typing import List
import pandas as pd 

from transit_network.trips import Trip
from transit_network.stops import Stop 

from root_logger import RootLogger

class BaseRoute:

    def __init__(self, id: str, name: str, city_name: str, ridership: int):
        self.id = id 
        self.name = name
        self.city_name = city_name
        self.ridership = ridership
    
    def __str__(self):
        return f'(route_id: {self.id}, route_name: {self.name}, ridership: {self.ridership})'

class GTFSRoute(BaseRoute):
    
    def __init__(self, id: str, name: str, city_name: str, ridership: int):
        BaseRoute.__init__(self, id=id, name=name, city_name=city_name, ridership=ridership)
        self.trips = []
        self.shapes_covered = {}
    
    def add_trips(self, trips):
        self.trips += trips
    
    def display_trips(self):
        return ''.join([f'{t}\n' for t in self.trips])

    def get_trips_for_route(self, trips_df: pd.DataFrame, stop_times_df: pd.DataFrame, stops_df: pd.DataFrame):

        RootLogger.log_debug(f'Getting trips for route {self.id}...')
        trip_id_for_route= trips_df.loc[(trips_df['route_id'] == self.id)]
            
        trip_objects = []
        for index, row in trip_id_for_route.iterrows():
            shape_id = row['shape_id']
            direction_id = row['direction_id']

            if shape_id not in self.shapes_covered:
                new_trip = Trip(trip_id=row['trip_id'], 
                                route_id=row['route_id'], 
                                message=row['trip_headsign'], 
                                shape_id=shape_id, 
                                direction= direction_id)
                trip_objects.append(new_trip)
                self.shapes_covered[shape_id] = True 
                RootLogger.log_debug(f'Matched shape_id {shape_id} with direction {direction_id} to route {self.id}')


        if trip_objects == []:
            RootLogger.log_warning(f'No trips found for id {self.id}')
        else:
            RootLogger.log_info(f'Successfully matched {len(trip_objects)} unique trips to route {self.id}')

        # Currently use heuristic to just take longest trips in each direction and assign them to route. 
        longest_trips = self.get_longest_trips(trip_objects, stop_times_df, stops_df)
        self.add_trips(longest_trips)
    
    def get_all_stops(self) -> List[Stop]:
        all_stops = []
        for trip in self.trips:
            all_stops += [s[0] for s in trip.stops]
        
        return all_stops


    def get_longest_trips(self, trip_objects: List[Trip], stop_times_df: pd.DataFrame, stops_df:pd.DataFrame):
        """
        Take the longest trips in each direction and assign them to the route. 
        This ensures we have a 2-1 mapping of trips to routes. 

        Args:
            trip_objects (List[Trip]): List of trip objects to consider
            stop_times_df (pd.DataFrame): Dataframe of stops on trips to determine length. 

        Returns:
            (direction_0_max, direction_1_max): where direction_0_max is longest trip in direction 0 
            and direction_1_max is the longest trip is direction 1
        """
        RootLogger.log_debug(f'Computing longest trips for route {self.id}...')

        max_len = [0, 0]
        max_trips = [None, None]

        for cur_trip in trip_objects:
            stops = cur_trip.update_stops(stop_times_df, stops_df)
            trip_len = len(stops)
            trip_dir = cur_trip.direction

            if trip_len > max_len[trip_dir]:
                max_len[trip_dir] = trip_len
                max_trips[trip_dir] = cur_trip

        RootLogger.log_info(f'Found longest trips {max_trips[0].id} and {max_trips[1].id} for route {cur_trip.route_id}, dropping all other trips.')

        if max_len[0] != max_len[1]:
            RootLogger.log_warning(f'Asymetric trips found of length {max_len[0]} and {max_len[1]} for route {cur_trip.route_id}')

        return max_trips

class SimpleRoute(BaseRoute):

    def __init__(self, id: str, name: str, city_name: str, ridership: int):
        BaseRoute.__init__(id, name, city_name, ridership)
