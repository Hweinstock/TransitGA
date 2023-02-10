#Import the gtfs-kit module
import gtfs_kit as gk
from pathlib import Path
import warnings 
import pandas as pd
from typing import List

from root_logger import RootLogger


def generate_diagram(zip_path: str, output_filename: str, route_ids: List[int] = None, include_stops=True):
    RootLogger.log_debug(f'Generating diagram for {zip_path} with routes restricted to {route_ids}...')
    output_filename = f'{output_filename}.html'
    warnings.simplefilter('ignore')
    path = Path(zip_path)
    feed = gk.read_feed(path, dist_units='km')

    if route_ids is None:
        route_ids = feed.routes.route_id.iloc[:]
    stop_route = feed.map_routes(route_ids, include_stops=include_stops)
    stop_route.save(output_filename)
    RootLogger.log_debug(f'Diagram saved to {output_filename}.')

# warnings.simplefilter('ignore')

# #Declare the directory path for the GTFS zip file
# my_path = Path('output_gtfs.zip')
# orig_path = Path('data/gtfs_data/SFMTA.zip')

# #Read the feed with gtfs-kit
# my_feed = gk.read_feed(my_path, dist_units='km')
# original_feed = gk.read_feed(orig_path, dist_units='km')
# #df = feed.validate() 
# #df.to_csv('errors.csv')

# print('Process:: mapping stop_route')
# my_stop_route_map = my_feed.map_routes(my_feed.routes.route_id.iloc[:], include_stops=True)
# # orig_stop_route_map = original_feed.map_routes(original_feed.routes.route_id.iloc[:], include_stops=True)

# my_stop_route_map.save('my_stop_route_map.html')
# orig_stop_route_map.save('original_stop_route_map.html')

# print(feed.stop_times)
