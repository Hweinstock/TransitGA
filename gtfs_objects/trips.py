#from preprocessing.gtfs_data import GTFSData

from typing import List
import pandas as pd 

from gtfs_objects.stops import Stop, stop_from_stop_row_data
from root_logger import RootLogger

class Trip:

    def __init__(self, trip_id, route_id, message, shape_id, direction):
        self.id = trip_id
        self.route_id = route_id
        self.message = message
        self.shape_id = shape_id 
        self.direction = direction
        self.stops = []


    def get_stops(self, stop_times_df: pd.DataFrame, stops_df: pd.DataFrame) -> List[Stop]:
        """
        Return a list of stop ids associated with trip. 

        Returns:
            List[str]: stop_ids
        """

        # If already computed...
        if self.stops != []:
            return self.stops 

        resulting_stops = stop_times_df.loc[(stop_times_df['trip_id'] == self.id)]
        stations=[]
        for index, row in resulting_stops.iterrows():
            stop_id = row['stop_id']
            trip_sequence = row['stop_sequence']
            stop_data = stops_df.loc[(stops_df['stop_id'] == stop_id)]

            if len(stop_data.index) == 0:
                RootLogger.log_warning(f'Failed to find stop with id {stop_id} on trip {self.id} from route {self.route_id}, dropping it.')
                continue

            if len(stop_data.index) > 1:
                RootLogger.log_warning(f'Matched multiple stop with id {stop_id} on trip {self.id} from route {self.route_id}, dropping rest of them.')
            else:
                RootLogger.log_info(f'Successfully matched stop with id {stop_id} to trip {self.id}')
            stop_row = stop_data.iloc[0]
            stop_obj = stop_from_stop_row_data(stop_row)
            stations.append((stop_obj, trip_sequence))

        self.stops = stations
        return stations
    
    def display_stops(self):
        result_str= '['
        for stop_id, order in self.stops[:-1]:
            result_str += f'{stop_id} -> '
        
        result_str += str(self.stops[-1][0])
        return result_str + ']'

    def __str__(self):
        return f'(trip_id: {self.id}, \
        route_id: {self.route_id}, \
        message: {self.message}, \
        shape_id: {self.shape_id}, \
        direction: {self.direction}'