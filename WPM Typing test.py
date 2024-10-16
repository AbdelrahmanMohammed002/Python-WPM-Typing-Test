import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    """
    Displays the start screen and waits for the user to press any key to begin.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()  # Wait for any key press

def display_text(stdscr, target, current, wpm=0):
    """
    Displays the target text and the user's current input with color highlighting.

    Args:
        stdscr: The screen object to write on.
        target (str): The target text for typing.
        current (list): The current typed characters by the user.
        wpm (int): Words per minute (WPM) calculated.
    """
    stdscr.addstr(target)  # Display target text at the top
    stdscr.addstr(1, 0, f"WPM: {wpm}")  # Display the WPM on the second line

    # Loop through each character typed by the user
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)  # Default color for correct characters

        if char != correct_char:
            color = curses.color_pair(2)  # Use red for incorrect characters

        # Display each typed character with its corresponding color
        stdscr.addstr(0, i, char, color)

def load_text():
    """
    Loads random text from a file to be used as the target for typing.
    """
    with open("text.txt", "r") as text_file:
        lines = text_file.readlines()
        return random.choice(lines).strip()  # Strip removes any extra whitespace

def wpm_test(stdscr):
    """
    Runs the WPM (Words Per Minute) typing test.
    """
    target_text = load_text()  # Load the target text
    current_text = []  # Track the current input from the user
    wpm = 0
    start_time = time.time()  # Record the start time
    stdscr.nodelay(True)  # Make getkey non-blocking for real-time input

    while True:
        time_elapsed = max(time.time() - start_time, 1)  # Ensure no divide by zero
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # Calculate WPM

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)  # Display text and WPM
        stdscr.refresh()

        # Check if the user has completed typing the target text
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ESC key to exit
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):  # Handle backspace
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    """
    Initializes colors, runs the typing test, and handles replay or exit.
    """
    # Initialize color pairs for correct and incorrect characters
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct character
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Incorrect character
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text

    start_screen(stdscr)  # Display the start screen

    while True:
        wpm_test(stdscr)  # Run the WPM typing test
        stdscr.addstr(2, 0, "You completed the text! Press any key to replay (ESC to quit)...")
        key = stdscr.getkey()
        if ord(key) == 27:  # If ESC key is pressed, exit the program
            break

# Wrap the main function in curses' wrapper to initialize and handle cleanup automatically
wrapper(main)
