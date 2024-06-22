

class AuthException(Exception):
    pass

class Auth:
    def __init__(self):
        pass

    def login(self, token):
        pass
    @staticmethod
    def signup(user):
        
        pass
    def logout(self, token):
        pass

    @staticmethod
    def isLoggedIn():
        with open("__logged_in_.cache", "r") as f:
            return f.read()!=""
    
    @property
    def curent_user(self):
        pass