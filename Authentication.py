import sqlite3
import os
import platform
#options
OSType = ""
    

def checkOS():
     OSType = platform.system()
    


def setUserName():
    x=1

def setPassword():
    x=1


def signup():
    setUserName()


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

    selected = input()
    #select user naem
    if selected == "1":
        setUserName()
    elif selected == "2":
        setUserName()
        setPassword()



        