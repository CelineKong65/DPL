import os

MEMBERS_FILE = "member.txt"
MEMBERS_ID_FILE = "member_id.txt"
ADMINS_FILE = "admin.txt"
PRODUCT_FILE = "product.txt"

class Member:
    def __init__(self, full_name="", member_id="", email="", password="", age="", gender="" , contact="", status="Active"):
        self.member_id = member_id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender
        self.contact = contact
        self.status = status
    
    def __str__(self):
        return f"{self.member_id}\n{self.full_name}\n{self.email}\n{self.password}\n{self.age}\n{self.gender}\n{self.contact}\n{self.status}"

class Admin:
    def __init__(self, name="", password="", contact="", position="admin"):
        allowed_positions = ["admin", "superadmin"]
        if position not in allowed_positions:
            raise ValueError(f"Invalid position: {position}. Must be 'admin' or 'superadmin'.")
        
        self.name = name
        self.password = password
        self.contact = contact
        self.position = position

    def __str__(self):
        return f"{self.name}\n{self.password}\n{self.contact}\n{self.position}"

members = []
logged_in_member = ""
logged_in_admin = ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_members():
    global members
    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as file:
            members = []
            data_lines = []
            for line in file:
                line = line.strip()
                if line != "":
                    data_lines.append(line)

                if len(data_lines) == 8:
                    member = Member(
                        member_id=data_lines[0],
                        full_name=data_lines[1],
                        email=data_lines[2],
                        password=data_lines[3],
                        age=data_lines[4],
                        gender=data_lines[5],
                        contact=data_lines[6],
                        status=data_lines[7]
                    )
                    members.append(member)
                    data_lines = []
    except FileNotFoundError:
        open(MEMBERS_FILE, "w", encoding='utf-8').close()


def get_next_member_id():
    try:
        with open(MEMBERS_ID_FILE, "r", encoding='utf-8') as file:
            read_current_id = file.readlines()
            if read_current_id:
                last_id = read_current_id[-1].strip()
                last_id_number = int(last_id[1:])
                next_id_number = last_id_number + 1 
                next_id = f"U{next_id_number:04d}"
                return next_id
            else:
                return "U0001"
    except FileNotFoundError:
        with open(MEMBERS_ID_FILE, "w", encoding='utf-8') as file:
            file.write("\nU0001\n")
        return "U0001"

def save_member(member):
    with open(MEMBERS_FILE, "a", encoding='utf-8') as file:
        file.write(f"\n\n{member.member_id}\n{member.full_name}\n{member.email}\n{member.password}\n{member.age}\n{member.gender}\n{member.contact}\n{member.status}\n\n")

