import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")
import sqlite3
import os
import platform
import better_profanity
from better_profanity import profanity

#options
OSType = ""


def checkOS():
     OSType = platform.system()
    

def clear_terminal():
    if OSType == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    
def SQL_create_account():
    clear_terminal()    

def set_username():
    clear_terminal()

    
    print("Please select a username: ")
    username = input()
    containsProfanity = profanity.contains_profanity(username)
    if containsProfanity == True:
        print("Usernames must not cointain offensive language\n enter 1 to retry")
        opt = input()
        if opt != "1":
            return
        else:
            clear_terminal()
    else:
        return



def set_password():
    x=1




while(1):
    checkOS()
    clear_terminal()
    
    opt1 = "1. Sign up"
    opt2 = "2. Sign In"
    opt3 = "3. Exit"

#print option
    print("Welcome please select an option")
    print(opt1)
    print(opt2)
    print(opt3)
    try:
            selected = input()
            option = int (selected)
    #select user naem
            if option == 1:
                signup()
            elif option == 2:
                set_username()
                set_password()
            elif option == 3:
                exit(0)
            else:
                raise ValueError
                
    except ValueError: 
        print("Error " + selected + " is not a valid input")
        print("press 'ENTER' to continue"   )

        input()






        
    



        