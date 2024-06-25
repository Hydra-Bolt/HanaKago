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
        print("Welcome to HanaKago!\nPlease choose an option:\n1. Sign Up\n2. Log In\n(Press 'e' to exit)")
        while True:
            key = input()
            if key == '1':
                self.signUp()
                self.authScreen()
                break
            elif key == '2':
                self.login()
                break
            elif key == 'e':
                print("\nExiting the program.")
                exit()

    def signUp(self):
        """
        Handles the sign-up process.
        """
        # Clear the screen and display a welcome message
        self.clearScreen()
        print("Great to have you with us!")
        
        # Get the user's first name and last name
        first_name = self.getInput("What's your first name? ", self.validateNonEmpty)
        last_name = self.getInput("What's your last name? ", self.validateNonEmpty)
        
        # Get the user's age and print a nice message
        age = int(self.getInput("How old are you? (this helps us make the shopping experience better) ", self.validateAge))
        print(f"Nice to meet you, {first_name} {last_name}!")
        
        # Get the user's desired username
        username = self.getInput("Now let's make your account. What would you like your username to be? ", self.validateNonEmpty)
        
        # Get and confirm the user's password
        while True:
            password = self.getInput("Great! What would you like your password to be? (min 6 characters) ", self.validatePassword)
            password_confirm = self.getInput("Please confirm your password: ")
            if password == password_confirm:
                break
            else:
                print("Passwords do not match. Please try again.")
        
        try:
            # Create a new customer account
            self.authorization.signup(Customer(first_name, last_name, age, username, password))
        except Exception as e:
            # If the account creation fails, print the error and return
            print(f"Account couldn't be made for the following reason: {e}")
            sleep(2)
            return
        
        # Clear the screen and display a success message
        self.clearScreen()
        print(f"User created successfully! Welcome, {first_name}!")
        sleep(2)
        

    def login(self):
        """
        Handles the login process.

        This function clears the screen, prompts the user for their username and password,
        attempts to log in with the provided credentials, and starts the main application
        if the login is successful. If the login fails, it prompts the user to try again.
        """
        # Clear the screen and display a welcome message
        self.clearScreen()
        print("Welcome back!")

        # Get the user's username and password
        username = self.getInput("What's your username? ", self.validateNonEmpty)
        password = self.getInput("What's your password? ", self.validatePassword)

        try:
            # Attempt to log in with the provided credentials
            self.authorization.login(Customer('', '', 0, username, password))

            # If the login is successful, display a success message and start the main application
            print("Login successful!")
            sleep(2)
            self.user = self.authorization.curent_user
            self.mainApp()

        except AuthException as e:
            # If the login fails, display an error message and prompt the user to try again
            print(f"Login failed for the following reason: {e}")
            print("Let's try that again.")
            sleep(2)
            self.login()  # Recursively call the login function to allow the user to try again

    def mainApp(self):
        """
        Starts the main application.

        This function initializes a new cart, displays a welcome message,
        displays the products, and handles keyboard input.
        """
        # Initialize a new cart
        self.cart = Cart()

        # Display a welcome message
        self._display_welcome_message()

        # Display the products
        self._display_products()

        # Handle keyboard input
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
        self.products.pretty_print(2)
        print("Type in the ID of the product to add the product to cart. \nEnter 'c' to check out. \nEnter 'h' to check out history. \nEnter 'l' to logout(or 'e' to exit).")

    def _handle_keyboard_input(self):
        """
        Handles the keyboard input.

        This function continuously listens for keyboard input and performs
        corresponding actions based on the input.
        """
        try:
            while True:
                key_event = input()

                # Handle 'e' key event to exit the program
                if key_event == 'e':
                    self._handle_exit_request()

                # Handle digit key event to add a product to the cart
                elif key_event.isdigit():
                    self._handle_add_product_to_cart(key_event)

                # Handle 'c' key event to view and checkout the cart
                elif key_event == 'c':
                    self._handle_cart_operation()

                # Handle 'h' key event to view the checkout history
                elif key_event == 'h':
                    self._handle_checkout_history()

                # Handle 'l' key event to logout
                elif key_event == "l":
                    self._handle_logout()

                # Handle invalid input
                else:
                    print("Invalid input. Please try again.")

        except KeyboardInterrupt:
            print("Exiting the program.")
            exit()

    def _handle_add_product_to_cart(self, key_event):
        """
        Handles the event of adding a product to the cart.

        Args:
            key_event (str): The keyboard input representing the product ID.
        """
        product_id = int(key_event) - 1

        # Validate the product ID
        if product_id < 0 or product_id >= len(self.products.products):
            print("Invalid product ID. Please try again.")
            return

        # Prompt for the quantity and add the product to the cart
        product_quantity = int(self.getInput("How much would you like: ", lambda x: x.isdigit()))
        self.cart.add(product_id, product_quantity)
        print(f"{self.products.products[product_id]['name']} added to cart!")
        sleep(2)
        self.clearScreen()
        self._display_products()
        self._handle_keyboard_input()

    def _handle_cart_operation(self):
        """
        Handles the event of viewing and checking out the cart.
        """
        self.clearScreen()
        print("Cart:")
        self.cart.get_cart()
        total = self.cart.get_total()
        print(f"{'-'*50}\nTotal: Rs{total}")
        print("Press 'y' to checkout. Press 'r' to remove any product. Press 'n' to go back. Press 'e' to exit.")
        self._handle_cart_options(total)

    def _handle_cart_options(self, total):
        """
        Handles the options for the cart.

        Args:
            total (float): The total cost of the cart.
        """
        while True:
            key_event = input()

            # Handle 'y' key event to checkout
            if key_event == 'y':
                self._handle_checkout_request(total)
                self._display_products()
                break

            # Handle 'n' key event to go back
            elif key_event == 'n':
                self.clearScreen()
                self._display_products()
                break

            # Handle 'e' key event to exit
            elif key_event == 'e':
                self._handle_exit_request()
                break

            # Handle 'r' key event to remove a product
            elif key_event == 'r':
                self._handle_remove_product_from_cart()

            # Handle invalid input
            else:
                print("Invalid input. Please try again.")

    def _handle_checkout_history(self):
        """
        Handles the event of viewing the checkout history.
        """
        self.clearScreen()
        try:
            carts = self.cart.get_user_cart(self.user['user_id'])
        except Exception as e:
            print(e)
            sleep(2)
            self.clearScreen()
            self._display_products()
            return

        for cart in carts:
            self._print_cart_details(cart)

        print("Press 'n' to go back. Press 'e' to exit.")
        self._handle_history_options()

    def _print_cart_details(self, cart):
        """
        Prints the details of a cart.

        Args:
            cart (dict): The cart details.
        """
        print(f"Cart ID: {cart['cart_id']}")
        print(f"Checkout out on: {cart['created_at']}")
        print("Products:")
        for product in cart['products']:
            print(f"  Product: {self.products.products[product['pid']]['name']}, Quantity: {product['quantity']}")
        print(f"Total: {cart['total']}\n")

    def _handle_history_options(self):
        """
        Handles the options for the checkout history.
        """
        while True:
            key_event = input()

            # Handle 'n' key event to go back
            if key_event == 'n':
                self.clearScreen()
                self._display_products()
                break

            # Handle 'e' key event to exit
            elif key_event == 'e':
                self._handle_exit_request()
                break

    def _handle_remove_product_from_cart(self):
        """
        Handles the event of removing a product from the cart.
        """
        product_id = int(self.getInput("Enter the product ID: ", lambda x: x.isdigit())) - 1
        if product_id < 0 or product_id >= len(self.products.products):
            print("Invalid product ID. Please try again.")
            return
        product_quantity = int(self.getInput("How much would you like: ", lambda x: x.isdigit()))
        self.cart.remove(product_id, product_quantity)
        print(f"{self.products.products[product_id]['name']} removed from cart!")
        sleep(2)
        self.clearScreen()
        self._display_products()
        self._handle_keyboard_input()

    def _handle_logout(self):
        """
        Handles the event of logging out.
        """
        self.authorization.logout()
        self.clearScreen()
        self.authScreen()

    def _handle_checkout_request(self, total):
        """
        Handles the checkout request.
        """
        if total <=0:
            print("Oops! Working with an empty shopping cart.")
            sleep(2)
            self.clearScreen()
            return
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
