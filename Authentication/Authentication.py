import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")
import sqlite3
import secrets  
import maskpass
import os
import platform
from better_profanity import profanity
import re
import bcrypt
import password_filter

#options
OSType = ""
user = ""


def read_profanity(file_path):
    word_list = []

    # Open the text file in read mode
    with open(file_path, 'r') as file:
        # Read each line of the file
        for line in file:
            # Strip whitespace and newline characters from the line and split it into words
            words = line.strip().split()

            # Add each word to the word_list
            word_list.extend(words)

    return word_list

def better_better_profanity(username, profanity_list):

    for profanity_word in profanity_list:
        # Define a regular expression pattern to match the profanity word surrounded by any characters
        pattern = fr'\b\w*{re.escape(profanity_word)}\w*\b'

        # Find all matches of the pattern in the username
        matches = re.findall(pattern, username, re.IGNORECASE)

        # Check if any match is found
        if matches:
            return True
    return False

def SQL_get_user_infromation(username):
    con = sqlite3.connect("authentication.db")
    cursor = con.cursor()
   

    cursor.execute(''' SELECT username, salt,passwordhash FROM users WHERE username = ? ''',(username,))
    user = cursor.fetchone()
    if user:
        userInfo = user  # Returns a tuple (username, password, salt)
        return userInfo
    
    else:
        usserInfo = None
        return userInfo


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
def SQL_create_account(username, Salt, hashedSalt):
    #connect to database 
    con = sqlite3.connect("authentication.db")
    cursor = con.cursor()
    cursor.execute('''
        INSERT INTO users (username, salt,passwordhash) VALUES (?,?,?)
                   ''',(username,Salt,hashedSalt))
    con.commit()
    #enter data into database
    clear_terminal()    


#hash password using bcrypt
def create_acc(username, password):

   # print("salted pwoed " + salted_password+"\n")
   #print("hash " + hashed +"\n")
    salt = bcrypt.gensalt(16)

    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
    SQL_create_account(username,salt,hashed)
    

#init signup process
def signup():
    username = set_username()
    if username != 0:
       password = set_password()
       if password !=0:
           create_acc(username,password)


#set a username for a new user
def set_username():
    wordlist = read_profanity('profanity_wordlist.txt')
    clear_terminal()
    while(1):
        print("Please select a username: ")
        username = input()
        while(1):
            #check username uses corret set of characters    
            charSetCheck = check_username(username)
            if charSetCheck == False:
                print("Error! Username must only use characters [a-zA-Z0-9_]\n enter 1 to retry")
                opt = input()
                if opt == "1":
                    #break out of current checks
                    break
                else:
                    #quit
                    return 0
            #check for any profanity in the username
            containsProfanity = better_better_profanity(username,wordlist)
            if containsProfanity == True:
                print("Error! Usernames must not cointain offensive language\n enter 1 to retry")
                x = input()
                if x == "1":
                    #break out of current checks
                    break
                else:
                    #quit
                    return  0

            #finish
            return username
        

#Set a new password for a new user        
def set_password():
     #Set password
    while(1):
        #prompt user for password 
        print("Please enter a password")
        password = maskpass.askpass(mask="*")
        while(1):
            if len(password) < 8:
                print("Error! Password is too short.\nThe password must be at least 8 characters long and not contain sequential or repeating characters \n enter 1 to retry")
                opt = input()
                if opt != "1":
                    break
                else:
                    return 0
            
            isValid = password_filter.check_sequential(password)
            isWeak = password_filter.check_compromised_password(password,"weakpasswords.txt")
            if isWeak == True:
                print("Error! Password is too weak\n.The password must be at least 8 characters long and not contain sequential or repeating characters \n enter 1 to retry")
                opt = input()
                if opt != "1":
                    break
                else:
                    return 0
    
            isCompromised = password_filter.check_compromised_password(password,"breachedpasswords.txt")
            if isCompromised == True:
                print("Error! Error! Password is too weak\n.The password must be at least 8 characters long and not contain sequential or repeating characters \n enter 1 to retry")
                opt = input()
                if opt != "1":
                    break
                else:
                    return 0

            if isValid == True:
                return password
            else:
                print("Error! Password must not Repeating or Sequential characters. \n enter 1 to retry")
                opt = input()
                if opt != "1":
                    break
                else:
                    return 0


def validate_password(password,salt,hashed_salt):
    # Verify the entered password against the retrieved hashed password
    if bcrypt.checkpw(password.encode('utf-8'), hashed_salt):
        return 1
    else:
        return 0
    

def approve_sign_in():
    clear_terminal()
    print("Sign in successful")


def validate_user(input_username,password):
    #get user information
    user_information = SQL_get_user_infromation(input_username)

    if user_information == None:
        print("Error: invalid Username or Password")
    else:
      #if user information exists
       username,salt,hashed_salt =user_information
       isValid = validate_password(salt,hashed_salt,password)
       if isValid == 1:
           approve_sign_in()

       else:
            print("Error: invalid Username or Password")



def signin():
    print("Enter username: ")
    username = input()
    print("Enter password: ")
    password = maskpass.askpass(mask=("*"))

    validate_user(username,password)
    

#Main program
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
            signin()    
        elif option == 3:
            exit(0)
        else:
            raise ValueError
                
    except ValueError: 
        print("Error " + selected + " is not a valid input")
        print("press 'ENTER' to continue" )
        input()
        