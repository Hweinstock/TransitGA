from gtfs_objects.trips import Trip
from root_logger import RootLogger

class Route:
    
    def __init__(self, id, name, city_name, ridership):
        self.id = id 
        self.name = name
        self.city_name = city_name
        self.trips = []
        self.ridership = ridership
        self.shapes_covered = {}
    
    def add_trips(self, trips):
        self.trips += trips

    def __str__(self):
        return f'(route_id: {self.id}, route_name: {self.name}, ridership: {self.ridership})'
    
    def display_trips(self):
        return ''.join([f'{t}\n' for t in self.trips])

    def get_trips_for_route(self, trips_df):
        trip_id_for_route= trips_df.loc[(trips_df['route_id'] == self.id)]
            
        trip_objects = []
        for index, row in trip_id_for_route.iterrows():
            trip_id = row['trip_id']
            route_id = row['route_id']
            trip_headwaysign = row['trip_headsign']
            shape_id = row['shape_id']
            direction_id = row['direction_id']

            if shape_id not in self.shapes_covered:
                new_trip = Trip(trip_id=trip_id, 
                                route_id=route_id, 
                                message=trip_headwaysign, 
                                shape_id=shape_id, 
                                direction= direction_id)
                trip_objects.append(new_trip)
                self.shapes_covered[shape_id] = True 
                RootLogger.log_debug(f'Matched shape_id {shape_id} to route {route_id}')


        if trip_objects == []:
            RootLogger.log_warning(f'No trips found for id {self.id}')
        else:
            RootLogger.log_info(f'Successfully matched {len(trip_objects)} unique trips to route {self.id}')

        self.add_trips(trip_objects)
    
