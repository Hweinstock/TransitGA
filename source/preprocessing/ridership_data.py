import pandas as pd  
from typing import List

from root_logger import RootLogger
from preprocessing.data import DataBase
from preprocessing.gtfs_data import GTFSData
from transit_network.routes import GTFSRoute

class RawRidershipData(DataBase):

    def read_data(self) -> pd.DataFrame:
        df = pd.read_excel(self.filepath)
        return df 

class RidershipData(DataBase):

    def __init__(self, raw_data : RawRidershipData):
        self.raw_data = raw_data
        DataBase.__init__(self, raw_data.filepath, raw_data.city_name)

    def read_data(self) -> pd.DataFrame:
        raw_df = self.raw_data.read_data()
        routes = raw_df['Route']
        total_ridership_data = []

        # Total up ridership for each route
        for route in set(routes):
            # Double dash ids exist. Currently we remove dashes and mash together
            route_lst = route.split('-')
            route_id = "".join(route_lst[:-1])
            route_name = route_lst[-1]
            subset_df = raw_df.loc[routes == route]

            # We round this value since excel data in SFMTA stores excessive decimal points. 
            total_ridership = int(subset_df['Average Daily Ridership'].sum())

            total_ridership_data.append((route_id, route_name, total_ridership))
        new_data = pd.DataFrame(total_ridership_data, 
                    columns=['route_id', 'route_name', 'total_ridership'])

        return new_data
    
    def get_matched_ids_from_gtfs(self, gtfs: GTFSData) -> List[GTFSRoute]:
        """
        Parse through GTFS data to determine which ridership routes are in GTFS data. 

        Args:
            gtfs (GTFSData): 

        Returns:
            List[Route]: List of route objects that were matched with a route in gtfs. 
        """
        ridership_df = self.read_data() 
        gtfs_routes_df = gtfs.read_data().routes
        matched_routes = []

        for index, row in ridership_df.iterrows():
            route_id = row['route_id']
            result = gtfs_routes_df.loc[(gtfs_routes_df['route_id'] == route_id)]
            if result.empty:
                RootLogger.log_warning(f'Failed to match route with id {route_id}, dropping it.')
            else:
                if len(result.index) > 1:
                    RootLogger.log_warning(f'Matched multiple routes with {route_id}, taking first found.')

                route = result.iloc[0]
                route_type = route['route_type']

                if route_type != 3:
                    RootLogger.log_info(f'Found non-bus route, dropping route with id {route_id}')
                    continue
                
                RootLogger.log_info(f'Successfuly found route with id {route_id}')
                route_long_name = route['route_long_name']
                ridership = row['total_ridership']
                new_route = GTFSRoute(id=route_id, 
                                  name=route_long_name,  
                                  ridership=ridership)
                matched_routes.append(new_route)
        
        return matched_routes

            