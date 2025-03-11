from utils.id_manager import GenerateID

class Cart:
    def __init__(self, item_id: int, user_id: int):
        self.id = GenerateID("cart_id")
        self.item_id = item_id
        self.user_id = user_id

    def GetFormattedCart(self) -> dict:
        return {str(self.id): {
            "item_id": self.item_id,
            "user_id": self.user_id
        }}



    

