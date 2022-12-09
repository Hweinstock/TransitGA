#from preprocessing.gtfs_data import GTFSData

from typing import List
import pandas as pd 

from transit_network.stops import Stop, stop_from_stop_row_data
from transit_network.shapes import ShapePoint
from root_logger import RootLogger

class BaseTrip:
    
    def __init__(self, trip_id, route_id, message, direction):
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


class SimpleTrip(BaseTrip):

    def __init__(self, trip_id, route_id, message, direction, shape_points, stops, ridership):
        BaseTrip.__init__(self, trip_id, route_id, message, direction)
        self.stops = stops
        self.shape_points = shape_points

    @property
    def flattened_shape_points(self):
        return [Point for partition in self.shape_points for Point in partition]

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
    
    def update_stops(self, stop_times_df: pd.DataFrame, stops_df: pd.DataFrame) -> List[Stop]:
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

    def __str__(self):
        return f'(trip_id: {self.id}, \
        route_id: {self.route_id}, \
        message: {self.message}, \
        shape_id: {self.shape_id}, \
        direction: {self.direction}, \
        ridership: {self.ridership}'


def partition_shape_points(shape_points: List[ShapePoint], stops: List[Stop]) -> List[List[ShapePoint]]:
    partition = []
    cur_stop_points = []

    num_stops = len(stops)
    num_points = len(shape_points)

    cur_closest_stop_index = 0
    prev_dist_to_stop = 0

    local_min = float('inf')
    for point in shape_points:
        # Current stop that is closest
        closest_stop = stops[cur_closest_stop_index]

        # Distance from stop to ShapePoint 
        cur_dist_to_cur_stop = closest_stop.distance_to_point(point)
        local_min = min(local_min, cur_dist_to_cur_stop)
        if cur_dist_to_cur_stop == 0.0:
            RootLogger.log_debug(f'Found shape point on top of stop!')

        # If this distance is increasing i.e. we are moving away from stop, move to next stop. 
        if cur_dist_to_cur_stop > prev_dist_to_stop:
            partition.append(cur_stop_points)

            cur_stop_points = []
            cur_closest_stop_index += 1
            if cur_closest_stop_index == num_stops:
                cur_closest_stop_index -= 1
                RootLogger.log_warning(f'Hit final stop, but at point {point.sequence_num} out of {num_points}. \
                    decrementing cur_closest_stop_index')

            closest_stop = stops[cur_closest_stop_index]
            cur_dist_to_cur_stop = closest_stop.distance_to_point(point)

        prev_dist_to_stop = cur_dist_to_cur_stop
        cur_stop_points.append(point)
    
    # Add final stop
    partition.append(cur_stop_points)
    cur_closest_stop_index += 1
    RootLogger.log_debug(f'Found minimum distance: {local_min}')
    if cur_closest_stop_index < num_stops:
        RootLogger.log_error(f'Invalid partition generated for stops. Made it to stop {cur_closest_stop_index} out of {num_stops}')
    return partition

def simplify_trip(original_trip: GTFSTrip, new_stops: List[Stop], route_ridership: int, shape_points: List[ShapePoint]) -> SimpleTrip:
    
    # We set the trip sequence values for stop, this is used in exporting to gtfs. 
    for index, stop in enumerate(new_stops):
        # want start sequence to start at 1 -> n
        stop.trip_sequences[original_trip.id] = index + 1 

    seperated_shape_points = partition_shape_points(shape_points, new_stops)
    trip_ridership = route_ridership / 2.0
    assign_ridership_to_stops(new_stops, trip_ridership)
    NewTrip = SimpleTrip(trip_id=original_trip.id, 
                              route_id=original_trip.route_id,
                              message=original_trip.message, 
                              direction=original_trip.direction, 
                              shape_points=seperated_shape_points,
                              stops=new_stops, 
                              ridership= trip_ridership)
    return NewTrip


def assign_ridership_to_stops(StopList: List[Stop], trip_ridership: int):
    num_of_stops = len(StopList)

    # We incremement since transfer stops will naturally occur multiple times. 
    # This rewards transfer stops by counting them on each route they transfer for. 
    for stop in StopList:
        stop.ridership += trip_ridership / num_of_stops