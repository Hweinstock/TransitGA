import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from math import cos, sin, pi

from typing import List, Tuple

from genetic_algorithm.zone_evaluator import Zone
from genetic_algorithm.params import ZONE_RADIUS

def convert_zones_to_df(zones: List[Zone]) -> pd.DataFrame:
    rows = []
    
    headers = ['zone_name', 'lat', 'lon', 'color']
    for zone in zones:
        cur_row = [zone.name] + zone.get_coords() + [zone.color]
        rows.append(cur_row) 
    df = pd.DataFrame(rows, columns=headers)
    df['radius'] = ZONE_RADIUS

    return df


def get_circle_radius(lat: float, lon: float) -> Tuple[List[Tuple[float, float]]]:
    N = 360 # number of discrete sample points to be generated along the circle

    radius = ZONE_RADIUS #m
    # generate points
    circle_lats, circle_lons = [], []
    for k in range(N):
        # compute
        angle = pi*2*k/N
        dx = radius*cos(angle)
        dy = radius*sin(angle)
        circle_lats.append(lat + (180/pi)*(dy/6378137))
        circle_lons.append(lon + (180/pi)*(dx/6378137)/cos(lat*pi/180))
    circle_lats.append(circle_lats[0])
    circle_lons.append(circle_lons[0])

    return circle_lats, circle_lons

def plot_from_df(df: pd.DataFrame):

    fig = px.scatter_mapbox(df, 
                            lat="lat", 
                            lon="lon", 
                            hover_name="zone_name", 
                            hover_data=["zone_name", "lat", "lon"],
                            size="radius",
                            zoom=10)

    for index, row in df.iterrows():
        circle_lats, circle_lons = get_circle_radius(row['lat'], row['lon'])
        fig.add_trace(go.Scattermapbox(
                    lat=circle_lats,
                    lon=circle_lons,
                    line={'width': 5},
                    mode='markers+lines', 
                    name=row['zone_name'],
                    marker={'size':1, 'color': row['color']})
        )
        
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def plot_zones(zones: List[Zone]) -> None:
    df = convert_zones_to_df(zones)
    plot_from_df(df)