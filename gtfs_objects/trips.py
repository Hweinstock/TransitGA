
class Trip:

    def __init__(self, trip_id, route_id, message, shape_id, direction):
        self.id = trip_id
        self.route_id = route_id
        self.message = message
        self.shape_id = shape_id 
        self.direction = direction
    
    def __str__(self):
        return f'(trip_id: {self.id}, \
        route_id: {self.route_id}, \
        message: {self.message}, \
        shape_id: {self.shape_id}, \
        direction: {self.direction}'