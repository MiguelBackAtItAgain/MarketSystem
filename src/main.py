import sys
from services.CartService import CartSingleton
from services.UserService import UserService
from services.ItemService import ItemService
from services.InventoryService import LoadItemsFromInventory

def DisplayMenu():
    print("\n========= POINT OF SALE SYSTEM =========")
    print("1. Add Items to Cart")
    print("2. Remove Items from Cart")
    print("3. View Cart")
    print("4. Checkout and Print Receipt")
    print("5. Cancel Transaction")
    print("6. Change User Membership Status")
    print("0. Exit")
    print("========================================")


def AskForUserID() -> int:
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

def AddItemsToCart(user_id):
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

            CartSingleton.AddToCart(item_id, user_id)

        except ValueError:
            print("Please enter a valid numerical ID.")

def RemoveItemFromCart():
    cart_id = int(input("Enter Cart ID to remove: "))
    CartSingleton.RemoveFromCart(cart_id)
    print(f"Item with Cart ID {cart_id} removed from cart.")

def ViewCart():
    cart_summary = CartSingleton.GetFormattedCart()
    print(cart_summary)

def Checkout(cash_given):
    CartSingleton.GenerateBill(cash_given)
    print("Transaction completed and receipt generated.")
    CartSingleton.ClearCart()
    return AskForUserID()

def ChangeUserMembership():
    try:
        user_id = int(input("Enter User ID to change membership status: "))
        result = UserService.ToggleMembershipStatus(user_id)
        print(result)
    except ValueError:
        print("Invalid input. Please enter a valid numerical User ID.")

def CancelTransaction():
    CartSingleton.ClearCart()
    print("Transaction cancelled and cart cleared.")

def main():
    print("System starting...")
    LoadItemsFromInventory()
    user_id = AskForUserID()
    while True:
        DisplayMenu()
        choice = input("Enter your choice: ")
        if choice == '1':
            AddItemsToCart(user_id)
        elif choice == '2':
            RemoveItemFromCart()
        elif choice == '3':
            ViewCart()
        elif choice == '4':
            ViewCart()
            cash_given = float(input("Enter cash given: "))
            user_id = Checkout(cash_given)
        elif choice == '5':
            CancelTransaction()
        elif choice == '6':
            ChangeUserMembership()
        elif choice == '0':
            print("Exiting the system....")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

