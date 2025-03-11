# MarketSystem - Point of Sale (POS) System

## Overview
MarketSystem is a command-line Point of Sale (POS) app that allows users to manage a shopping cart, checkout, and handle user memberships. The system interacts with an inventory database based on json files and provides a structured interface for managing transactions.

## Features
- **Add Items to Cart**: Select and add products to a virtual shopping cart.
- **Remove Items from Cart**: Remove items before checkout.
- **View Cart**: Display current cart contents.
- **Checkout and Print Receipt**: Complete transactions and generate receipts.
- **Cancel Transaction**: Clear the cart without proceeding to checkout.
- **Change User Membership Status**: Toggle membership benefits for customers.
- **Exit**: Terminate the application.

## Project Structure
```
deft-challenge/
│── src/
|   │── db/
|   |   │── id/
|   |   |   │── id_store.json      # It stores the last generated IDs for both items and users
|   |   │── json/
|   |   |   │── items.json         # It stores all the items that are available in the inventory.txt file
|   |   |   │── users.json         # It stores the users that come to buy stuff in the store
|   |   |   │── transactions/          # It stores all of the bills that are generated at checkout
|       │── inventory/
|   |   |   │── inventory.txt      # File where the information is pre-loaded for it to be added to the items.json file at runtime.  
│   ├── main.py                # Main entry point of the application
│   ├── models/                # Data models
│   │   ├── bill.py
│   │   ├── cart.py
│   │   ├── item.py
│   │   ├── user.py
│   ├── services/              # Business logic
│   │   ├── CartService.py
│   │   ├── InventoryService.py
│   │   ├── ItemService.py
│   │   ├── UserService.py
│   ├── utils/                 # Utility functions
│   │   ├── constants.py       # Defines database and inventory file paths
│   │   ├── id_manager.py      # Handles ID management for transactions and items
│   │   ├── utils.py           # General utility functions for path handling
│   ├── tests/
│   │   ├── test_main.py       # Contains automated tests to ensure everything is working correctly
│── inventory-sample.txt       # Sample inventory data, you can copy and paste it in the inventory.txt file
│── requirements.txt           # Dependencies for automated tests using pytest
│── README.md                  # Project documentation
```

## Installation & Setup
### Prerequisites
- Python 3.x

### Installation
1. Clone the repository or extract the ZIP file:
   ```bash
   git clone https://github.com/MiguelBackAtItAgain/MarketSystem.git
   cd MarketSystem/deft-challenge
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python src/main.py
   ```
2. Follow the on-screen menu prompts to interact with the system.

## Dependencies
The project uses the following Python libraries, these are part of pytest for automated testing of the code:
- `colorama` (Terminal text formatting)
- `pytest` (Testing framework)
- `pluggy`, `iniconfig`, `packaging` (Supporting dependencies)

## Contributing
Feel free to submit issues or pull requests if you want to improve the project.

## License
This project is licensed under the MIT License.
