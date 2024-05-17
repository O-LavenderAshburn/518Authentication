"""
User Authentication Simulation 
"""

import sys
import sqlite3
import secrets  
import maskpass
import os
import platform
from better_profanity import profanity
import re
import bcrypt
import password_filter


sys.path.append("/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages")


def read_profanity(file_path):
    """ Reads in profanity words """

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
    """
    Uses Regex to check for profanity words in username 
    Play on words with the library better profanity

    @param username Username to check
    @param profanity_list List of profanity words

    @returns True if profanity is found in the username, else false
    """
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
    """
    gets user information from SQLite

    @param username Username of the user
    """

    #connect to sqlite
    con = sqlite3.connect("authentication.db")
    cursor = con.cursor()
    
    #execute query
    cursor.execute(''' SELECT username, salt,passwordhash FROM users WHERE username = ? ''',(username,))

    #store user information
    global user
    user = cursor.fetchone()
    if user:
        userInfo = user  # Returns a tuple (username, password, salt)
        return userInfo
    
    else:
        userInfo = None
        return userInfo


def check_username_characters(username):
    """
    Checks that characters in username are valid characters A-Z, a-z, 0-9

    @param username Username to check
    """
    pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    return bool(pattern.match(username))


def checkOS():
     """Get operating system type for clearing the terminal"""

     global OSType
     OSType = platform.system()
    

def clear_terminal():
    """ clears the terminal based on the os type """

    if OSType == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def create_account_sql(username, salt, hashed_salt):
    """
    Creates account in database using SQLite

    @param username Username of the account
    @param salt salt to use on the password 
    @param hashed_salt bCrypt hashed salt 
    """
    try:
        #connect to database 
        conn = sqlite3.connect("authentication.db")
        cursor = conn.cursor()

        #execute query
        cursor.execute('''
            INSERT INTO users (username, 
                       salt,passwordhash) 
                       VALUES (?,?,?)
                    ''',(username,salt,hashed_salt))
        
        conn.commit()
        # Close the connection
        conn.close()
        #enter data into database
        clear_terminal()
    except sqlite3.Error as e:    
        # Handle the error
        print("SQLite error:", e)
        print("press 'enter' to return")

         # Rollback the transaction
        conn.rollback()
        input()
    
    finally:
        # Close the connection
        conn.close()


def create_acc(username, password):
    """
    Hashes password and calls function to create the account in the database 

    @param username the username of the user
    @param password the password to use and to be hashed
    """
    
    #generate salt
    salt = bcrypt.gensalt(16)

    #hash password with salt
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)

    create_account_sql(username,salt,hashed)
    

def signup():
    """signup protocol"""
    username = set_username()
    if username != 0:
       password = set_password()
       if password !=0:
           create_acc(username,password)


def set_username():
    """set username protocol for a new user"""

    #read in wordlist
    wordlist = read_profanity('profanity_wordlist.txt')
    clear_terminal()
    while(1):
        print("Please select a username: ")
        username = input()
        while(1):

            #check username uses corret set of characters    
            charSetCheck = check_username_characters(username)
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
            explicitProfanity = profanity.contains_profanity(username3)
            containsProfanity = better_better_profanity(username,wordlist)

            if containsProfanity or explicitProfanity == True:

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
        
     
def set_password():
    """run password setting protocol to set a new password for a new user"""

    while(1):

        #prompt user for password 
        print("Please enter a password")
        password = maskpass.askpass(mask="*")

        while(1):

            if len(password) < 8:

                print("Error! Password is too short.\nThe password must be at least 8 characters long and not contain sequential or repeating characters \n enter 1 to retry")
                opt = input()
                if opt == "1":
                    break
                else:
                    return 0
            
            #check that password isn't too weak
            isWeak = password_filter.check_compromised_password(password,"weakpasswords.txt")
            if isWeak == True:
                
                #print error
                print("Error! Password is too weak\n.The password must be at least 8 characters long and not contain sequential or repeating characters \n enter 1 to retry")
                opt = input()
                if opt == "1":
                    break
                else:
                    return 0
            #check if password is a compromised password
            isCompromised = password_filter.check_compromised_password(password,"breachedpasswords.txt")
            if isCompromised == True:
                
                #print error
                print("Error! Error! Password is too weak\n.The password must be at least 8 characters long and not contain sequential or repeating characters \n enter 1 to retry")
                opt = input()
                if opt == "1":
                    break
                else:
                    return 0
            return password
                

def validate_password(password,hashed_salt):
    """
    Verify the entered password against the retrieved hashed password

    @param password Password to valitdae 
    @param hashed_salt Salt to use to check passowrd

    @return 1 if password is valid else 0
    """

    pword = bytes(password,'utf-8')

    #check password is valid 
    if bcrypt.checkpw(pword, hashed_salt):
        return 1
    else:
        return 0
    

def approve_sign_in():
    """Print if passwod is login is successful"""

    #clear terminal 
    clear_terminal()
    #print success
    print("Sign in successful")
    input()


def validate_user(input_username,password):
    """
    Validate user protocol 

    @param input_username Username user has input
    @param password password the user has input
    """
    #get user information
    user_information = SQL_get_user_infromation(input_username)

    if user_information == None:
        print("Error: invalid Username or Password")
        input()
    else:
      #if user information exists
       username,salt,hashed_salt =user_information
       isValid = validate_password(password,hashed_salt)
       if isValid == 1:
           approve_sign_in()

       else:
            print("Error: invalid Username or Password")


def signin():
    """ sign in protocol"""

    #prompt user
    print("Enter username: ")
    username = input()

    #mask password
    password = maskpass.askpass(mask=("*"))

    #call validate_user
    validate_user(username,password)
    

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
            clear_terminal()
            exit(0)
        else:
            raise ValueError
                
    except ValueError: 
        print("Error " + selected + " is not a valid input")
        print("press 'ENTER' to continue")
        input()
        