def signup():
    global logged_in_member 

    member_id = get_next_member_id()
    full_name = input("Enter your full name: ")
    status = "Active"

    while True:
        email = input("Enter your email (example: xuanting@example.com): ")

        clean_email = ""
        
        at = False
        dot = False
        for char in email:
            if char != ' ' and char != '\n':
                clean_email += char
            if char == '@':
                at = True
            if char == '.':
                dot = True

        if not at or not dot:
            print("Invalid email format. Please include @ and . in your email!")
            continue

        same = False
        for member in members:
            stored_email = member.email

            if len(stored_email) == len(email):
                match = True
                for i in range(len(email)):
                    if email[i] != stored_email[i]:
                        match = False
                        break
                if match:
                    same = True
                    break

        if same:
            print("This email is already registered. Please use a different email!")
            continue
        
        break

    while True:
        password = ""
        password = input("Enter your new password (example: Xuanting123): ")

        if len(password) < 8:
            print("Password must be at least 8 characters!")
            continue

        upper = False
        lower = False
        digit = False

        for char in password:
            if 'A' <= char <= 'Z':
                upper = True
            elif 'a' <= char <= 'z': 
                lower = True
            elif '0' <= char <= '9': 
                digit = True

        if not upper:
            print("Password must contain at least one uppercase letter!")
            continue
        if not lower:
            print("Password must contain at least one lowercase letter!")
            continue
        if not digit:
            print("Password must contain at least one digit!")
            continue
        
        confirm_password = input("Confrim your password: ")
        if confirm_password != password:
            print("Passwords do not match!")
            continue
    
        break

    while True:
        age = input("Enter your age: ")

        if len(age) != 2:
            print("Age must be exactly 2 digits!")
            continue

        is_digit = True
        for char in age:
            if char < '0' or char > '9':
                is_digit = False

        if not is_digit:
            print("Age must contain only digits!")
            continue

        if age[0] == '0':
            print("Age cannot start with 0!")
            continue

        break

    while True:
        gender = input("Enter your gender (male or female): ")

        is_valid= False

        if len(gender) == 4:
            if ((gender[0] == 'M' or gender[0] == 'm') and
                (gender[1] == 'a' or gender[1] == 'A') and
                (gender[2] == 'l' or gender[2] == 'L') and
                (gender[3] == 'e' or gender[3] == 'E')):
                is_valid = True

        elif len(gender) == 6:
            if ((gender[0] == 'F' or gender[0] == 'f') and
                (gender[1] == 'e' or gender[1] == 'E') and
                (gender[2] == 'm' or gender[2] == 'M') and
                (gender[3] == 'a' or gender[3] == 'A') and
                (gender[4] == 'l' or gender[4] == 'L') and
                (gender[5] == 'e' or gender[5] == 'E')):
                is_valid = True

        if not is_valid:
            print("Please enter 'Male', 'Female', 'male' or 'female'!")
            continue
        break

    while True:
        contact = input("Enter your contact number (example: 012-34567890): ")

        if len(contact) < 4 or contact[3] != '-':
            print("Format must be like 012-34567890 with a dash at the 4th position!")
            continue

        part1 = ""
        part2 = ""
        for i in range(len(contact)):
            if i < 3:
                part1 += contact[i]
            elif i > 3:
                part2 += contact[i]


        if not (part1[0] == '0' and part1[1] == '1'):
            print("Phone number must start with '01'!")
            continue

        combined = part1 + part2
        only_digits = True
        for c in combined:
            if not ('0' <= c <= '9'):
                only_digits = False
                break
        if not only_digits:
            print("Phone number cannot contain symbols or space!")
            continue

        if len(combined) != 10 and len(combined) != 11:
            print("Phone number must be 10 or 11 digits!")
            continue
    
        break
   
    if not all([full_name, password, confirm_password, email, age, gender, contact]):
        print("Error : All fields are required!")
    elif password != confirm_password:
        print("Error : Passwords do not match!")
    else:
        new_member = Member(full_name=full_name, member_id=member_id, email=email, password=password, age=age, gender=gender, contact=contact,status=status)
        members.append(new_member)

        with open(MEMBERS_ID_FILE, "a", encoding='utf-8') as file:
            file.write(member_id + "\n")
            
        save_member(new_member)
        print(f"Registration successful! Your Member ID: {member_id}")
        input("\nPress [ENTER] to return to login menu.")
        clear_screen()

def to_lower_case(s):
    result = ""
    for char in s:
        if 'A' <= char <= 'Z':
            result += chr(ord(char) + 32)
        else:
            result += char
    return result

def login():
    global logged_in_member 
    
    email = input("\nEnter your email :").strip()
    password = input("Enter your password :").strip()

    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 8):  
            stored_email = lines[i + 2]
            stored_password = lines[i + 3]
            status = lines[i + 7]

            if email == stored_email:
                if to_lower_case(status) != "active":
                    print("Your account is inactive. Please contact admin.")
                    input("\nPress [ENTER] to return to login menu.")
                    clear_screen()
                    return False
                
                attempts = 0
                while attempts < 3:
                    if password == stored_password:
                        print("Logged in Successfully!")
                        logged_in_member = Member(
                            full_name=lines[i + 1],
                            member_id=lines[i],
                            email=lines[i + 2],
                            password=lines[i + 3],
                            age=lines[i + 4],
                            gender=lines[i + 5],
                            contact=lines[i + 6],
                            status=lines[i + 7]
                        )
                        input("\nPress [ENTER] to continue.")
                        return main_menu()
                    else:
                        attempts += 1
                        print(f"Incorrect password! Attempts left: {3 - attempts}")
                        password = input("Please enter your password again: ").strip()

                print("Too many failed attempts. Login terminating.")
                input("\nPress [ENTER] to return to login menu.")
                clear_screen()
                return False
                    
        print("Email not found.\n")
        input("\nPress [ENTER] to continue.")
        clear_screen()
        return False

    except FileNotFoundError:
        print("Error: Members file not found!")
        return False

