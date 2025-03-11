from models.bill import Bill
from .ItemService import ItemService
from .UserService import UserService
from utils.utils import Utils
from utils.constants import TRANSACTIONS_STORE_PATH

class CartSingleton:

    _cart_items = {}  

    @classmethod
    def AddToCart(cls, item_id: int, user_id: int):
        if item_id in cls._cart_items:
            print(f"item with ID {item_id} is already in the cart.")
            return
        else:
            print(f"Added item {item_id} to cart.")
        cls._cart_items[item_id] = user_id 

    @classmethod
    def RemoveFromCart(cls, item_id: int):
        if item_id in cls._cart_items:
            del cls._cart_items[item_id]
            print(f"Removed item {item_id} from cart.")
        else:
            print(f"Item {item_id} not found in cart.")

    @classmethod
    def ClearCart(cls):
        cls._cart_items.clear()
        print("Cart cleared.")

    @classmethod
    def __GetCartItems(cls):
        return cls._cart_items 

    @classmethod
    def GetFormattedCart(cls):        
        cart_items = cls.__GetCartItems()
        if not cart_items:
            return "Cart is empty."

        grouped_items = {}
        total_tax = 0.0
        sub_total = 0.0

        user_id = next(iter(cart_items.values()), None)
        user_data = UserService.GetUserByID(user_id) if user_id else None
        is_member = user_data["is_member"] if user_data else False

        for item_id in cart_items.keys():
            item_data = ItemService.GetItemByID(item_id)

            if not item_data:
                continue 

            item_name = item_data["name"]
            unit_price = item_data["member_price"] if is_member else item_data["reg_price"]
            tax_status = item_data["tax_status"]
            tax_rate = 0.065 if tax_status else 0 
            item_tax = unit_price * tax_rate

            if item_name in grouped_items:
                grouped_items[item_name]["quantity"] += 1
                grouped_items[item_name]["total"] += unit_price
                grouped_items[item_name]["tax"] += item_tax
            else:
                grouped_items[item_name] = {
                    "quantity": 1,
                    "unit_price": unit_price,
                    "tax": item_tax,
                    "total": unit_price + item_tax
                }

            sub_total += unit_price
            total_tax += item_tax

        grand_total = sub_total + total_tax

        cart_summary = "\n=================== CART ITEMS ===================\n"
        cart_summary += "{:<20} {:<10} {:<10} {:<10} {:<10}\n".format("ITEM", "QUANTITY", "UNIT PRICE", "TAX", "TOTAL")

        for item_name, details in grouped_items.items():
            cart_summary += "{:<20} {:<10} ${:<10.2f} ${:<10.2f} ${:<10.2f}\n".format(
                item_name,
                details["quantity"],
                details["unit_price"],
                details["tax"],
                details["total"]
            )

        cart_summary += "===================================================\n"
        cart_summary += f"SUB-TOTAL: ${sub_total:.2f}\n"
        cart_summary += f"TAX (6.5% on taxable items): ${total_tax:.2f}\n"
        cart_summary += f"TOTAL: ${grand_total:.2f}\n"

        return cart_summary

    @classmethod
    def GenerateBill(cls, cash_given: float) -> None:

        if not cls._cart_items:
            print("Cart is empty. Cannot generate a bill.")
            return

        user_id = next(iter(cls._cart_items.values()))  
        user_data = UserService.GetUserByID(user_id)

        if not user_data:
            print(f"Error: Could not retrieve data for user ID {user_id}")
            return

        is_member = user_data["is_member"]
        sub_total = 0.0
        total_tax = 0.0
        total_savings = 0.0
        bill_items = {}

        for item_id in list(cls._cart_items.keys()):
            item_data = ItemService.GetItemByID(item_id)

            if not item_data:
                print(f"Error: Could not retrieve data for item ID {item_id}")
                continue

            item_name = item_data["name"]
            reg_price = item_data["reg_price"]
            member_price = item_data["member_price"]
            tax_status = item_data["tax_status"]

            unit_price = member_price if is_member else reg_price
            savings_per_item = reg_price - member_price if is_member else 0
            total_savings += savings_per_item

            subtotal = unit_price
            tax = subtotal * (0.065 if tax_status else 0)

            sub_total += subtotal
            total_tax += tax

            if item_name in bill_items:
                bill_items[item_name]["quantity"] += 1
                bill_items[item_name]["total"] += subtotal
                bill_items[item_name]["savings"] += savings_per_item 
            else:
                bill_items[item_name] = {
                    "item_name": item_name,
                    "quantity": 1,
                    "unit_price": unit_price,
                    "total": subtotal,
                    "savings": savings_per_item 
                }

            ItemService.RemoveItemByID(item_id)

        grand_total = sub_total + total_tax

        while cash_given < grand_total:
            print(f"Insufficient cash. Total is ${grand_total:.2f}, but received ${cash_given:.2f}.")
            try:
                cash_given = float(input("Enter a valid cash amount: "))
            except ValueError:
                print("Invalid input. Please enter a numerical value.")

        change = cash_given - grand_total
        bill_items_list = list(bill_items.values())

        bill = Bill(
            items=bill_items_list,
            sub_total=sub_total,
            tax=total_tax,
            total=grand_total,
            cash_given=cash_given,
            change=change,
            savings=total_savings
        )

        cls.__SaveBillToFile(bill)
        cls.ClearCart()


    @classmethod
    def __SaveBillToFile(cls, bill: Bill) -> None:

        file_name = f"transaction_{bill.transaction_number}_{bill.date}.txt"
        current_date = Utils.GetCurrentDate()
        bill_data = bill.GetFormattedBill()

        with open(f"{Utils.GetAbsPath(TRANSACTIONS_STORE_PATH)}\\{file_name}", "w") as file:
            file.write(f"{current_date}")
            file.write(f"\nTRANSACTION: {bill.transaction_number}")
            file.write("\n{:20} {:10} {:10} {:10}\n".format("ITEM", "QUANTITY", "UNIT PRICE", "TOTAL"))
            for item in bill_data["items"]:
                file.write("{:20} {:10} ${:<10.2f} ${:<10.2f}\n".format(
                    item["item_name"],
                    item["quantity"],
                    item["unit_price"],
                    item["total"]
                ))

            file.write("*" * 50 + "\n")
            file.write(f"TOTAL NUMBER OF ITEMS SOLD: {len(bill_data['items'])}\n")
            file.write(f"SUB-TOTAL: ${bill_data['sub_total']:.2f}\n")
            file.write(f"TAX (6.5%): ${bill_data['tax']:.2f}\n")
            file.write(f"TOTAL: ${bill_data['total']:.2f}\n")
            file.write(f"CASH: ${bill_data['cash_given']:.2f}\n")
            file.write(f"CHANGE: ${bill_data['change']:.2f}\n")
            file.write("*" * 50 + "\n")
            file.write(f"YOU SAVED: ${bill_data['savings']:.2f}!\n")


        print(f"Bill saved to {file_name}")