from users import delete_user, login, create_account 

# Main loop to run the program 
def main():
    print("Pathfinding Algorithms Visualization: Explore BFS, DFS, UCS, and A* in Action.")
    print()
    print("Log in or Create an account.")

    while True:
        print("Choose an option:")
        print("1. Log In")
        print("2. Create Account")
        print("3. Delete Account")
        print("4. Exit")

        choice = input("Enter your option (1, 2, 3, or 4): ")

        if choice == '1':
            login()

        elif choice == '2':
            create_account()

        elif choice == '3':
            delete_user()

        elif choice == '4':
            break 

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4")

if __name__ == "__main__":
    main()
