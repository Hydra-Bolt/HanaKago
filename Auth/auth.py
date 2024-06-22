

from Auth.encryption import Encryption
from Main.users import Customer, User
from hakoniwa import Hakoniwa


class AuthException(Exception):
    pass

class Auth:
    __users = Hakoniwa("./TABLES/users.json")

    def login(self, user: User):
        if self.__users.find({"username": user.get_username, "password": user.get_password}):
            with open("__logged_in_.cache", "wb") as f:
                f.write(Encryption.encrypt_data(user.get_username))
            return True
        else:
            raise AuthException("Invalid username or password")
        
    def signup(self, user: Customer):
        print(self.__users)
        if self.__users.find({"username": user.get_username}):
            raise AuthException("User already exists")
        self.__users.insert(user.to_dict(), "user_id")
        self.__users._update_db()

    def logout(self):
        with open("__logged_in_.cache", "wb") as f:
            f.truncate(0)

    @staticmethod
    def loginSession():
        Encryption.load_fernet_token()
        with open("__logged_in_.cache", "rb") as f:
            return Encryption.decrypt_data(f.read()) if f.read() else ''
    
    @property
    def curent_user(self):
        return self.__users.find({"username": Auth.loginSession()})
    
