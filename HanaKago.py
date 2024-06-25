import keyboard
import os
from time import sleep

from Auth.auth import Auth, AuthException
from Main.cart import Cart
from Main.products import Products
from Main.users import Customer, User


class HanaKago:
    """
    The main class for the application.
    """

    @staticmethod
    def clearScreen():
        """
        Clears the screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def getInput(prompt, validationFunc=None):
        """
        Gets user input and validates it.
        """
        while True:
            value = input(prompt)
            if validationFunc is None or validationFunc(value):
                return value
            else:
                print("Invalid input. Please try again.")

    @staticmethod
    def validateAge(age):
        """
        Validates the age input.
        """
        return age.isdigit() and 0 < int(age) < 120

    @staticmethod
    def validateNonEmpty(value):
        """
        Validates if the input is non-empty.
        """
        return len(value.strip()) > 0

    @staticmethod
    def validatePassword(password):
        """
        Validates the password input.
        """
        return len(password) >= 6  # Simple length check, can be enhanced

    def __init__(self):
        """
        Initializes the application.
        """
        self.authorization = Auth()
        self.authScreen()

    def authScreen(self):
        """
        Displays the authentication screen.
        """
        self.clearScreen()
        try:
            self.user = self.authorization.curent_user
            print(f'Logged in as {self.user["username"]}')
            sleep(2)
            self.mainApp()
        except AuthException as e:
            print(e)
            self.clearScreen()
            self.displayAuthOptions()

    def displayAuthOptions(self):
        """
        Displays the authentication options.
        """
        print("Welcome to HanaKago!\nPlease choose an option:\n1. Sign Up\n2. Log In\n(Press 'esc' to exit)")
        while True:
            key = input()
            if key == '1':
                self.signUp()
                self.authScreen()
                break
            elif key == '2':
                self.login()
                break
            elif key == 'esc':
                print("\nExiting the program.")
                exit()

    def signUp(self):
        """
        Handles the sign-up process.
        """
        self.clearScreen()
        print("Great to have you with us!")
        first_name = self.getInput("What's your first name? ", self.validateNonEmpty)
        last_name = self.getInput("What's your last name? ", self.validateNonEmpty)
        age = int(self.getInput("How old are you? (this helps us make the shopping experience better) ", self.validateAge))

        print(f"Nice to meet you, {first_name} {last_name}!")
        username = self.getInput("Now let's make your account. What would you like your username to be? ", self.validateNonEmpty)

        while True:
            password = self.getInput("Great! What would you like your password to be? (min 6 characters) ", self.validatePassword)
            password_confirm = self.getInput("Please confirm your password: ")
            if password == password_confirm:
                break
            else:
                print("Passwords do not match. Please try again.")

        try:
            self.authorization.signup(Customer(first_name, last_name, age, username, password))
        except Exception as e:
            print(f"Account couldn't be made for the following reason: {e}")
            sleep(2)
            return

        self.clearScreen()
        print(f"User created successfully! Welcome, {first_name}!")
        sleep(2)

    def login(self):
        """
        Handles the login process.
        """
        self.clearScreen()
        print("Welcome back!")
        username = self.getInput("What's your username? ", self.validateNonEmpty)
        password = self.getInput("What's your password? ", self.validatePassword)
        try:
            self.authorization.login(Customer('', '', 0, username, password))
            print("Login successful!")
            sleep(2)
            self.user = self.authorization.curent_user
            self.mainApp()
        except AuthException as e:
            print(f"Login failed for the following reason: {e}")
            print("Let's try that again.")
            sleep(2)
            self.login()

    def mainApp(self):
        """
        Starts the main application.
        """
        self.cart = Cart()
        self._display_welcome_message()
        self._display_products()
        self._handle_keyboard_input()

    def _display_welcome_message(self):
        """
        Displays the welcome message.
        """
        self.clearScreen()
        print("HanaKago - The basket of dreams!")
        sleep(2)

    def _display_products(self):
        """
        Displays the products.
        """
        self.products = Products()
        self.products.pretty_print()
        print("Type in the ID of the product to add the product to cart. Enter 'c' to check out. (or 'esc' to exit).")

    def _handle_keyboard_input(self):
        """
        Handles the keyboard input.
        """
        try:
            while True:
                key_event = input()
                if key_event == 'esc':
                    self._handle_exit_request()
                elif key_event.isdigit():
                    product_id = int(key_event) - 1
                    product_quantity = int(self.getInput("", lambda x: x.isdigit()))
                    self.cart.add(product_id, product_quantity)
                    print(f"{self.products.products[product_id]['name']} added to cart!")
                    sleep(2)
                    self.clearScreen()
                    self._display_products()
                    self._handle_keyboard_input()
                elif key_event == 'c':
                    self.clearScreen()
                    print("Cart:")
                    self.cart.get_cart()
                    total = self.cart.get_total()
                    print(f"{'-'*50}\nTotal: Rs{total}")
                    print("Press 'y' to checkout. Press 'n' to go back. Press 'esc' to exit.")
                    while True:
                        key_event = input()
                        if key_event == 'y':
                            self.clearScreen()
                            self._handle_checkout_request(total)
                            break
                        elif key_event == 'n':
                            self.clearScreen()
                            self._display_products()
                            break
                        elif key_event == 'esc':
                            self._handle_exit_request()
                            break
                        else:
                            print("Invalid input. Please try again.")

                else:
                    print("Invalid input. Please try again.")

        except KeyboardInterrupt:
            print("Exiting the program.")
            exit()

    def _handle_checkout_request(self, total):
        """
        Handles the checkout request.
        """
        self.clearScreen()
        self.cart.checkout(self.user['user_id'])
        self.cart = Cart()
        sleep(2)
        self.mainApp()

    def _handle_exit_request(self):
        """
        Handles the exit request.
        """
        print("Are you sure? Press 'y' to exit, n to go back.")
        while True:
            key_event = input()
            if key_event == 'y':
                print("Exiting the program.")
                exit()
            elif key_event == 'n':
                break

if __name__ == '__main__':
    HanaKago()
