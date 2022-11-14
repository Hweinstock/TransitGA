from pathlib import Path

class DataBase:
    """
    Data Skeleton class to generalize data objects throughout the project. 
    """

    def __init__(self, filepath : str , city_name: str):
        self.filepath = filepath
        self.filetype = Path(filepath).suffix
        self.city_name = city_name

    def read_data(self):
        """
        Skeleton method to be implemented by children classes. 

        Returns:
            NoneType: 
        """
        return None