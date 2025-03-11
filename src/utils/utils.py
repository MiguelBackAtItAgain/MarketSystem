import os
from datetime import datetime

class Utils:

    def __get_db_basepath() -> str:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return base_path

    @staticmethod
    def db_exists(path: str):
        base_path = Utils.__get_db_basepath()
        absolute_path = os.path.join(base_path, path)
        return os.path.exists(absolute_path)
    
    @staticmethod
    def get_abs_path(path: str):
        base_path = Utils.__get_db_basepath()
        absolute_path = os.path.join(base_path, path)
        return absolute_path

    def get_current_date():
        current_date = datetime.now() 
        return current_date.strftime("%B %d, %Y")