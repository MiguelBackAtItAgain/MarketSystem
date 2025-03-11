import sys
from services.CartService import CartSingleton
from services.UserService import UserService
from services.ItemService import ItemService
from services.InventoryService import load_items_from_inventory

transaction_number = 1

def display_menu():
    print("\n========= POINT OF SALE SYSTEM =========")
    print("1. Add Items to Cart")
    print("2. Remove Items from Cart")
    print("3. View Cart")
    print("4. Checkout and Print Receipt")
    print("5. Cancel Transaction")
    print("6. Change User Membership Status")
    print("0. Exit")
    print("========================================")


def ask_for_user_id() -> int:
    while True:
        try:
            user_id = int(input("Enter Customer ID: "))
            user_data = UserService.GetUserByID(user_id)
            if user_data:
                print(f"Welcome, {user_data['name']}! Membership status: {'Rewards Member' if user_data['is_member'] else 'Regular'}")
                return user_id
            else:
                print("Id not recognized, let's create a new user: ")
                user_id = int(input("Enter personal ID: "))
                ssn = int(input("Enter SSN: "))
                name = input("Enter name: ")
                is_member = input("Is the customer a Rewards Member? (yes/no): ").strip().lower() == 'yes'
                UserService.CreateUser(user_id, ssn, name, is_member)
                print(f"User {name} created successfully.")
                return user_id
        except ValueError:
            print("Please enter a valid numerical ID.")

def add_items_to_cart(user_id):
    while True:
        try:
            item_id = int(input("Enter Item ID to add (0 to stop): "))
            if item_id == 0:
                print("Finished adding items to cart.")
                break

            item_data = ItemService.GetItemByID(item_id)
            if not item_data:
                print(f"Error: No item found with ID {item_id}")
                continue

            CartSingleton._AddToCart(item_id, user_id)

        except ValueError:
            print("Please enter a valid numerical ID.")

def remove_item_from_cart():
    cart_id = int(input("Enter Cart ID to remove: "))
    CartSingleton._RemoveFromCart(cart_id)
    print(f"Item with Cart ID {cart_id} removed from cart.")

def view_cart():
    cart_items = CartSingleton._GetCartItems()
    if not cart_items:
        print("Cart is empty.")
        return

    grouped_items = {}

    print("\n=================== CART ITEMS ===================")
    print("{:<20} {:<10} {:<10} {:<10}".format("ITEM", "QUANTITY", "UNIT PRICE", "TOTAL"))

    for item_id in cart_items.keys():
        item_data = ItemService.GetItemByID(item_id)

        if not item_data:
            print(f"Warning: Could not retrieve data for item ID {item_id}")
            continue

        item_name = item_data["name"]
        unit_price = item_data["member_price"] if UserService.GetUserByID(next(iter(cart_items.values())))["is_member"] else item_data["reg_price"]

        if item_name in grouped_items:
            grouped_items[item_name]["quantity"] += 1
            grouped_items[item_name]["total"] += unit_price
        else:
            grouped_items[item_name] = {
                "quantity": 1,
                "unit_price": unit_price,
                "total": unit_price
            }

    for item_name, details in grouped_items.items():
        print("{:<20} {:<10} ${:<10.2f} ${:<10.2f}".format(
            item_name,
            details["quantity"],
            details["unit_price"],
            details["total"]
        ))

    total_price = CartSingleton._GetTotalPrice()
    print("===================================================")
    print(total_price)

def view_cart():
    cart_summary = CartSingleton._GetFormattedCart()
    print(cart_summary)


def checkout(cash_given):
    global transaction_number
    CartSingleton._GenerateBill(cash_given)
    transaction_number += 1
    print("Transaction completed and receipt generated.")
    CartSingleton._ClearCart()
    return ask_for_user_id()

def change_user_membership():
    try:
        user_id = int(input("Enter User ID to change membership status: "))
        result = UserService.ToggleMembershipStatus(user_id)
        print(result)
    except ValueError:
        print("Invalid input. Please enter a valid numerical User ID.")

def cancel_transaction():
    CartSingleton._ClearCart()
    print("Transaction cancelled and cart cleared.")

def main():
    print("System starting...")
    load_items_from_inventory()
    user_id = ask_for_user_id()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_items_to_cart(user_id)
        elif choice == '2':
            remove_item_from_cart()
        elif choice == '3':
            view_cart()
        elif choice == '4':
            view_cart()
            cash_given = float(input("Enter cash given: "))
            user_id = checkout(cash_given)
        elif choice == '5':
            cancel_transaction()
        elif choice == '6':
            change_user_membership()
        elif choice == '0':
            print("Exiting the system....")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

