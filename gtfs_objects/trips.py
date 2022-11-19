from preprocessing.gtfs_data import GTFSData
class Trip:

    def __init__(self, trip_id, route_id, message, shape_id, direction):
        self.id = trip_id
        self.route_id = route_id
        self.message = message
        self.shape_id = shape_id 
        self.direction = direction
        self.stops = []


    def get_stops(self, GtfsData: GTFSData):

        # If already computed...
        if self.stops != []:
            return self.stops 

        stop_times_df = GtfsData.read_data().stop_times
        resulting_stops = stop_times_df.loc[(stop_times_df['trip_id'] == self.id)]
        stations=[]
        for index, row in resulting_stops.iterrows():
            station_id = row['stop_id']
            trip_sequence = row['stop_sequence']
            stations.append((station_id, trip_sequence))

        self.stops = stations
        return stations
    
    def __str__(self):
        return f'(trip_id: {self.id}, \
        route_id: {self.route_id}, \
        message: {self.message}, \
        shape_id: {self.shape_id}, \
        direction: {self.direction}'