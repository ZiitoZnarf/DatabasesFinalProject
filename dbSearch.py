import sqlite3

def getFilters(dbName):
    filters = []
    conn = getConnection(dbName)
    c = conn.cursor()

    print("For all of the following options, type skip to skip")


    filters.append(input("What is the name of the item?\t"))

    # Get all of the broad types available
    options = getOptions("SELECT BroadType FROM CLOTHINGSTORE", c)
    userMessage = f"What is the broad type? Please choose from these options: {options}"
    # Add the answer to our filters
    filters.append(getAnswer(userMessage, options))

    # Get all of the specific types corresponding to a broad type
    options = getOptions("SELECT SpecificType FROM CLOTHINGSTORE WHERE BroadType = " + filters[1], c)
    userMessage = f"What is the specific type? Please choose from these options: {options}"
    # Add the answer to our filters
    filters.append(getAnswer(userMessage, options))

    # Get all of the sizes corresponding to a broad type
    options = getOptions("SELECT Size FROM CLOTHINGSTORE WHERE BroadType = " + filters[1], c)
    userMessage = f"What is the size? Please choose from these options: {options}"
    # Add the answer to our filters
    filters.append(getAnswer(userMessage, options))

    # Get all of the brands corresponding to a broad type
    options = getOptions("SELECT Brand FROM CLOTHINGSTORE WHERE BroadType = " + filters[1], c)
    userMessage = f"What is the brand? Please choose from these options: {options}"
    # Add the answer to our filters
    filters.append(getAnswer(userMessage, options))

    # Convert to the proper type
    filters.append(int(input("What is the minimum stock?")))
    filters.append(float(input("What is the minimum price?")))
    filters.append(float(input("What is the maximum price?")))

    filters.append(input("What is the gender? M, F, or Y\t"))

    # Close connections
    conn.close()
    c.close()
    # Returned like [description, broadType, specificType, Size, Brand, Stock, minPrice, maxPrice, Gender <F, M, Y>
    return filters

def search(filters, orderNum):
    query = "SELECT * FROM CLOTHINGSTORE WHERE 1 = 1"

    # For each of the filters, make sure it exists and then add corresponding query conditions
    if filters[0] != "":
        query += f"AND Description LIKE %{filters[0]}%"
    if filters[1] != "":
        query += f"AND BroadType = {filters[1]}"
    if filters[2] != "":
        query += f"AND SpecificType = {filters[2]}"
    if filters[3] != "":
        query += f"AND Size = {filters[3]}"
    if filters[4] != "":
        query += f"AND Brand = {filters[4]}"
    if filters[5] != "":
        query += f"AND Stock > {filters[5]}"
    if filters[6] != "":
        query += f"AND Price >= {filters[6]}"
    if filters[7] != "":
        query += f"AND Price <= {filters[7]}"
    if filters[8] != "":
            if filters[8] == "M":
                query += "AND GenderM"
            elif filters[8] == "F":
                query += "AND GenderF"
            elif filters[8] == "Y":
                query += "AND GenderY"

    # Create connections and execute query
    conn = getConnection(dbName)
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()

    # Formatted string to print header
    header = f"{'Description':<30}{'Broad Type':<15}{'Specific Type':<15}{'Size':<10}{'Brand':<15}{'Stock':<10}{'Price':<10}{'Gender':<10}"
    print(header)
    print("-" * len(header) + 5)  # Print a divider line

    itemNum = 1
    for item in results:
        # Find the gender of the clothing
        if item[8] == "True":
            gender = "F"
        elif item[9] == "True":
            gender = "M"
        elif item[10] == "True":
            gender = "Y"

        # Print the info of the item formatted to match the header
        print(f"{itemNum} {item[1]:<28}{item[2]:<15}{item[3]:<15}{item[4]:<10}"
              f"{item[5]:<15}{item[6]:<10}{item[7]:<10}{gender:<10}")
        itemNum += 1

    if input("Type Y to add something to your cart.\t") == "Y":
        itemIndex = -1
        # Make sure they are adding a valid item that was printed
        while itemIndex < 0 and itemIndex > itemNum:
            itemIndex = input("Enter the number of the item you want to add:\t")

        quantity = input("How many would you like to buy?\t")
        addItem(results[itemIndex - 1][0], quantity, orderNum)

    conn.close()
    c.close()

def addItem(itemID, quantity, orderNum):
    conn = getConnection(dbName)
    c = conn.cursor()

    # Get the ID and Stock of the item being added to the cart
    c.execute(f"SELECT UniqueNum, Stock FROM CLOTHINGSTORE WHERE UniqueNum = {itemID}")
    results = c.fetchall()

    uniqueID = results[0][0]
    stock = results[0][1]

    # return if they are ordering more than what is in stock
    if quantity > stock:
        print("There is not that much in stock!")
        return

    # Add the item to holds table
    c.execute(f"INSERT INTO HOLDS (OrderNum, ClothUniID, Quantity) VALUES ({orderNum}, {uniqueID}, {quantity})")
    # Update the stock of the item that was just ordered
    c.execute(f"UPDATE CLOTHING SET Stock = {stock - quantity} WHERE UniqueNum = {uniqueID}")

    conn.close()
    c.close()

def getConnection(dbName):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    return conn

def getOptions(query, c):
    c.execute(query)
    results = c.fetchall()

    options = "\n"
    counter = 0

    # For everything in result, print it until it exceeds a character limit
    for result in results:
        counter += len(result + 5)
        if counter > 110:
            options += result + "\n"
            counter = 0
        else:
            options += result + "\t"
    return options

def getAnswer(userMessage, options):
    # default message to get into the while loop
    answer = "thismessageiscompletelyinvalidandthereisnothinglikethisinthedatabase"

    while answer not in options or answer != "skip":
        answer = input(userMessage)

    if answer == "skip":
        return ""
    return answer