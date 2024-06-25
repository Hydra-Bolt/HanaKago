

from Auth.encryption import Encryption
from Main.users import Customer, User
from hakoniwa import Hakoniwa


class AuthException(Exception):
    pass

class Auth:
    __users = Hakoniwa("./TABLES/users.json")

    def login(self, user: User):
        if self.__users.find({"username": user.get_username, "password": user.get_password}):
            with open("__logged_in_.cache", "w") as f:
                f.write(user.get_username)
            return True
        else:
            raise AuthException("Invalid username or password")
        
    def signup(self, user: Customer):
        if self.__users.find({"username": user.get_username}):
            raise AuthException("User already exists")
        self.__users.insert(user.to_dict(), "user_id")
        self.__users._update_db()

    def logout(self):
        with open("__logged_in_.cache", "w+") as f:
            f.truncate(0)

    @staticmethod
    def loginSession():
        with open("__logged_in_.cache", "r") as f:
            return f.read() 
    
    @property
    def curent_user(self):
        user = self.__users.find({"username": Auth.loginSession()})
        if user:
            return user[0]
        else:
            raise AuthException("Invalid User!")
    
