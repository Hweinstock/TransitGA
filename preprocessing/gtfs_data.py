from typing import List
import gtfs_kit as gk
from pathlib import Path

from root_logger import RootLogger
from preprocessing.data import DataBase


class GTFSData(DataBase):

    def __init__(self, filepath, city_name):
        DataBase.__init__(self, filepath, city_name)
        path = Path(filepath)
        self.feed = gk.read_feed(path, dist_units='mi')

    def read_data(self):
        return self.feed
    
    def get_trips_for_route(self, routes: List[str], fixed_direction=0):
        trips = self.read_data().trips 
        trip_ids = {}
        for route in routes:
            # Look at all trips on specified route. 
            # Extract out trip_id
            trip_id_for_route= trips.loc[(trips['route_id'] == route) & (trips['direction_id'] == fixed_direction)]['trip_id'].tolist()
            unique_trip_ids = list(set(trip_id_for_route))
            if unique_trip_ids == []:
                RootLogger.log_warning(f'No trips found for id {route}')
            else:
                RootLogger.log_info(f'Successfully matched {len(unique_trip_ids)} trips to {route}')
            trip_ids[route] = unique_trip_ids
        return trip_ids
    
    def get_stops_for_trip_id(self, trip_id: str):
        stop_times_df = self.read_data().stop_times
        resulting_stops = stop_times_df.loc[(stop_times_df['trip_id'] == trip_id)]
        stations=[]
        for index, row in resulting_stops.iterrows():
            station_id = row['stop_id']
            trip_sequence = row['stop_sequence']
            stations.append((station_id, trip_sequence))

        return stations

            
    
    
