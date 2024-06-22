import keyboard
import os
import time

from Auth.auth import Auth, AuthException
from Main.users import Customer, User



class HanaKago:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_input(prompt, validation_func=None):
        while True:
            value = input(prompt)
            if validation_func is None or validation_func(value):
                return value
            else:
                print("Invalid input. Please try again.")

    @staticmethod
    def validate_age(age):
        return age.isdigit() and 0 < int(age) < 120

    @staticmethod
    def validate_non_empty(value):
        return len(value.strip()) > 0

    @staticmethod
    def validate_password(password):
        return len(password) >= 6  # Simple length check, can be enhanced

    def __init__(self):
        self.authorization = Auth()
        self.main()
    def main(self):
        if self.authorization.loginSession()!='':
            print("You're already logged in.")
            time.sleep(2)
            return
        self.clear_screen()
        print("Welcome to HanaKago!\nPlease choose an option:\n1. Sign Up\n2. Log In\n(Press 'esc' to exit)")

        def on_key_event(event):
            if event.name == '1':
                keyboard.unhook_all()
                self.sign_up()
                self.clear_screen()
                print("Sign up successful! You can now log in.")
            elif event.name == '2':
                keyboard.unhook_all()
                self.clear_screen()
                self.login()
                time.sleep(2)
            elif event.name == 'esc':
                keyboard.unhook_all()
                print("Exiting the program.")
    
        keyboard.on_press(on_key_event)
        keyboard.wait('esc')

    def sign_up(self):
        self.clear_screen()
        print("Great to have you with us.")
        first_name = self.get_input("What's your first name? ", self.validate_non_empty)
        last_name = self.get_input("What's your last name? ", self.validate_non_empty)
        age = int(self.get_input("How old are you? (this helps us make the shopping experience better) ", self.validate_age))
        
        print(f"Nice to meet you, {first_name} {last_name}!")
        username = self.get_input("Now let's make your account. What would you like your username to be? ", self.validate_non_empty)
        
        while True:
            password = self.get_input("Great! What would you like your password to be? (min 6 characters) ", self.validate_password)
            password_confirm = self.get_input("Please confirm your password: ")
            if password == password_confirm:
                break
            else:
                print("Passwords do not match. Please try again.")
        
        try:
            self.authorization.signup(Customer(first_name, last_name, age, username, password))
        except Exception as e:
            print(f"Account couldnt be made for the following reason: {e}")
            return
        print(f"User created successfully! Welcome, {first_name}!")
        time.sleep(2)

    def login(self):
        self.clear_screen()
        print("Welcome back!")
        while True:
            username = self.get_input("What's your username? ", self.validate_non_empty)
            password = self.get_input("What's your password? ", self.validate_password)
            try:
                self.authorization.login(Customer('', '', 0, username, password))
                print("Login successful!")
                time.sleep(2)
                break
            except AuthException as e:
                print(f"Login failed for the following reason: {e}")
                print("Lets try that again.")
                return
        self.main()

if __name__ == '__main__':
    HanaKago()