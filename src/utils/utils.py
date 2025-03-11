import os
from datetime import datetime

class Utils:

    def __GetDbBasePath() -> str:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return base_path

    @staticmethod
    def DbExists(path: str):
        base_path = Utils.__GetDbBasePath()
        absolute_path = os.path.join(base_path, path)
        return os.path.exists(absolute_path)
    
    @staticmethod
    def GetAbsPath(path: str):
        base_path = Utils.__GetDbBasePath()
        absolute_path = os.path.join(base_path, path)
        return absolute_path

    @staticmethod
    def GetCurrentDate():
        current_date = datetime.now() 
        return current_date.strftime("%B %d, %Y")