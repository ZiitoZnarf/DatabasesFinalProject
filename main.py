import sqlite3, dbSearch, orderManager


database = "database.db"
employee_domain = "superclothing.com"

def main():
    conn = get_connection()

    print("==Welcome to Super Clothing Purchasing==\n")
    inp_login = input("Would you like to Register (R), Login (L), or Quit (Q): ")

    while True:
        #LOGIN
        if inp_login.lower() == "l":
            #execute login
            print("\n--Enter Login Information--\n")
            login_success = False
            valid = 0
            email = ""


            #While Not Information Incorrect
            while not login_success:
                inp_email = input("Please enter your email: ")
                inp_password = input("Please enter your password: ")

                #Return Values (-1 = login incorrect | 1 = customer login valid | 2 = employee login valid)
                valid = login_valid(conn, inp_email, inp_password)

                if valid == -1:
                    print("Given Username and/or Password are incorrect\n")
                    inp_tryagain = input("Press [ENTER] to try again, or go back to start menu (Q): ")
                    if inp_tryagain.lower() == "q":
                        login_success = True
                        valid = 0
                else:
                    login_success = True
                    email = inp_email

            #continue with user option selection
            if valid == 1:
                customer_options(conn, email)
            elif valid == 2:
                employee_options(conn, email)

            inp_login = input("Would you like to Register (R), Login (L), or Quit (Q): ")

        #REGISTER
        elif inp_login.lower() == "r":
            #execute register
            print("\n--Register New Account--\n")
            register_success = False
            valid = 0
            new_email = ""

            #Create email
            while not register_success:
                inp_email = input("Please enter your email: ")
                valid = email_valid(conn, inp_email)

                if valid == -1:
                    print("Email already has a registered Account")
                elif valid == -2:
                    print("Invalid email address")

                if valid == 1:
                    register_success = True
                    new_email = inp_email
                else:
                    inp_tryagain = input("Press [ENTER] to try again, or go back to start menu (Q): ")
                    if inp_tryagain.lower() == "q":
                        register_success = True


            if valid == 1:
                inp_password = input("Please enter your password: ")
                while len(inp_password) < 1:
                    inp_password = input()

                inp_fname = input("Please enter your first name: ")
                while len(inp_fname) < 1:
                    inp_fname = input()

                inp_lname = input("Please enter your last name: ")
                while len(inp_lname) < 1:
                    inp_lname = input()

                add_profile(conn, new_email, inp_password, inp_fname, inp_lname)
                print("\nProfile Registered Successfully")

            inp_login = input("Would you like to Register (R), Login (L), or Quit (Q): ")

        #QUIT
        elif inp_login.lower() == "q":
            #execute register
            print("Thank you, have a nice day!")
            conn.close()
            exit(0)

        #INVALID INPUT
        else:
            #Execute inp_login failure
            inp_login = input("Selection not Recognized, please enter one of the following options:"
                              "\nRegister (R), Login (L), or Quit (Q): ")

def login_valid(conn, inp_email, inp_password):
    #Check login validity
    curs = conn.cursor()
    query = "SELECT * FROM PROFILE WHERE Email = ? AND Password = ?"
    curs.execute(query, (f"%{inp_email}%", f"%{inp_password}%"))
    result = curs.fetchone()

    #if the login information is not legitimate
    if result is None:
        return -1

    #Check if customer or employee
    if inp_email.count("@" + employee_domain) == 1:
        return 2
    else:
        return 1

def email_valid(conn, inp_email):
    curs = conn.cursor()
    query = "SELECT * FROM PROFILE WHERE Email = ?"
    curs.execute(query, f"%{inp_email}%")
    result = curs.fetchone()

    #Email already registered
    if result is not None:
        return -1

    #Checks to see that the DOMAIN of the email is valid (Local-Part is not checked)
    if inp_email.count("@") != 1:
        return -2
    if inp_email.count(".") == 0:
        return -2
    if inp_email.find("@") + 1 == inp_email.rfind("."):
        return -2
    if len(inp_email) - 1 == inp_email.rfind("."):
        return -2

    #If email is valid and not taken
    return 1

def add_profile(conn, inp_email, inp_password, inp_fname, inp_lname):
    curs = conn.cursor()
    query = "INSERT INTO PROFILE (Email, Password, FirstName, LastName) VALUES (?, ?, ?, ?)"
    curs.execute(query, (inp_email, inp_password, inp_fname, inp_lname))
    conn.commit()


def customer_options(conn, cust_email):
    logged_out = False

    print("==Customer Actions==\n")
    inp_selection = input("Would you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")

    while not logged_out:
        if inp_selection.lower() == 's':
            option_search(conn, cust_email)
            inp_selection = input("Would you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'c':
            option_cart(conn, cust_email)
            inp_selection = input("Would you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'p':
            option_profile(conn, cust_email)
            inp_selection = input("Would you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'q':
            logged_out = True
        else:
            print ("Selection not Recognized, please enter one of the following options:")
            inp_selection = input("Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")





def employee_options(conn, emp_email):
    logged_out = False

    print("==Employee Actions==\n")
    inp_selection = input("Would you like to Search Items (S), View Profile (P), or logout (Q): ")

    while not logged_out:
        if inp_selection.lower() == 's':
            option_search(conn, emp_email)
            inp_selection = input("Would you like to Search Items (S), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'p':
            option_profile(conn, emp_email)
            inp_selection = input("Would you like to Search Items (S), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'q':
            logged_out = True
        else:
            print ("Selection not Recognized, please enter one of the following options:")
            inp_selection = input("Search Items (S), View Profile (P), or logout (Q): ")


def option_search(conn, email):
    has_quit = False

    while not has_quit:
        filters = dbSearch.getFilters(database)
        dbSearch.search(filters)
        is_selecting = True

        print("Type an item's \"UniqueID\" to add it to cart.")
        inp_selection = input("You can also Change Search Filters (S) or Return to Menu (Q): ")

        while is_selecting:
            if inp_selection.lower() == "q":
                has_quit = True
                is_selecting = False

            elif inp_selection.lower() == "s":
                is_selecting = False

            elif not inp_selection.isdigit():
                print ("Selection not Recognized, please enter one of the following options:")
                inp_selection = input("An Item's \"UniqueID\", Change Search Filters (S), or Return to Menu (Q): ")

            else:
                inp_id = int(inp_selection)
                inp_quantity = input("Please enter item quantity: ")

                while (not inp_quantity.isdigit()) or (int(inp_quantity) < 1):
                    inp_quantity = input("Please enter item quantity (Must be a positive integer): ")

                dbSearch.addItem(inp_id, inp_quantity)

                print("Type an item's \"UniqueID\" to add it to cart.")
                inp_selection = input("You can also Change Search Filters (S) or Return to Menu (Q): ")


def option_cart(conn, email):
    has_quit = False

    while not has_quit:
        orderManager.viewCart(email)
        inp_selection = input("Please enter an input or Return to Menu (Q): ")


        if inp_selection.lower == "q":
            has_quit = True




def option_profile(conn, email):
    return

def get_connection():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn




if __name__ == '__main__':
    main()