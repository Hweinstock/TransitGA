from typing import List
import gtfs_kit as gk
from pathlib import Path

from root_logger import RootLogger
from preprocessing.data import DataBase
from transit_network.routes import GTFSRoute


class GTFSData(DataBase):

    def __init__(self, filepath, city_name):
        DataBase.__init__(self, filepath, city_name)
        path = Path(filepath)
        self.feed = gk.read_feed(path, dist_units='mi')

    def read_data(self):
        return self.feed

    def set_trips_for_all_routes(self, routes: List[GTFSRoute]):
        """
        Modifies route objects in place to add trips associated with them. 
        Only adds trips with unique shape_ids. 

        Args:
            routes (List[Route]): List of Routes to update. 
        """
        trips_df = self.read_data().trips 
        stop_times_df = self.read_data().stop_times
        stops_df = self.read_data().stops
        for route in routes:
            route.get_trips_for_route(trips_df, stop_times_df, stops_df)
    @property
    def num_stops(self):
        return len(self.read_data().stops.index)
    
    @property
    def num_trips(self):
        return len(self.read_data().trips.index)
    
    @property
    def num_routes(self):
        return len(self.read_data().routes.index)