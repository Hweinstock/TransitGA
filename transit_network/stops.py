from typing import List, Dict
from math import dist 

from root_logger import RootLogger
from transit_network.shapes import ShapePoint

def stop_from_stop_row_data(row, route_id):
    id = row['stop_id']
    stop_lat = row['stop_lat']
    stop_lon = row['stop_lon']
    stop_name = row['stop_name']
    if 'parent_station' in row:
        parent_station = row['parent_station']
    else:
        parent_station = None 
    
    return Stop(id= id, name=stop_name, location=(stop_lat, stop_lon), parent_id=parent_station, routes=[route_id])


class Stop:

    def __init__(self, id: str, name: str, location: tuple, parent_id: str, routes: List[str]):
        self.id = id 
        self.name = name
        self.parent_id = parent_id
        self.matches_trips = []
        self.routes = routes
        self.trip_sequences = {} # This is set when we simplify the trip. 
        self.ridership = 0
        self.location = location
    
    def add_transfer_routes(self, new_routes: List[str]):
        self.routes += [new_routes]

    @property
    def location_lat(self):
        return self.location[0]

    @property
    def location_lon(self):
        return self.location[1]

    def distance_to_stop(self, other_stop) -> float:
        x_1 = self.location_lat
        x_2 = other_stop.location_lat 

        y_1 = self.location_lon
        y_2 = other_stop.location_lon

        return dist([x_1, y_1], [x_2, y_2])
        
    def distance_to_point(self, point: ShapePoint) -> float:
        x_1 = self.location_lat
        x_2 = point.lat

        y_1 = self.location_lon
        y_2 = point.lon

        return dist([x_1, y_1], [x_2, y_2])

    def merge_with(self, second_stop):
        if self.id == second_stop.id:
            # Found duplicate stops
            self.add_transfer_routes(second_stop.routes)
            return self
        elif self.parent_id == second_stop.parent_id and self.parent_id is not None:
            # Found stops with common parent stop
            new_id = self.parent_id
            new_name = self.name + '-' + second_stop.name
            new_parent = None
        else:
            # We found stops within threshhold distance. 
            new_id = self.id + '-' + second_stop.id
            new_name = self.name + '-' + second_stop.name
            if self.parent_id is not None and second_stop.parent_id is not None:
                RootLogger.log_warning(f'Merging stops within threshold distance with two distinct parents \
                     {self.parent_id} and {second_stop.parent_id}.')
            new_parent = self.parent_id if second_stop.parent_id is None else second_stop.parent_id
        
        new_routes = self.routes + second_stop.routes 
        new_lat = (self.location_lat + second_stop.location_lat) / 2.0
        new_lon = (self.location_lon + second_stop.location_lon) / 2.0

        return Stop(id= new_id, name=new_name, location=(new_lat, new_lon), parent_id=new_parent, routes=new_routes)

    def is_transfer(self):
        if len(self.routes) == 0:
            RootLogger.log_warning(f'Stop {self.id} with parent {self.parent_id} has no routes!')
        return len(self.routes) > 1
    
    def get_id(self):
        if self.parent_id is not None:
            return self.parent_id 
        else:
            return self.id 
    @property
    def all_ids(self):
        return self.get_id().split('-')
    
    def to_stop_time_gtfs_rows(self):
        rows = []
        for trip_id in list(self.trip_sequences.keys()):
            # set 0, 0 arrival depature since we don't care about time. 
            cur_row = [trip_id, 0, 0, self.id, self.trip_sequences[trip_id]]
            rows.append(cur_row)
        
        return rows
    
    def to_gtfs_row(self):
        return [self.id, self.name, self.location_lat, self.location_lon, self.parent_id]

    def __str__(self) -> str:
        return f'(stop_id: {self.id}, stop_name: {self.name}, parent_stop: {self.parent_id}, routes: {self.routes})'
    

def map_ids_to_obj(stop_objs: List[Stop]) -> Dict[int, Stop]:
    """Generates mapping from merged stop ids to stop objs for easy lookup from original stops to new merged stops.  

    Args:
        stop_objs (List[Stop]): merged stops

    Raises:
        KeyError: If stop ids found. 

    Returns:
        Dict[int, Stop]: Mapping from ids to stops. 
    """
    mapping_dict = {}
  
    for stop in stop_objs:
        cur_ids = stop.all_ids
        for id in cur_ids:
            if id in mapping_dict:
                RootLogger.log_error('Duplicate stop ids in merged stop objects!')
                raise KeyError
            else:
                mapping_dict[id] = stop
    
    return mapping_dict
