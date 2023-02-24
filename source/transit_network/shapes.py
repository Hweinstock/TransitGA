import pandas as pd 
from typing import List

class Coords:

    def __init__(self, lat: float, lon: float):
        self.lat = lat 
        self.lon = lon
    
    def get_coords(self) -> List[float]:
        return [self.lat, self.lon]

class ShapePoint(Coords):

    def __init__(self, shape_id, lat: float, lon: float, sequence_num: int):
        Coords.__init__(self, lat, lon)
        self.shape_id = shape_id
        self.sequence_num = sequence_num 
    
    def to_gtfs_row(self, new_shape_id: str):
        return [new_shape_id , self.lat, self.lon, self.sequence_num]


def get_shapes_from_df(df: pd.DataFrame) -> List[ShapePoint]: 
    sorted_df = df.sort_values(by=['shape_pt_sequence'])
    shapes = []
    for index, row in sorted_df.iterrows():
        new_point = ShapePoint(shape_id = row['shape_id'], 
                   lat =row['shape_pt_lat'], 
                   lon=row['shape_pt_lon'], 
                   sequence_num=row['shape_pt_sequence'])
        
        shapes.append(new_point)
    
    return shapes