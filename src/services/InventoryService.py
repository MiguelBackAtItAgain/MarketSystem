import os
import json
from utils.utils import Utils
from utils.constants import INVENTORY_DOC_PATH, ITEM_DB_PATH
from .ItemService import ItemService

absolute_path = Utils.GetAbsPath(INVENTORY_DOC_PATH)  
items_path = Utils.GetAbsPath(ITEM_DB_PATH)

def LoadItemsFromInventory():
    if not os.path.exists(absolute_path):
        print(f"Inventory file '{absolute_path}' not found.")
        return

    try:
        with open(absolute_path, "r") as file:
            lines = file.readlines()

        if not lines:
            print("Inventory file is empty. No items to load.")
            return

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            try:
                name_part, details_part = line.split(":", 1)
                name = name_part.strip()

                details = [item.strip() for item in details_part.split(",")]
                quantity = int(details[0])
                reg_price = float(details[1].replace("$", ""))
                member_price = float(details[2].replace("$", ""))
                tax_status = details[3].lower() == "taxable"

                for _ in range(quantity):
                    ItemService.CreateItem(name, reg_price, member_price, tax_status)

            except ValueError as ve:
                print(f"Error parsing line '{line}': {ve}")

        with open(absolute_path, "w") as file:
            file.write("")
        
        print("Inventory file successfully processed and cleared.")

    except Exception as e:
        print(f"Failed to load inventory: {e}")

