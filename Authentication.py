import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")
import sqlite3
import secrets  
import maskpass
import os
import platform
import better_profanity
from better_profanity import profanity
import re
#options
OSType = ""


#generatre random salt 
def generate_salt(length=16):
    return secrets.token_hex(length)

#check username conforms to the charaters 
def check_username(input_string):
    pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    return bool(pattern.match(input_string))


#get operating system type for clearing the terminal
def checkOS():
     OSType = platform.system()
    
#clear the terminal
def clear_terminal():
    if OSType == "Windows":
        os.system('cls')
    else:
        os.system('clear')

#creates the tables for sql
def SQL_create_account():
    clear_terminal()    

#init signup process
def signup():
    success = set_username()
    if success == 1:
        set_password()

#set a username for a new user
def set_username():
    clear_terminal()
    while(1):
        print("Please select a username: ")
        username = input()
        while(1):
            #check for any profanity in the username
            containsProfanity = profanity.contains_profanity(username)
            if containsProfanity == True:
                print("Error! Usernames must not cointain offensive language\n enter 1 to retry")
                x = input()
                if x == "1":
                    break
                else:
                    return  0
             #check username uses corret set of characters    
            charSetCheck = check_username(username)
            if charSetCheck == False:
                print("Error! Username must only use characters [a-zA-Z0-9_]\n enter 1 to retry")
                opt = input()
                if opt != "1":
                    break
                else:
                    return 0
        return 1

#Set a new password for a new user        
def set_password():
     #Set password
    while(1):
        #prompt user for password 
        print("Please enter a password")
        password = maskpass.askpass(mask="*")
        while(1):
            if len(password) < 8:
                print("Error! Password is too short. The password must be at least 8 characters long \n enter 1 to retry")
                opt = input()
                if opt != "1":
                    break
                else:
                    return 0
        return 1
        


while(1):
    checkOS()
    clear_terminal()
    #set options
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
        
        #run sign up process
        if option == 1:
            signup()
        #run signin process
        elif option == 2:
            x=1
        elif option == 3:
            exit(0)
        else:
            raise ValueError
                
    except ValueError: 
        print("Error " + selected + " is not a valid input")
        print("press 'ENTER' to continue"   )

        input()






        
    



        