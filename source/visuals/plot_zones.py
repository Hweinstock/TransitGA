import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List 

from genetic_algorithm.zone_evaluator import Zone
from genetic_algorithm.params import ZONE_RADIUS

def convert_zones_to_df(zones: List[Zone]) -> pd.DataFrame:
    rows = []
    
    headers = ['zone_name', 'lat', 'lon']
    for zone in zones:
        cur_row = [zone.name] + zone.get_coords()
        rows.append(cur_row) 
    df = pd.DataFrame(rows, columns=headers)
    df['radius'] = ZONE_RADIUS

    return df

def plot_from_df(df: pd.DataFrame):

    color_scale = [(0, 'orange'), (1,'red')]

    fig = px.scatter_mapbox(df, 
                            lat="lat", 
                            lon="lon", 
                            hover_name="zone_name", 
                            hover_data=["zone_name", "lat", "lon"],
                            color_continuous_scale=color_scale,
                            size="radius",
                            zoom=10)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def plot_zones(zones: List[Zone]) -> None:
    df = convert_zones_to_df(zones)
    plot_from_df(df)