"""
Handles sql calls and fuctions
"""
import sqlite3
from Authentication import clear_terminal

def create_account_sql(username, salt, hashed_salt):
    """
    Creates account in database using SQLite

    @param username Username of the account
    @param salt salt to use on the password
    @param hashed_salt bCrypt hashed salt
    """

    try:
        # connect to database
        conn = sqlite3.connect("authentication.db")
        cursor = conn.cursor()

        # execute query
        cursor.execute(
            """
            INSERT INTO users (username, 
                       salt,passwordhash) 
                       VALUES (?,?,?)
                    """,
            (username, salt, hashed_salt),
        )

        conn.commit()
        # Close the connection
        conn.close()
        # enter data into database
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

def SQL_get_user_infromation(username):
    """
    Gets user information from SQLite

    @param username Username of the user
    """

    # connect to sqlite
    con = sqlite3.connect("authentication.db")
    cursor = con.cursor()

    # execute query
    cursor.execute(
        """ SELECT username, salt,passwordhash FROM users WHERE username = ? """,
        (username,),
    )

    # store user information
    global user
    user = cursor.fetchone()
    if user:
        userInfo = user  # Returns a tuple (username, password, salt)
        return userInfo

    else:
        userInfo = None
        return userInfo