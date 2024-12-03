import sqlite3

def editName(desiredEmail, dbName):
    conn = connection(dbName)
    curs = conn.cursor()
    firstName = input("Enter new first name here: ")
    lastName = input("Enter new last name here: ")

    curs.execute(f"UPDATE PROFILE SET FirstName = {firstName} WHERE Email = {desiredEmail}")
    curs.execute(f"UPDATE PROFILE SET LastName = {lastName} WHERE Email = {desiredEmail}")

    conn.close()
    curs.close()

def editPassword(desiredEmail, dbName):
    conn = connection(dbName)
    curs = conn.cursor()
    currentPassword = input("Enter password: ")
    curs.execute("SELECT Password FROM PROFILE WHERE Email = ?", (desiredEmail,))
    result = curs.fetchone()
    if result:
        password = result[0]
        if currentPassword == password:
            newPassword = input("Enter new password: ")
            curs.execute(f"UPDATE PROFILE SET Password = {newPassword} WHERE Email = {desiredEmail}")
        else:
            print("Incorrect password. Access denied")

    conn.close()
    curs.close()

def viewOrders(desiredEmail, dbName):
    conn = connection(dbName)
    curs = conn.cursor()

    curs.execute("SELECT * FROM CUSTOMER_ORDER WHERE ProfileEmail = ?", desiredEmail)
    orders = curs.fetchall()

    for order in orders:
        print(order)


    conn.close()
    curs.close()

def connection(dbName):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    return conn