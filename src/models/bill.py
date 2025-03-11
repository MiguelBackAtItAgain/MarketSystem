from datetime import datetime
from utils.id_manager import GenerateID

class Bill:

    def __init__(self, items: list, sub_total: float, tax: float,
                 total: float, cash_given: float, change: float, savings: float):
        self.transaction_number = f"{GenerateID("transaction_id"):06d}"
        self.items = items  
        self.sub_total = sub_total
        self.tax = tax
        self.total = total
        self.cash_given = cash_given
        self.change = change
        self.date = datetime.now().strftime("%m%d%Y")
        self.savings = savings

    def GetFormattedBill(self) -> dict:
        return { 
            "transaction_number": self.transaction_number,
            "date": self.date,
            "items": self.items,
            "sub_total": self.sub_total,
            "tax": self.tax,
            "total": self.total,
            "cash_given": self.cash_given,
            "change": self.change,
            "savings": self.savings
        }
