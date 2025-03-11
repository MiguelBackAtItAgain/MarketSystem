from utils.constants import ITEM_DB_PATH
from models.item import Item
from utils.utils import Utils
import json, os

class ItemService:

    absolute_path = Utils.get_abs_path(ITEM_DB_PATH)

    @staticmethod
    def GetItemByID(id: int) -> dict:
        if not Utils.db_exists(ITEM_DB_PATH):
            print(f"Error: File not found at {ITEM_DB_PATH}")
            return {}
        try:
            with open(ItemService.absolute_path, 'r') as file:
                content = json.load(file)
            return content.get(str(id), {})
        except (json.JSONDecodeError) as e:
            print(f"Error reading user data: {e}")

    def CreateItem(name: str, reg_price: float, member_price: float, tax_status: bool) -> str:
        try:
            item = Item(name, reg_price, member_price, tax_status)
            item_data = item.getFormattedItem()
            with open(ItemService.absolute_path, 'r') as file:
                try:
                    items_data = json.load(file)
                except json.JSONDecodeError:
                    items_data = {}
                items_data.update(item_data)
                with open(ItemService.absolute_path, 'w') as file:
                    json.dump(items_data, file, indent=4)
        except Exception as e:
            return f"Failed to create the item"
        
    @staticmethod
    def RemoveItemByID(item_id: int) -> None:
        """Removes an item from items.json by its ID."""
        if not os.path.exists(ItemService.absolute_path):
            print("Error: items.json does not exist.")
            return

        try:
            with open(ItemService.absolute_path, "r") as file:
                try:
                    items_data = json.load(file)
                except json.JSONDecodeError:
                    print("Error: Cannot read items.json.")
                    return
                
            if str(item_id) not in items_data:
                print(f"Item with ID {item_id} not found in inventory.")
                return
            
            del items_data[str(item_id)]

            with open(ItemService.absolute_path, "w") as file:
                json.dump(items_data, file, indent=4)

        except Exception as e:
            print(f"Failed to update inventory: {e}")

    
        
    