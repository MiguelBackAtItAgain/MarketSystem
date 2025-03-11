import json
import os
from .utils import Utils
from utils.constants import ID_STORE_PATH

absolute_path = Utils.get_abs_path(ID_STORE_PATH)

def load_id_store():
    if not os.path.exists(absolute_path):
        id_store = {
            "item_id": 0,
            "transaction_id": 0
        }
        save_id_store(id_store)
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
                save_id_store(id_store)
    return id_store

def save_id_store(id_store):
    with open(absolute_path, "w") as file:
        json.dump(id_store, file, indent=4)

def generate_id(entity_name):
    id_store = load_id_store()
    id_store[entity_name] += 1 
    save_id_store(id_store) 
    return id_store[entity_name] 
