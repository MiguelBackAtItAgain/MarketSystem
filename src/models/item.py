from utils.id_manager import generate_id

class Item:

    def __init__(self, name: str, reg_price: float, member_price:float, tax_status:bool):
        self.id = generate_id("item_id") 
        self.name = name
        self.reg_price = reg_price
        self.member_price = member_price
        self.tax_status = tax_status

    def getFormattedItem(self) -> dict:
        return {str(self.id): {"name": self.name, "reg_price": self.reg_price, "member_price": self.member_price,
                               "tax_status": self.tax_status}}