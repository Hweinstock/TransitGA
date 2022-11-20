

def stop_from_stop_row_data(row):
    id = row['stop_id']
    stop_name = row['stop_name']
    if 'parent_station' in row:
        parent_station = row['parent_station']
    else:
        parent_station = None 
    
    return Stop(id= id, name=stop_name, parent_id=parent_station)

class Stop:

    def __init__(self, id, name, parent_id=None):
        self.id = id 
        self.name = name
        self.parent_id = parent_id
        self.matches_trips = []
    
    def __str__(self) -> str:
        return f'(stop_id: {self.stop_id}, stop_name: {self.stop_name}, parent_stop: {self.parent_id}'

    
