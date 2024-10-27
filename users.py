from db_connection import get_db_connection
from algorithms import get_city_id 
import hashlib
import os
from algorithms import bfs, dfs, ucs, a_star_search, city_in_DB

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
def insert_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()

    # Hash and generate a salt for the password
    salt, hashed_password = salt_hash_password(password)
    try:
        cur.execute("""
            INSERT INTO Users (username, salt, password)
            VALUES (%s, %s, %s)""",
                    (username, salt, hashed_password))
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
def right_password(username, password):
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
def delete_user():
    conn = get_db_connection()
    cur = conn.cursor()

    confirmation = input("Are you sure you want to delete your account? Enter 'yes' to confirm: ")
    if confirmation.lower() != 'yes':
        print("Deletion of account was successfully cancelled.")
        return 

    while True:
        username = input("Choose a username: ")

        if not user_in_DB(username):
            print("The username you entered is invalid.")
            print("1. Try again.")
            print("2. Cancel the deletion.")
            option = input("Enter your option ('1' or '2'): ")

            if option == '1':
                continue
            
            elif option == '2':
                return 

            else:
                print("Invalid choice. Please enter '1' or '2'.")

        else:
            break

    while True: 
        password = input("Enter your password: ")

        if not right_password(username, password):
            print("The password you entered is incorrect")
            print("1. Try again.")
            print("2. Cancel the deletion.")
            option = input("Enter your option ('1' or '2'): ")

            if option == '1':
                continue

            elif option == '2':
                return
            
            else:
                print("Invalid choice. Please enter '1' or '2'.")

        else:
            break 
    
    try:
        cur.execute("""
            DELETE FROM Users
            WHERE username = %s""",
                    (username,))
        conn.commit()
        print("Your account was deleted successfully.")
    finally:
        cur.close()
        conn.close()

# Function to update the user information. 
# This might happen when the user selects other cities to explore 
# or try to use another algorithm 
def update_start_and_end_city(username, new_start_city_name, new_end_city_name):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get start_city_id and end_city_id
    new_start_city_id = get_city_id(new_start_city_name)
    new_end_city_id = get_city_id(new_end_city_name)

    try:
        cur.execute("""
            UPDATE Users
            SET start_city_id = %s, end_city_id = %s 
            WHERE username = %s""",
                    (new_start_city_id, new_end_city_id, username))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# Function to update the algorithm used by the user.
def update_algorithm(username, new_algorithm_chosen):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE Users
            SET algorithm_chosen = %s
            WHERE username = %s""",
                    (new_algorithm_chosen, username))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# Function to create an account 
def create_account():
    while True:
        new_username = input("Enter your username: ")

        if user_in_DB(new_username):
            print("The username you entered is already being used.")
            print("1. Try again.")
            print("2. Create Account. ")
            option = input("Enter your option (1 or 2): ")

            if option == '1':
                continue
            
            elif option == '2':
                create_account()
                return 

            else:
                print("Invalid choice. Please enter '1' or '2'.")

        else:
            break

    new_password = input("Choose a password: ")
    insert_user(new_username, new_password)
    print("Account successfully created. You can log in now.")

# Function to log the user into the program 
def login():
    while True:
        username = input("Enter your username: ")

        if not user_in_DB(username):
            print("The username you entered is invalid.")
            print("1. Try again.")
            print("2. Create Account. ")
            option = input("Enter your option (1 or 2): ")

            if option == '1':
                continue
            
            elif option == '2':
                create_account()
                return 

            else:
                print("Invalid choice. Please enter '1' or '2'.")

        else:
            break

    while True: 
        password = input("Enter your password: ")

        if not right_password(username, password):
            print("The password you entered is incorrect")
            print("1. Try again.")
            print("2. Change your password")
            option = input("Enter your option (1 or 2): ")

            if option == '1':
                continue

            elif option == '2':
                new_password = input("Enter your new password: ")
                update_password(username, new_password)
            
            else:
                print("Invalid choice. Please enter '1' or '2'.")

        else:
            break 

    while True:
        start_city_name = input("Enter a starting city: ").lower().replace(" ", "")

        if not city_in_DB(start_city_name):
            print("The starting city you entered is not in the database. Try again.")

        else:
            break 

    while True:
        end_city_name = input("Enter an ending city: ").lower().replace(" ", "")
        
        if not city_in_DB(end_city_name):
            print("The ending city you entered is not in the database. Try again.")

        else:
            break 

    while True:
        print("Choose from the following algorithms the one you want to use:")
        print("1. BFS")
        print("2. DFS")
        print("3. UCS")
        print("4. AStar")
        option = input("Enter you option ('bfs', 'dfs', 'ucs', or 'astar'): ").lower()

        if option == 'bfs':
            path = bfs(start_city_name, end_city_name)
            print("Breadth First Search Path found: ", path)
            break 

        elif option == 'dfs':
            path = dfs(start_city_name, end_city_name)
            print("Depth First Search Path found: ", path)
            break 

        elif option == 'ucs':
            path = ucs(start_city_name, end_city_name)
            print("Uniformed Cost Search Path found: ", path)
            break 

        elif option == 'astar':
            path = a_star_search(start_city_name, end_city_name)
            print("A*Star Path found: ", path)
            break
        
        else:
            print("Invalid choice. Please enter bfs, dfs, ucs, or a*star")

    # Update the cities from the previous selected cities when the user last logged in.
    update_start_and_end_city(username, start_city_name, end_city_name)

    # Update the algorithm from the previous selected algorithm when the user last logged in.
    update_algorithm(username, option)

