import sqlite3

def editName(desiredEmail, dbName):
    conn = connection(dbName)
    curs = conn.cursor()
    firstName = input("Enter new first name here: ")
    lastName = input("Enter new last name here: ")

    curs.execute("UPDATE PROFILE SET FirstName = ? WHERE Email = ?", [firstName, desiredEmail])
    curs.execute("UPDATE PROFILE SET LastName = ? WHERE Email = ?", [lastName, desiredEmail])

    conn.commit()
    curs.close()
    conn.close()

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
            curs.execute("UPDATE PROFILE SET Password = ? WHERE Email = ?", [newPassword, desiredEmail])
        else:
            print("Incorrect password. Access denied")

    conn.commit()
    curs.close()
    conn.close()

def editAddress(desiredEmail, dbName):
    conn = connection(dbName)
    curs = conn.cursor()

    newAddress = input("Enter new billing address: ")
    curs.execute("UPDATE PROFILE SET BillingAddress = ? WHERE Email = ?", [newAddress, desiredEmail])

    conn.commit()
    curs.close()
    conn.close()

def editCardInfo(desiredEmail, dbName):
    conn = connection(dbName)
    curs = conn.cursor()

    newCard = input("Enter new card info: ")
    if len(newCard) == 16 and newCard.isdigit():
        curs.execute("UPDATE PROFILE SET CardInfo = ? WHERE Email = ?", [newCard, desiredEmail])
    else:
        print("New card info is not valid.")

    curs.close()
    conn.close()

def connection(dbName):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    return conn
