
class Route:
    
    def __init__(self, id, name):
        self.id = id 
        self.name = name
    
    def __str__(self):
        return f'(route_id: {self.id}, route_name: {self.name}'
    
