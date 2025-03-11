from utils.id_manager import generate_id

class Cart:
    def __init__(self, item_id: int, user_id: int):
        self.id = generate_id("cart_id")
        self.item_id = item_id
        self.user_id = user_id

    def GetFormattedCart(self) -> dict:
        return {str(self.id): {
            "item_id": self.item_id,
            "user_id": self.user_id
        }}



    

