from db_connection import get_db_connection
import hashlib
import os

# Everything I used about hashing and salting the password of the user, I did not come up with it on my own. 
# I saw it online (I used ChatGPT to help me understand and implement the concepts of hashing and salting) and that sounded very cool to me 
# so I decided to implement it in this project. 


# Function to salt and hash the password entered by the user
# salting is important and an additional layer of security on top of hashing
# since people might have the same password. 
def salt_hash_password(password):
    salt = os.urandom(16) # Generate a 16-byte (128 bits) random salt
    salted_password_bytes = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(salted_password_bytes).hexdigest()
    return salt, hashed_password

# Function to insert a user in the DB 
def insert_user(username, password, role):
    conn = get_db_connection()
    cur = conn.cursor()

    # Hash and generate a salt for the password
    salt, hashed_password = salt_hash_password(password)
    try:
        cur.execute("""
            INSERT INTO Users (username, salt, password, role)
            VALUES (%s, %s, %s, %s)""",
                    (username, salt, hashed_password, role))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# Function to check whether the User is already in the DB 
def user_in_DB(username):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT username
            FROM Users
            WHERE username = %s""",
                    (username,))

        result = cur.fetchone()
        
        if result:
            return True
        else:
            return False
    finally:
        cur.close()
        conn.close()
   
# Function to hash the entered password from with the salt from the database.
# This will help re-create the hashed password stored in the DB which will ultimately help in checking whether
# the password entered by the user is right or not.
def re_salt_hash_password(password, salt):
    salted_password_bytes = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(salted_password_bytes).hexdigest()
    return hashed_password

# Function to check whether the password is correct or not. 
# First retrieve the password from the DB based on the username and then check if it matches
# with what the user entered.
def check_password(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT salt, password
            FROM Users
            WHERE username = %s""",
                    (username,))

        result = cur.fetchone()

        if result:
            salt_in_db, password_in_db = result

            # Hash the entered password and salt it to see if it is the same as the one in the DB 
            hashed_entered_password = re_salt_hash_password(password, salt_in_db)
            if password_in_db == hashed_entered_password:
                return True
            else:
                return False
        else:
            return False

    finally:
        cur.close()
        conn.close()

# Function to update the users password. This function should be called when the user 
# does not remember their password or just if they want to change their password
def update_password(username, new_password):
    conn = get_db_connection()
    cur = conn.cursor()

    # Hash and generate a salt for the new password
    new_salt, new_hashed_password = salt_hash_password(new_password)
    try:
        cur.execute("""
            UPDATE Users
            SET salt = %s, password = %s 
            WHERE username = %s""",
                    (new_salt, new_hashed_password, username))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# Function to delete a user from the database. This can be used in case the user wants to delete their account.
def delete_user(username):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            DELETE FROM Users
            WHERE username = %s""",
                    (username,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# Function to implement the login functionality
def login():
    print("Pathfinding Algorithms Visualization: Explore BFS, DFS, UCS, and A* in Action.")
    print()
    print("Log in")
    print("Enter 'exit' quit")
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        role = input("Enter your role ('admin', or 'user'): ")

        if user_in_DB(username):
            print("The username you entered is already being used. Choose a different username.")
        if check_password(password):
            print("The password you entered is incorrect.")
            print("Try again or enter 'change your password' to change your password")
        if check_role(role):
            print("")

print(login())

#while True:
#    username = input("Enter the username: ")
#    password = input("Enter your password: ")
#    role = input("Enter your role: ")
#
#    if user_in_DB(username):
#        print("The username you entered  is already in the DB bro")
#        print("Choose a different username")
#
#    if role != 'admin' or role != 'user':
#        print("The role should be 'admin' or 'user'")
#
#    else:
#        insert_user(username, password, role)
