"""
Handles password creation
"""

import maskpass


def set_password():
    """Run password setting protocol to set a new password for a new user"""

    while 1:

        # prompt user for password
        print("Please enter a password")
        password = maskpass.askpass(mask="*")

        while 1:

            if len(password) < 8:

                print(
                    """
                    Error! Password is too short.\nThe password must be at least 8 characters long and 
                    not contain sequential or repeating characters \n enter 1 to retry
                    """
                )
                opt = input()
                if opt == "1":
                    break
                else:
                    return 0

            # check that password isn't too weak
            isWeak = check_password_file(password, "weakpasswords.txt")
            if isWeak == True:

                # print error
                print(
                    """
                    Error! Password is too weak\n.The password must be at least 8 characters long 
                    and not contain sequential or repeating characters \n enter 1 to retry
                    """
                )
                opt = input()
                if opt == "1":
                    break
                else:
                    return 0
            # check if password is a compromised password
            isCompromised = check_password_file(password, "breachedpasswords.txt")
            if isCompromised == True:

                # print error
                print(
                    """
                    Error! Error! Password is too weak\n.The password must be at least 8 characters
                    long and not contain sequential or repeating characters \n enter 1 to retry
                    """
                )
                opt = input()
                if opt == "1":
                    break
                else:
                    return 0
            return password


def check_password_file(password, filename):
    """
    Checks if password is contained in file

    @param password Password to check
    @param filename Name of file with compromised passwords

    @return True if the password is part of the compromised password list else False
    """
    with open(filename, "r") as file:
        compromised_passwords = file.readlines()
        compromised_passwords = [pwd.strip() for pwd in compromised_passwords]
        if password in compromised_passwords:
            return True
        else:
            return False