def update_member(updated_member):
    try:
        with open(MEMBERS_FILE, "r", encoding='utf-8') as file:
            content = file.read().strip()

        members = content.split("\n\n")

        updated_members = []

        for member_data in members:
            fields = member_data.splitlines()

            if fields and fields[0] == updated_member.member_id:
                new_member_data = [
                    updated_member.member_id,
                    updated_member.full_name,
                    updated_member.email,
                    updated_member.password,
                    str(updated_member.age),
                    updated_member.gender,
                    updated_member.contact,
                    updated_member.status
                ]
                updated_members.append("\n".join(new_member_data))
            else:
                updated_members.append(member_data)

        new_content = "\n\n".join(updated_members)

        with open(MEMBERS_FILE, "w", encoding='utf-8') as file:
            file.write(new_content)

    except FileNotFoundError:
        print("Member file not found.")
    except Exception as e:
        print(f"An error occurred while updating member: {e}")
    
def member_profile():
    global logged_in_member 

    clear_screen()

    while True:
        print("------------------------------------------------------------------")
        print("|                         YOUR PROFILE                           |")
        print("------------------------------------------------------------------")
        print(f"| 1. Member ID         : {logged_in_member.member_id:<40}|")
        print(f"| 2. Full Name         : {logged_in_member.full_name:<40}|")
        print(f"| 3. Email             : {logged_in_member.email:<40}|")
        print(f"| 4. Password          : {logged_in_member.password:<40}|")
        print(f"| 5. Age               : {logged_in_member.age:<40}|")
        print(f"| 6. Gender            : {logged_in_member.gender:<40}|")
        print(f"| 7. Contact Number    : {logged_in_member.contact:<40}|")
        print("------------------------------------------------------------------")

        choice = input("\nDo you want to edit your profile? (Y/N) : ")

        if choice == "Y" or choice == "y" or choice == "yes":
            edit_member_profile()
        elif choice == "N" or choice == "n" or choice == "no":
            input("Press [Enter] to return to the main menu.")
            clear_screen()
            return main_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def edit_member_profile():
    global logged_in_member 

    while True:
        clear_screen()
        print("------------------------------------------------------------------")
        print("|                       EDIT YOUR PROFILE                        |")
        print("------------------------------------------------------------------")
        print("| 1. Member ID (Not Editable)                                    |")
        print("| 2. Full Name                                                   |")
        print("| 3. Email                                                       |")
        print("| 4. Password                                                    |")
        print("| 5. Age                                                         |")
        print("| 6. Gender                                                      |")
        print("| 7. Contact Number                                              |")
        print("| 8. Return to Profile Menu                                      |")
        print("------------------------------------------------------------------")

        choice = input("\nSelect the number you want to edit (1-8): ")

        if choice == "1":
            input("\nMember ID cannot be edited. Press [ENTER] to continue.")

        elif choice == "2":
            logged_in_member.full_name = input("Enter new Full Name: ")
            update_member(logged_in_member)
            print("Full Name updated successfully!")
            input("Press [ENTER] to continue.")

        elif choice == "3":
            while True:
                logged_in_member.email = input("Enter your new email (example: xuanting@example.com): ")

                clean_email = ""
                
                at = False
                dot = False
                for char in logged_in_member.email:
                    if char != ' ' and char != '\n':
                        clean_email += char
                    if char == '@':
                        at = True
                    if char == '.':
                        dot = True

                if not at or not dot:
                    print("Invalid email format. Please include @ and . in your email!")
                    continue

                update_member(logged_in_member)
                print("Email updated successfully!")
                input("Press [ENTER] to continue.")

                break

        elif choice == "4":
            while True:
                logged_in_member.password = ""
                logged_in_member.password = input("Enter your new password (example: Xuanting123): ")

                if len(logged_in_member.password) < 8:
                    print("Password must be at least 8 characters!")
                    continue

                upper = False
                lower = False
                digit = False

                for char in logged_in_member.password:
                    if 'A' <= char <= 'Z':
                        upper = True
                    elif 'a' <= char <= 'z': 
                        lower = True
                    elif '0' <= char <= '9': 
                        digit = True

                if not upper:
                    print("Password must contain at least one uppercase letter!")
                    continue
                if not lower:
                    print("Password must contain at least one lowercase letter!")
                    continue
                if not digit:
                    print("Password must contain at least one digit!")
                    continue
                
                confirm_password = input("Confrim your password: ")
                if confirm_password != logged_in_member.password:
                    print("Passwords do not match!")
                    continue
            
                update_member(logged_in_member)
                print("Password updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "5":
            try:
                while True:
                    logged_in_member.age = input("Enter new age: ")

                    if len(logged_in_member.age) != 2:
                        print("Age must be exactly 2 digits!")
                        continue

                    is_digit = True
                    for char in logged_in_member.age:
                        if char < '0' or char > '9':
                            is_digit = False

                    if not is_digit:
                        print("Age must contain only digits!")
                        continue

                    if logged_in_member.age[0] == '0':
                        print("Age cannot start with 0!")
                        continue

                    update_member(logged_in_member)
                    print("Age updated successfully!")
                    break
            except ValueError:
                print("Invalid input! Age must be a number.")
            input("Press [ENTER] to continue.")

        elif choice == "6":
            while True:
                logged_in_member.gender = input("Enter new gender (male or female): ")

                is_valid= False

                if len(logged_in_member.gender) == 4:
                    if ((logged_in_member.gender[0] == 'M' or logged_in_member.gender[0] == 'm') and
                        (logged_in_member.gender[1] == 'a' or logged_in_member.gender[1] == 'A') and
                        (logged_in_member.gender[2] == 'l' or logged_in_member.gender[2] == 'L') and
                        (logged_in_member.gender[3] == 'e' or logged_in_member.gender[3] == 'E')):
                        is_valid = True

                elif len(logged_in_member.gender) == 6:
                    if ((logged_in_member.gender[0] == 'F' or logged_in_member.gender[0] == 'f') and
                        (logged_in_member.gender[1] == 'e' or logged_in_member.gender[1] == 'E') and
                        (logged_in_member.gender[2] == 'm' or logged_in_member.gender[2] == 'M') and
                        (logged_in_member.gender[3] == 'a' or logged_in_member.gender[3] == 'A') and
                        (logged_in_member.gender[4] == 'l' or logged_in_member.gender[4] == 'L') and
                        (logged_in_member.gender[5] == 'e' or logged_in_member.gender[5] == 'E')):
                        is_valid = True

                if not is_valid:
                    print("Please enter 'Male', 'Female', 'male' or 'female'!")
                    continue

                update_member(logged_in_member)
                print("Gender updated successfully!")
                input("Press [ENTER] to continue.")
                break

        elif choice == "7":
            while True:
                logged_in_member.contact  = input("Enter your contact number (example: 012-34567890): ")

                if len(logged_in_member.contact) < 4 or logged_in_member.contact[3] != '-':
                    print("Format must be like 012-34567890 with a dash at the 4th position!")
                    continue

                part1 = ""
                part2 = ""
                for i in range(len(logged_in_member.contact)):
                    if i < 3:
                        part1 += logged_in_member.contact[i]
                    elif i > 3:
                        part2 += logged_in_member.contact[i]


                if not (part1[0] == '0' and part1[1] == '1'):
                    print("Phone number must start with '01'!")
                    continue

                combined = part1 + part2
                only_digits = True
                for c in combined:
                    if not ('0' <= c <= '9'):
                        only_digits = False
                        break
                if not only_digits:
                    print("Phone number cannot contain symbols or space!")
                    continue

                if len(combined) != 10 and len(combined) != 11:
                    print("Phone number must be 10 or 11 digits!")
                    continue
    
                update_member(logged_in_member)
                print("Contact Number updated successfully!")
                input("Press [ENTER] to continue.")
                break
        
        elif choice == "8":
            input("\nPress [ENTER] to return to your profile.")
            clear_screen()
            return member_profile()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()
    
def login_menu():
    global logged_in_member 

    while True:
        print("\n===============================================================")
        print("                   WELOCOME TO YESMOLAR BAKERY                 ")
        print("===============================================================")
        print("1.    Sign Up  ")
        print("2.    Login  ")
        print("3.    Admin Login  ")
        print("4.    Exit  ")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            load_members()
            signup()
        elif choice == '2':
            login()
        elif choice == '3':
            admin_login()
        elif choice == '4':
            print("\nThank you for visiting Yesmolar Bakery!\n")
            exit()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def admin_login():
    global logged_in_admin

    name = input("\nEnter your name :").strip()
    password = input("Enter your password :").strip()

    try:
        with open(ADMINS_FILE, "r", encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != ''] 

        for i in range(0, len(lines), 4):  
            stored_name = lines[i]
            stored_password = lines[i + 1]
            stored_position = lines[i + 3]

            if name == stored_name:
                attempts = 0
                while attempts < 3:
                    if password == stored_password:
                        print("Logged in Successfully!")
                        print(f"Welcome {stored_position}!\n")
                        logged_in_admin = Admin(
                            name=lines[i],
                            password=lines[i + 1],
                            contact=lines[i + 2],
                            position=lines[i + 3]
                        )
                        input("\nPress [ENTER] to continue.")
                        clear_screen()
                        return admin_menu()
                        
                    else:
                        attempts += 1
                        print(f"Incorrect password! Attempts left: {3 - attempts}")
                        password = input("Please enter your password again: ").strip()

                print("Too many failed attempts. Login terminating.")
                input("\nPress [ENTER] to return to login menu.")
                clear_screen()
                return False
                    
        print("Name not found.\n")
        input("\nPress [ENTER] to continue.")
        clear_screen()
        return False

    except FileNotFoundError:
        print("Error: Admins file not found!")
        return False
    
def admin_menu():
    global logged_in_member 

    while True:
        print("===============================================================")
        print("                          ADMIN MENU                           ")
        print("===============================================================")
        print(" [1] Manage Pastry Inventory")
        print(" [2] Manage Member List")
        print(" [3] Manage Admin List")
        print(" [4] Manage Feedback and Rating")
        print(" [5] View Dashboard")
        print(" [6] My profile")
        print(" [7] Log Out")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            return
        elif choice == '2':
            return
        elif choice == '3':
            return
        elif choice == '4':
            return
        elif choice == '5':
            return
        elif choice == '6':
            print("admin_profile()")
        elif choice == '7':
            input("\nPress [ENTER] to logout.")
            clear_screen()
            return login_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")
            clear_screen()

def main_menu():
    global logged_in_member
    if not logged_in_member:
        print("Error: No user logged in.")
        return

    while True:
        clear_screen()
        print(f"Welcome {logged_in_member.full_name} ! ")
        print("===============================================================")
        print("                            Main Menu                          ")
        print("===============================================================")
        print(" [1] Browse Products")
        print(" [2] View My Cart")
        print(" [3] My Profile")
        print(" [4] Rate Our System")
        print(" [5] Log Out")
        print("===============================================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("filter_products()")
        elif choice == '2':
            print("cart = []")
            print("display_cart(cart)")
        elif choice == '3':
            member_profile()
        elif choice == '4':
            print("rating")
        elif choice == '5':
            input("\nPress [ENTER] to logout.")
            clear_screen()
            return login_menu()
        else:
            input("\nInvalid choice. Press [ENTER] to try again.")

def main():
    global logged_in_member
    logged_in_member = None 

    if not os.path.exists(PRODUCT_FILE):
        print(f"Error: Product file '{PRODUCT_FILE}' not found.")
        input("Press [ENTER] to exit.")
        return
    
    login_menu()

    main_menu()
main()