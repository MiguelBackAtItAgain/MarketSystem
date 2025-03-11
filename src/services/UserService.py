from utils.constants import USER_DB_PATH
from models.user import User
from utils.utils import Utils
import json

class UserService:

    absolute_path = Utils.get_abs_path(USER_DB_PATH)

    @staticmethod
    def GetUserByID(id: int) -> dict:
        if Utils.db_exists(USER_DB_PATH):
            try:
                with open(UserService.absolute_path, 'r') as file:
                    content = json.load(file)
                return content.get(str(id), {})
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading user data: {e}")
                return {}
        else:
            print(f"An unknown error has ocurred, please try again later")
            return {}
    
    @staticmethod
    def UserExists(id: int) -> bool:
        return UserService.GetUserByID(id) != {}
       
    @staticmethod
    def CreateUser(id: int, ssn: int, name: str, is_member: bool) -> str:
        if not UserService.UserExists(id):
            try:
                user = User(id, ssn, name, is_member)
                user_data = user.getFormattedUser()
                with open(UserService.absolute_path, 'r') as file:
                    try:
                        users_data = json.load(file)
                    except json.JSONDecodeError:
                        users_data = {}
                users_data.update(user_data)
                with open(UserService.absolute_path, 'w') as file:
                    json.dump(users_data, file, indent=4)
            except Exception as e:
                return f"Failed to create user."
        else:
            return f"User with personal id {id} already exists."
    
    @staticmethod
    def ToggleMembershipStatus(user_id: int) -> str:
        """Toggles a user's membership status and updates the file."""
        try:
            with open(UserService.absolute_path, 'r') as file:
                try:
                    users_data = json.load(file)
                except json.JSONDecodeError:
                    users_data = {}

            if str(user_id) not in users_data:
                return f"Error: User with ID {user_id} not found."

            # Toggle the `is_member` status
            users_data[str(user_id)]["is_member"] = not users_data[str(user_id)]["is_member"]

            # Save the updated user data
            with open(UserService.absolute_path, 'w') as file:
                json.dump(users_data, file, indent=4)

            new_status = "Rewards Member" if users_data[str(user_id)]["is_member"] else "Regular"
            return f"User {user_id} is now a {new_status}."
        
        except Exception as e:
            return f"Failed to update membership status: {e}"

        
    
           
