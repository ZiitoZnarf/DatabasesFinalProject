import sqlite3, dbSearch, orderManager, ProfileManager


database = "ClothingStore.db"
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

            inp_login = input("\nWould you like to Register (R), Login (L), or Quit (Q): ")

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

            inp_login = input("\nWould you like to Register (R), Login (L), or Quit (Q): ")

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
    curs.execute(query, (f"{inp_email}", f"{inp_password}"))
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
    curs.execute(query, (f"{inp_email}",))
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

    print("\n==Customer Actions==\n")
    inp_selection = input("Would you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")

    while not logged_out:
        getCartOrderID(conn, cust_email)
        if inp_selection.lower() == 's':
            option_search(conn, cust_email)
            inp_selection = input("\nWould you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'c':
            option_cart(conn, cust_email)
            inp_selection = input("\nWould you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'p':
            option_profile(conn, cust_email)
            inp_selection = input("\nWould you like to Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'q':
            logged_out = True
        else:
            print ("Selection not Recognized, please enter one of the following options:")
            inp_selection = input("Search Items (S), View Cart (C), View Profile (P), or logout (Q): ")





def employee_options(conn, emp_email):
    logged_out = False

    print("\n==Employee Actions==\n")
    inp_selection = input("Would you like to Search Items (S), View Profile (P), or logout (Q): ")

    while not logged_out:
        if inp_selection.lower() == 's':
            option_search(conn, emp_email)
            inp_selection = input("\nWould you like to Search Items (S), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'p':
            option_profile(conn, emp_email)
            inp_selection = input("\nWould you like to Search Items (S), View Profile (P), or logout (Q): ")
        elif inp_selection.lower() == 'q':
            logged_out = True
        else:
            print ("Selection not Recognized, please enter one of the following options:")
            inp_selection = input("Search Items (S), View Profile (P), or logout (Q): ")


def option_search(conn, email):
    cartID = getCartOrderID(conn, email)
    has_quit = False
    isEmployee = False
    if email.count("@" + employee_domain) == 1:
        isEmployee = True

    ###while not has_quit:
    filters = dbSearch.getFilters(database)
    dbSearch.search(filters, cartID, database, isEmployee)
    '''''''''
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

                #dbSearch.addItem(inp_id, inp_quantity)

                print("Type an item's \"UniqueID\" to add it to cart.")
                inp_selection = input("You can also Change Search Filters (S) or Return to Menu (Q): ")
        '''''''''


def option_cart(conn, email):
    has_quit = False
    orderManager.viewCart(email)


def option_profile(conn, email):
    logged_out = False

    print("\n==Your Profile==\n")
    displayProfileInfo(conn, email)

    if email.count("@" + employee_domain) == 1:
        inp_selection = input("\nWould you like to Change Name (N) or Password (P) or Return to Menu (Q): ")
    else:
        inp_selection = input("\nWould you like to View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                              "Shipping Address (A), or Password (P), or Return to Menu (Q): ")

    while not logged_out:
        if inp_selection.lower() == 'o' and email.count("@" + employee_domain) == 0:
            orderManager.viewPastOrders(email)
            print("\n==Your Profile==\n")
            displayProfileInfo(conn, email)
            if email.count("@" + employee_domain) == 1:
                inp_selection = input("\nWould you like to Change Name (N) or Password (P) or Return to Menu (Q): ")
            else:
                inp_selection = input("\nWould you like to View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                                      "Shipping Address (A), or Password (P), or Return to Menu (Q): ")
        elif inp_selection.lower() == 'n':
            ProfileManager.editName(email, database)
            print("\n==Your Profile==\n")
            displayProfileInfo(conn, email)
            if email.count("@" + employee_domain) == 1:
                inp_selection = input("\nWould you like to Change Name (N) or Password (P) or Return to Menu (Q): ")
            else:
                inp_selection = input("\nWould you like to View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                                      "Shipping Address (A), or Password (P), or Return to Menu (Q): ")
        elif inp_selection.lower() == 'c' and email.count("@" + employee_domain) == 0:
            ProfileManager.editCardInfo(email, database)
            print("\n==Your Profile==\n")
            displayProfileInfo(conn, email)
            if email.count("@" + employee_domain) == 1:
                inp_selection = input("\nWould you like to Change Name (N) or Password (P) or Return to Menu (Q): ")
            else:
                inp_selection = input("\nWould you like to View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                                      "Shipping Address (A), or Password (P), or Return to Menu (Q): ")
        elif inp_selection.lower() == 'a' and email.count("@" + employee_domain) == 0:
            ProfileManager.editAddress(email, database)
            print("\n==Your Profile==\n")
            displayProfileInfo(conn, email)
            if email.count("@" + employee_domain) == 1:
                inp_selection = input("\nWould you like to Change Name (N) or Password (P) or Return to Menu (Q): ")
            else:
                inp_selection = input("\nWould you like to View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                                      "Shipping Address (A), or Password (P), or Return to Menu (Q): ")
        elif inp_selection.lower() == 'p':
            ProfileManager.editPassword(email, database)
            print("\n==Your Profile==\n")
            displayProfileInfo(conn, email)
            if email.count("@" + employee_domain) == 1:
                inp_selection = input("\nWould you like to Change Name (N) or Password (P) or Return to Menu (Q): ")
            else:
                inp_selection = input("\nWould you like to View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                                      "Shipping Address (A), or Password (P), or Return to Menu (Q): ")
        elif inp_selection.lower() == 'q':
            logged_out = True
        else:
            print ("\nSelection not Recognized, please enter one of the following options:")

            if email.count("@" + employee_domain) == 1:
                inp_selection = input("Change Name (N) or Password (P) or Return to Menu (Q): ")
            else:
                inp_selection = input("View Past Orders (O) or Change Name (N), CC-Number (C), \n"
                                      "Shipping Address (A), or Password (P), or Return to Menu (Q): ")

def displayProfileInfo(conn, email):
    curs = conn.cursor()

    query = "SELECT * FROM PROFILE WHERE Email = ?"
    curs.execute(query, (f"{email}",))


    tup = curs.fetchone()
    results = []
    for item in tup:
        results.append(item)

    print("Email: " + str(results[0]))
    print("Name: " + str(results[2]) + " " + str(results[3]))
    if email.count("@" + employee_domain) == 0:
        print("CC-Number: " + str(results[4]))
        print("Shipping Address: " + str(results[5]))


def getCartOrderID(conn, email):
    curs = conn.cursor()

    query = "SELECT * FROM CUSTOMER_ORDER WHERE ProfileEmail = ? AND Status = 'CA'"
    curs.execute(query, (f"{email}",))
    result = curs.fetchone()


    if result is None:
        #NEED TO CREATE NEW CART HERE
        curs.execute("SELECT Count(*) FROM CUSTOMER_ORDER")

        tup = curs.fetchone()
        results2 = []
        for item in tup:
            results2.append(item)
        num = int(results2[0]) + 1
        orderNum = "ORDER"
        if (num < 10):
            orderNum += "00" + str(num)
        elif (num < 100):
            orderNum += "0" + str(num)
        else:
            orderNum += str(num)

        curs.execute("SELECT BillingAddress FROM PROFILE WHERE Email = ?", (email,))
        result = curs.fetchone()
        results1 = []
        for item in result:
            results1.append(item)

        if results1[0] is None:
            curs.execute("INSERT INTO CUSTOMER_ORDER  VALUES (?, ?, ?, ?)",
                         (orderNum, "None", "CA", email))
        if results1[0] is not None:
            curs.execute("INSERT INTO CUSTOMER_ORDER  VALUES (?, ?, ?, ?)",
                         (orderNum, results1[0], "CA", email))

    else:
        results1 = []
        for item in result:
            results1.append(item)
        orderNum = results1[0]

        curs.execute("SELECT BillingAddress FROM PROFILE WHERE Email = ?", (email,))
        result = curs.fetchone()
        results2 = []
        for item in result:
            results2.append(item)

        if not results2[0] is None:
            curs.execute("UPDATE CUSTOMER_ORDER SET ShipAdd = ? WHERE ProfileEmail = ? AND status = 'CA'", (results2[0], email))


    conn.commit()
    return orderNum


def get_connection():
    conn = sqlite3.connect(database)
    return conn




if __name__ == '__main__':
    main()