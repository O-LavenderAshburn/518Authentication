import sqlite3
import os
import platform
import time
#options
OSType = ""
    
def SQL_create_account():
    x=1

def checkOS():
     OSType = platform.system()
    


def set_username():
    x=1

def set_password():
    x=1


def signup():
    set_username()


while(1):
    checkOS()
    if OSType == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    
    opt1 = "1. Sign up"
    opt2 = "2. sign in"
    opt3 = "3. exit"

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
                set_username()
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






        
    



        