from typing import List 

from root_logger import RootLogger
from transit_network.shapes import ShapePoint

def stop_from_stop_row_data(row):
    id = row['stop_id']
    stop_lat = row['stop_lat']
    stop_lon = row['stop_lon']
    stop_name = row['stop_name']
    if 'parent_station' in row:
        parent_station = row['parent_station']
    else:
        parent_station = None 
    
    return Stop(id= id, name=stop_name, location=(stop_lat, stop_lon), parent_id=parent_station)


class Stop:

    def __init__(self, id, name, location, parent_id=None):
        self.id = id 
        self.name = name
        self.parent_id = parent_id
        self.matches_trips = []
        self.routes = []
        self.trip_sequences = {} # This is set when we simplify the trip. 
        self.ridership = 0
        self.location = location
    
    def add_transfer_route(self, new_route: str):
        self.routes += [new_route]

    @property
    def location_lat(self):
        return self.location[0]

    @property
    def location_lon(self):
        return self.location[1]

    def distance_to_point(self, point: ShapePoint):
        # Standard distance formula for two points in two dimensions
        return abs((point.lat-self.location_lat)**2 + (point.lon-self.location_lon)**2)**(0.5)

    def is_transfer(self):
        if len(self.routes) == 0:
            RootLogger.log_warning(f'Stop {self.id} with parent {self.parent_id} has no routes!')
        return len(self.routes) > 1
    
    def get_id(self):
        if self.parent_id is not None:
            return self.parent_id 
        else:
            return self.id 
    
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
    
