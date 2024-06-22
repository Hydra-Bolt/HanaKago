import curses

def display_form(stdscr):
    # Turn on cursor blinking
    curses.curs_set(1)

    # Initialize colors if supported
    if curses.has_colors():
        curses.start_color()

    # Define colors for text input field
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    field_color = curses.color_pair(1)

    # Clear screen
    stdscr.clear()

    # Define the form fields
    stdscr.addstr(2, 2, "Please fill out the following information:")
    stdscr.addstr(4, 2, "Name: ")
    stdscr.addstr(5, 2, "Age: ")

    # Create text input fields
    stdscr.attron(field_color)
    name_field = curses.newwin(1, 20, 4, 8)
    age_field = curses.newwin(1, 10, 5, 8)
    stdscr.attroff(field_color)
    name_field.refresh()
    age_field.refresh()

    # Enable keypad mode for easy input handling
    stdscr.keypad(True)

    # Get user input
    name = ""
    age = ""

    while True:
        # Name input
        name_key = name_field.getch()
        if name_key == curses.KEY_ENTER or name_key in [10, 13]:
            break
        elif name_key == curses.KEY_BACKSPACE:
            name = name[:-1]
        else:
            name += chr(name_key)
        name_field.addstr(0, 0, name)

        # Age input
        age_key = age_field.getch()
        if age_key == curses.KEY_ENTER or age_key in [10, 13]:
            break
        elif age_key == curses.KEY_BACKSPACE:
            age = age[:-1]
        else:
            age += chr(age_key)
        age_field.addstr(0, 0, age)

    # Clean up
    stdscr.clear()
    stdscr.refresh()

    # Print collected data
    stdscr.addstr(2, 2, "Thank you! You entered:")
    stdscr.addstr(4, 2, f"Name: {name}")
    stdscr.addstr(5, 2, f"Age: {age}")
    stdscr.refresh()

    stdscr.getch()

def main():
    # Initialize curses
    curses.wrapper(display_form)

if __name__ == "__main__":
    main()
