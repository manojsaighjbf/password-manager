import os
import hashlib
import re

PASSWORD_FILE = "passwords.txt"

# Function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate password strength
def validate_password(password):
    if len(password) < 8:
        print("Password is too short. It must be at least 8 characters.")
        return False
    if not re.search(r"[A-Za-z]", password):
        print("Password must contain at least one letter.")
        return False
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one number.")
        return False
    return True

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux
        os.system('clear')

# Function to load passwords from the file
def load_passwords():
    try:
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, "r") as file:
                lines = file.readlines()
                return dict(line.strip().split(":", 1) for line in lines)
    except Exception as e:
        print(f"Error loading passwords: {e}")
    return {}

# Function to save passwords to the file
def save_passwords():
    try:
        with open(PASSWORD_FILE, "w") as file:
            for account, password in passwords.items():
                file.write(f"{account}:{password}\n")
    except Exception as e:
        print(f"Error saving passwords: {e}")

# Function to add a new password
def add_password(account, password):
    if not validate_password(password):
        return
    hashed_password = hash_password(password)
    passwords[account] = hashed_password
    save_passwords()
    print(f"Password for '{account}' added successfully!")

# Function to update an existing password
def update_password(account, current_password, new_password):
    if not validate_password(new_password):
        return
    hashed_new_password = hash_password(new_password)
    if account in passwords:
        if passwords[account] == hash_password(current_password):  # Compare hashed versions
            passwords[account] = hashed_new_password
            save_passwords()
            print(f"Password for '{account}' updated successfully!")
        else:
            print("Current password is incorrect.")
    else:
        print(f"Account '{account}' not found. Use option 1 to add it.")

# Function to retrieve the password for an account
def get_password(account):
    hashed_password = passwords.get(account, None)
    if hashed_password:
        return hashed_password
    return None

# Function to view all stored passwords (hashed)
def view_all_passwords():
    if passwords:
        print("\nStored Passwords (hashed):")
        for account, password in passwords.items():
            print(f"{account}: {password}")
    else:
        print("No passwords stored.")

# Function to delete an account
def delete_account(account):
    if account in passwords:
        del passwords[account]
        save_passwords()
        print(f"Account '{account}' deleted successfully!")
    else:
        print(f"Account '{account}' not found.")

# Function to export passwords to a backup file
def export_passwords():
    try:
        with open("passwords_backup.txt", "w") as file:
            for account, password in passwords.items():
                file.write(f"{account}:{password}\n")
        print("Passwords exported to passwords_backup.txt")
    except Exception as e:
        print(f"Error exporting passwords: {e}")

# Main function with the menu and user choices
def main():
    global passwords
    passwords = load_passwords()

    print("\nPassword Manager")
    print("1. Add a new password")
    print("2. Retrieve a password")
    print("3. Update a password")
    print("4. Delete an account")
    print("5. View all passwords")
    print("6. Export passwords (Backup)")
    print("7. Exit")

    while True:
        clear_screen()  # Clear screen for a cleaner UI
        print("Password Manager Menu:")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Update a password")
        print("4. Delete an account")
        print("5. View all passwords")
        print("6. Export passwords (Backup)")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            account = input("Enter the account name: ")
            password = input("Enter the password: ")
            add_password(account, password)
        elif choice == "2":
            account = input("Enter the account name: ")
            password = get_password(account)
            if password:
                print(f"Password for '{account}': {password}")
            else:
                print(f"No password found for '{account}'.")
        elif choice == "3":
            account = input("Enter the account name: ")
            current_password = input("Enter the current password: ")
            new_password = input("Enter the new password: ")
            update_password(account, current_password, new_password)
            break
        elif choice == "4":
            account = input("Enter the account name: ")
            delete_account(account)
            break
        elif choice == "5":
            view_all_passwords()
            break
        elif choice == "6":
            export_passwords()
            break
        elif choice == "7":
            confirm_exit = input("Are you sure you want to exit? (y/n): ")
            if confirm_exit.lower() == 'y':
                print("Exiting Password Manager. Goodbye!")
                break
            else:
                print("Returning to the menu...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
