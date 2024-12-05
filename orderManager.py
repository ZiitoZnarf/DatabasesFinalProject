import dbSearch
import sqlite3
import random


dbName = 'ClothingStore.db';
def viewCart(email):

    cart = getCart(email)

    if (cart.__len__() != 0):
        print("CART:")
        header = f"{'Description':<30}{'Broad Type':<15}{'Specific Type':<15}{'Size':<10}{'Brand':<15}{'Quantity':<15}{'Price':<10}{'Gender':<10}"
        print(header)
        itemNum = 1

        for item in cart:
            # Find the gender of the clothing
            if item[7] == 1:
                gender = "F"
            elif item[8] == 1:
                gender = "M"
            elif item[9] == 1:
                gender = "Y"

            # Print the info of the item formatted to match the header
            print(f"{itemNum} {item[0]:<28}{item[1]:<15}{item[2]:<15}{item[3]:<10}"
                  f"{item[4]:<15}{item[5]:<15}{item[6]:<10}{gender:<10}")
            itemNum += 1

        option = input("Would You like to edit cart or check out cart?\n(e)Edit Cart\n(c)Checkout\n(b)Exit\n")
        if (option == 'e'):
            editCart(email)
        elif (option == 'c'):
            CompletePurchase(email)
        elif(option == 'b'):
            print()
    else:
        print("Cart is empty")
    
    return cart

def getCart(email):

    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""SELECT Description, BroadType, SpecificType, Size, Brand, Quantity, Price, GenderF, GenderM, GenderY
                    FROM CUSTOMER_ORDER
                    INNER JOIN PROFILE p ON CUSTOMER_ORDER.ProfileEmail = p.Email
                    NATURAL JOIN HOLDS
                    INNER JOIN CUSTOMER_ORDER o ON o.OrderNum = HOLDS.OrderNum
                    INNER JOIN CLOTHING c ON HOLDS.ClothUniID = c.UniqueNum
                    WHERE o.Status = 'CA' AND p.Email = ?""", [email])
    cart = c.fetchall()

    if(len(cart)==0):
        c.execute("Select * from CUSTOMER_ORDER  WHERE ProfileEmail = ? AND Status = 'CA'", (email,))
        check = c.fetchall()
        if len(check) == 0:
            createCart(email)

    c.close()
    conn.close()
    return cart

def createCart(email):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    rand = random.randint(100, 999)
    order = 'ORDER' + str(rand) + ''

    c.execute("SELECT BillingAddress FROM PROFILE WHERE Email = (?)", (email,))
    bill = c.fetchall()
    for item in bill:
        c.execute("""
            INSERT INTO CUSTOMER_ORDER (OrderNum, ShipAdd, Status, ProfileEmail)
            VALUES (?, ?, ?, ?)
            """, (order, item[0], 'CA', email))
        conn.commit()
    c.close()
    conn.close()

def editCart(email):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""SELECT o.OrderNum,ClothUniID,Description, BroadType, SpecificType, Size, Brand, Price, Quantity, GenderF, GenderM, GenderY
                FROM CUSTOMER_ORDER
                INNER JOIN PROFILE p ON CUSTOMER_ORDER.ProfileEmail = p.Email
                NATURAL JOIN HOLDS
                INNER JOIN CUSTOMER_ORDER o ON o.OrderNum = HOLDS.OrderNum
                INNER JOIN CLOTHING c ON HOLDS.ClothUniID = c.UniqueNum
                WHERE o.Status = 'CA' AND p.Email = ?""", (email,))
    cart = c.fetchall()

    itemNumInput = input("Which item would you like to edit?\n(row number to select item else press c to cancel)\n")
    if itemNumInput == 'c':
        print()
    else:
        itemNumInput = int(itemNumInput)
        itemNum = 1
        for item in cart:
            if itemNum == itemNumInput:
                editOption = input("Would you like to:\na)Remove from cart\nb)change quantity\n")
                if(editOption == 'a'):
                    c.execute("DELETE FROM HOLDS WHERE OrderNum=(?) AND ClothUniID = (?)", (item[0], item[1]))
                    conn.commit()
                elif(editOption == 'b'):
                    quantity = int(input("What quantity would you Like to change it to?\n"))
                    c.execute("UPDATE HOLDS set Quantity = (?) WHERE OrderNum = (?) AND ClothUniID = (?)",(quantity, item[0],item[1]))
                    conn.commit()
                else:
                    print("Input invalid")
            itemNum += 1
    c.close()
    conn.close()

def CompletePurchase(email):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT CardInfo,BillingAddress FROM PROFILE WHERE Email = (?)", (email,))
    paymentInfo = c.fetchall()

    for item in paymentInfo:
        if item[0] == '<null>' or item[1] == '<null>':
            print("Profile does not contain payment method. Please implement a payment method in profile.")
        else:
            c.execute("UPDATE CUSTOMER_ORDER SET Status = 'Confirmed' where ProfileEmail = (?) AND Status = 'CA'", (email,))
            conn.commit()
            createCart(email)
            print("Your Purchase Order has been confirmed")



    c.close()
    conn.close()

def viewPastOrders(email):
    conn = sqlite3.connect(dbName )
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""SELECT Description, BroadType, SpecificType, Size, Brand, Price, Quantity, GenderF, GenderM, GenderY, o.OrderNum
                FROM CUSTOMER_ORDER
                INNER JOIN PROFILE p ON CUSTOMER_ORDER.ProfileEmail = p.Email
                NATURAL JOIN HOLDS
                INNER JOIN CUSTOMER_ORDER o ON o.OrderNum = HOLDS.OrderNum
                INNER JOIN CLOTHING c ON HOLDS.ClothUniID = c.UniqueNum
                WHERE o.Status != 'CA' AND p.Email = ? AND Quantity != '<null>'""", (email,))
    order = c.fetchall()

    c.execute("""SELECT DISTINCT o.OrderNum FROM CUSTOMER_ORDER o
                           INNER JOIN PROFILE p ON o.ProfileEmail = p.Email
                           INNER JOIN HOLDS h ON h.OrderNum = o.OrderNum
                            WHERE ProfileEmail = (?) 
                            AND Status != 'CA'; """, [email])
    order_id = c.fetchall()

    if order.__len__() != 0:
        print("Past Orders:")
        itemNum = 1
        orderNum = 1
        for iterOrder in order_id:
            print("orderNum:", iterOrder[0])
            header = f"{'Description':<30}{'Broad Type':<15}{'Specific Type':<15}{'Size':<10}{'Brand':<15}{'Quantity':<15}{'Price':<10}{'Gender':<10}"
            print(header)
            for item in order:
                if iterOrder[0] == item[10]:

                    orderNum += 1
                    # Find the gender of the clothing
                    if item[7] == 1:
                        gender = "F"
                    elif item[8] == 1:
                        gender = "M"
                    elif item[9] == 1:
                        gender = "Y"

                    # Print the info of the item formatted to match the header
                    print(f"{itemNum} {item[0]:<28}{item[1]:<15}{item[2]:<15}{item[3]:<10}"
                          f"{item[4]:<15}{item[5]:<15}{item[6]:<10}{gender:<10}")
                    itemNum += 1
    else:
        print("No Past Orders")
    c.close()
    conn.close()


viewCart('johnsmith@email.com')