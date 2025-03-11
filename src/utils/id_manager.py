import json
import os
from .utils import Utils
from utils.constants import ID_STORE_PATH

absolute_path = Utils.GetAbsPath(ID_STORE_PATH)

def __LoadIDStore():
    if not os.path.exists(absolute_path):
        id_store = {
            "item_id": 0,
            "transaction_id": 0
        }
        __SaveIDStore(id_store)
    else:
        with open(absolute_path, "r") as file:
            try:
                id_store = json.load(file)
            except json.JSONDecodeError:
                print("Error: `id_store.json` is corrupted. Resetting values.")
                id_store = {
                    "item_id": 0,
                    "transaction_id": 0
                }
                __SaveIDStore(id_store)
    return id_store

def __SaveIDStore(id_store):
    with open(absolute_path, "w") as file:
        json.dump(id_store, file, indent=4)

def GenerateID(entity_name):
    id_store = __LoadIDStore()
    id_store[entity_name] += 1 
    __SaveIDStore(id_store) 
    return id_store[entity_name] 
