"""
User Authentication Simulation 
"""

import sys
import maskpass
import os
import platform
import bcrypt

from sql_functions import create_account_sql
from password_handler import set_password
from username_handler import set_username
from validation_handler import validate_user

sys.path.append(
    "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages"
)


def checkOS():
    """Get operating system type for clearing the terminal"""

    global OSType
    OSType = platform.system()


def clear_terminal():
    """Clears the terminal based on the os type"""

    if OSType == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def create_acc(username, password):
    """
    Hashes password and calls function to create the account in the database

    @param username the username of the user
    @param password the password to use and to be hashed
    """

    # generate salt
    salt = bcrypt.gensalt(16)

    # hash password with salt
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    create_account_sql(username, salt, hashed)


def signup():
    """Signup protocol"""

    username = set_username()
    if username != 0:
        password = set_password()
        if password != 0:
            create_acc(username, password)


def approve_sign_in():
    """Print if passwod is login is successful"""

    # clear terminal
    clear_terminal()
    # print success
    print("Sign in successful")
    input()


def signin():
    """Sign in protocol"""

    # prompt user
    print("Enter username: ")
    username = input()

    # mask password
    password = maskpass.askpass(mask=("*"))

    # call validate_user
    validate_user(username, password)


while 1:
    checkOS()
    clear_terminal()
    # set options
    opt1 = "1. Sign up"
    opt2 = "2. Sign In"
    opt3 = "3. Exit"

    # print option
    print("Welcome please select an option")
    print(opt1)
    print(opt2)
    print(opt3)
    try:
        selected = input()
        option = int(selected)

        # run sign up process
        if option == 1:
            signup()
        # run signin process
        elif option == 2:
            signin()
        elif option == 3:
            clear_terminal()
            exit(0)
        else:
            raise ValueError

    except ValueError:
        print("Error " + selected + " is not a valid input")
        print("press 'ENTER' to continue")
        input()
