"""
Handles username creation and profanity checking
"""

import re

from Authentication import clear_terminal
from better_profanity import profanity


def set_username():
    """Set username protocol for a new user"""

    # read in wordlist
    wordlist = read_profanity("profanity_wordlist.txt")
    clear_terminal()
    while 1:
        print("Please select a username: ")
        username = input()
        while 1:

            # check username uses corret set of characters
            charSetCheck = check_username_characters(username)
            if charSetCheck == False:

                print(
                    "Error! Username must only use characters [a-zA-Z0-9_]\n enter 1 to retry"
                )
                opt = input()

                if opt == "1":
                    # break out of current checks
                    break
                else:
                    # quit
                    return 0

            # check for any profanity in the username
            explicitProfanity = profanity.contains_profanity(username)
            containsProfanity = better_better_profanity(username, wordlist)

            if containsProfanity or explicitProfanity == True:

                print(
                    "Error! Usernames must not cointain offensive language\n enter 1 to retry"
                )
                x = input()
                if x == "1":
                    # break out of current checks
                    break
                else:
                    # quit
                    return 0

            # finish
            return username


def check_username_characters(username):
    """
    Checks that characters in username are valid characters A-Z, a-z, 0-9

    @param username Username to check
    """
    pattern = re.compile(r"^[a-zA-Z0-9_]+$")
    return bool(pattern.match(username))


def read_profanity(file_path):
    """Reads in profanity words"""

    word_list = []

    # Open the text file in read mode
    with open(file_path, "r") as file:
        # Read each line of the file
        for line in file:
            # Strip whitespace and newline characters from the line and split it into words
            words = line.strip().split()
            # Add each word to the word_list
            word_list.extend(words)

    return word_list


def better_better_profanity(username, profanity_list):
    """
    Uses Regex to check for profanity words in username
    Play on words with the library better profanity

    @param username Username to check
    @param profanity_list List of profanity words

    @returns True if profanity is found in the username, else false
    """

    for profanity_word in profanity_list:
        # Define a regular expression pattern to match the profanity word surrounded by any characters
        pattern = rf"\b\w*{re.escape(profanity_word)}\w*\b"

        # Find all matches of the pattern in the username
        matches = re.findall(pattern, username, re.IGNORECASE)

        # Check if any match is found
        if matches:
            return True
    return False
