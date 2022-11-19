from typing import List
import gtfs_kit as gk
from pathlib import Path

from root_logger import RootLogger
from preprocessing.data import DataBase
from gtfs_objects.trips import Trip
from gtfs_objects.routes import Route


class GTFSData(DataBase):

    def __init__(self, filepath, city_name):
        DataBase.__init__(self, filepath, city_name)
        path = Path(filepath)
        self.feed = gk.read_feed(path, dist_units='mi')

    def read_data(self):
        return self.feed

    def set_trips_for_all_routes(self, routes: List[Route]):
        """
        Modifies route objects in place to add trips associated with them. 
        Only adds trips with unique shape_ids. 

        Args:
            routes (List[Route]): List of Routes to update. 
        """
        trips_df = self.read_data().trips 
        for route in routes:
            route.get_trips_for_route(trips_df)
    
    def get_stops_for_trip_id(self, trip_id: str):
        stop_times_df = self.read_data().stop_times
        resulting_stops = stop_times_df.loc[(stop_times_df['trip_id'] == trip_id)]
        stations=[]
        for index, row in resulting_stops.iterrows():
            station_id = row['stop_id']
            trip_sequence = row['stop_sequence']
            stations.append((station_id, trip_sequence))

        return stations

            
    
    
