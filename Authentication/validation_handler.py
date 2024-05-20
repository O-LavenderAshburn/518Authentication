"""
Handles user validation
"""

import bcrypt


from Authentication import approve_sign_in
from sql_functions import SQL_get_user_infromation
 

def validate_user(input_username, password):
    """
    Validate user protocol

    @param input_username Username user has input
    @param password password the user has input
    """
    # get user information
    user_information = SQL_get_user_infromation(input_username)

    if user_information == None:
        print("Error: invalid Username or Password")
        input()
    else:
        # if user information exists
        username, salt, hashed_salt = user_information
        isValid = validate_password(password, hashed_salt)
        if isValid == 1:
            approve_sign_in()

        else:
            print("Error: invalid Username or Password")


def validate_password(password, hashed_salt):
    """
    Verify the entered password against the retrieved hashed password

    @param password Password to valitdae
    @param hashed_salt Salt to use to check passowrd

    @return 1 if password is valid else 0
    """

    pword = bytes(password, "utf-8")

    # check password is valid
    if bcrypt.checkpw(pword, hashed_salt):
        return 1
    else:
        return 0