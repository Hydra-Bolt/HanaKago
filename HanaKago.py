import keyboard
import os
import time

from Auth.auth import Auth
from Main.users import User

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input(prompt, validation_func=None):
    while True:
        value = input(prompt)
        if validation_func is None or validation_func(value):
            return value
        else:
            print("Invalid input. Please try again.")


def validate_age(age):
    return age.isdigit() and 0 < int(age) < 120


def validate_non_empty(value):
    return len(value.strip()) > 0


def validate_password(password):
    return len(password) >= 6  # Simple length check, can be enhanced


def sign_up():
    clear_screen()
    print("Great to have you with us.")
    first_name = get_input("What's your first name? ", validate_non_empty)
    last_name = get_input("What's your last name? ", validate_non_empty)
    age = get_input("How old are you? (this helps us make the shopping experience better) ", validate_age)
    
    print(f"Nice to meet you, {first_name} {last_name}!")
    username = get_input("Now let's make your account. What would you like your username to be? ", validate_non_empty)
    
    while True:
        password = get_input("Great! What would you like your password to be? (min 6 characters) ", validate_password)
        password_confirm = get_input("Please confirm your password: ")
        if password == password_confirm:
            break
        else:
            print("Passwords do not match. Please try again.")
    
    try:
        Auth.signup(User(first_name, last_name, age, username, password))
    except Exception as e:
        print(f"Account couldnt be made for the following reason: {e}")
        return
    print(f"User created successfully! Welcome, {first_name}!")
    time.sleep(2)


def main():
    if Auth.loginSession():
        print("You're already logged in.")
        time.sleep(2)
        return
    clear_screen()
    print("Welcome to HanaKago!\nPlease choose an option:\n1. Sign Up\n2. Sign In\n(Press 'esc' to exit)")

    def on_key_event(event):
        if event.name == '1':
            keyboard.unhook_all()
            sign_up()
            main()
        elif event.name == '2':
            keyboard.unhook_all()
            clear_screen()
            print("Sign in functionality is not implemented yet.")
            time.sleep(2)
            main()
        elif event.name == 'esc':
            keyboard.unhook_all()
            print("Exiting the program.")
    
    keyboard.on_press(on_key_event)
    keyboard.wait('esc')

if __name__ == "__main__":
    main()