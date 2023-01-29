#from preprocessing.gtfs_data import GTFSData

from typing import List
import pandas as pd 

from transit_network.stops import Stop, stop_from_stop_row_data
from transit_network.shapes import ShapePoint
from root_logger import RootLogger
from preprocessing.partition_shape_points import partition_shape_points

class BaseTrip:
    
    def __init__(self, trip_id: str, route_id: str, message: str, direction: int):
        self.id = trip_id
        self.route_id = route_id
        self.message = message
        self.direction = direction
    
    @property
    def ridership(self):
        return sum([s.ridership for s in self.stops])
    
    def display_stops(self):
        result_str= '['
        for stop_id, order in self.stops[:-1]:
            result_str += f'{stop_id} -> '
        
        result_str += str(self.stops[-1][0])
        return result_str + ']'
    
    def get_index_of_stop_id(self, target_id: str):
        for index, cur_stop in enumerate(self.stops):
            if cur_stop.id == target_id: 
                return index 

        RootLogger.log_error(f'Unable to locate shared stop {target_id} in trip {self.id}')
        return None 
    
    def __eq__(self, other_obj: object) -> bool:
        return other_obj.id == self.id


class SimpleTrip(BaseTrip):

    def __init__(self, trip_id: str, route_id: str, message: str, 
                       direction: int, shape_points: List[List[ShapePoint]],
                       stops: List[str]):
        BaseTrip.__init__(self, trip_id, route_id, message, direction)
        self.stops = stops
        self.shape_points = shape_points
        self.dead = False
        self.set_sequence_values_for_stops()
        
    @property
    def flattened_shape_points(self):
        return [Point for partition in self.shape_points for Point in partition]
    
    @property
    def unique_stop_ids(self):
        return [stop.id for stop in self.stops]

    def count_intersections(self):
        unique_trips = {} 
        for stop in self.stops:
            for other_trip in stop.trip_sequences.keys():
                if other_trip not in unique_trips:
                    unique_trips[other_trip] = True 
        
        return len(unique_trips)

    def set_sequence_values_for_stops(self):
        # We set the trip sequence values for stop, this is used in exporting to gtfs. 
        for index, stop in enumerate(self.stops):
        # want start sequence to start at 1 -> n
            stop.trip_sequences[self.id] = index + 1 

    def does_share_stop_with(self, other_trip) -> str or None:
        # TODO: More efficient way to do this I believe. 
        for id_1 in self.unique_stop_ids:
            for id_2 in other_trip.unique_stop_ids:
                if id_1 == id_2:
                    return id_1
        return None 

    def to_gtfs_row(self):
        # Give all trips service id 0, since we don't care about what time they run, only geometry. 
        # We make shape_id to the same as trip_id with 00 on the end. 
        return [self.route_id, 0, self.id, self.direction, self.custom_shape_id, self.message]
    
    def get_shapes_rows(self):
        rows = []
        for index, shape in enumerate(self.flattened_shape_points):
            shape.sequence_num = index + 1
            new_row = shape.to_gtfs_row(self.custom_shape_id)
            rows.append(new_row)
    
        return rows
        
    @property
    def custom_shape_id(self):
        return self.id+'00'

class GTFSTrip(BaseTrip):

    def __init__(self, trip_id, route_id, message, shape_id, direction):
        BaseTrip.__init__(self, trip_id, route_id, message, direction)
        self.shape_id = shape_id 
        self.stops = [] # In Tuple format: (Stop, seq in trip)

    def set_stops(self, stops: List[Stop], shapes_df: pd.DataFrame):
        self.stops = stops

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
                RootLogger.log_debug(f'Successfully matched stop with id {stop_id} to trip {self.id}')
            stop_row = stop_data.iloc[0]
            stop_obj = stop_from_stop_row_data(stop_row, self.route_id)
            stations.append((stop_obj, trip_sequence))

        self.stops = stations
        return stations

    def __str__(self):
        return f'(trip_id: {self.id}, \
        route_id: {self.route_id}, \
        message: {self.message}, \
        shape_id: {self.shape_id}, \
        direction: {self.direction}, \
        ridership: {self.ridership}'

def simplify_trip(original_trip: GTFSTrip, new_stops: List[Stop], route_ridership: int, shape_points: List[ShapePoint]) -> SimpleTrip:

    seperated_shape_points = partition_shape_points(shape_points, new_stops)
    trip_ridership = route_ridership / 2.0

    # Move ridership data to the stops
    assign_ridership_to_stops(new_stops, trip_ridership)

    NewTrip = SimpleTrip(trip_id=original_trip.id, 
                              route_id=original_trip.route_id,
                              message=original_trip.message, 
                              direction=original_trip.direction, 
                              shape_points=seperated_shape_points,
                              stops=new_stops)
    return NewTrip

def assign_ridership_to_stops(StopList: List[Stop], trip_ridership: int):
    num_of_stops = len(StopList)

    # We incremement since transfer stops will naturally occur multiple times. 
    # This rewards transfer stops by counting them on each route they transfer for. 
    for stop in StopList:
        stop.ridership += trip_ridership / num_of_stops

def common_transfer_point(trip_A: SimpleTrip, trip_B: SimpleTrip) -> str or None:
    # Trips must be the same direction
    if trip_A.direction != trip_B.direction:
        return None 

    # Trip ids must be distinct (not breeding trip with itself)
    if trip_A.id == trip_B.id:
        return None 
    
    shared_stop = trip_A.does_share_stop_with(trip_B)
    
    # No common transfer stops
    if shared_stop is None:
        return shared_stop 
    
    return shared_stop