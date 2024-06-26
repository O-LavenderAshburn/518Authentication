"""
Sets up SQLite database locally
"""

import sqlite3


def setup_db():
    """set up database"""
    
    con = sqlite3.connect("authentication.db")
    cursor = con.cursor()

    create_table_query = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        salt TEXT NOT NULL,
        passwordhash TEXT NOT NULL
    );
    '''
    #execute query
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    con.commit()
    con.close()

setup_db()


