import sqlite3

def getFilters(dbName):
    filters = []
    conn = getConnection(dbName)
    c = conn.cursor()

    print("For all of the following options, type 'skip' to skip")
    print("Please keep in mind that filters are case sensitive")

    description = input("What is the name of the item?\t")
    if description == "skip" or description == "":
        filters.append("")
    else:
        filters.append(description)

    options = getOptions("SELECT BroadType FROM CLOTHING", c)
    userMessage = f"What is the broad type? Please choose from these options: {printOptions(options)}"
    filters.append(getAnswer(userMessage, options))

    if (filters[1] != ""):
        # Get all of the specific types corresponding to a broad type
        options = getOptions("SELECT SpecificType FROM CLOTHING WHERE BroadType = '" + filters[1] + "'", c)
        userMessage = f"What is the specific type? Please choose from these options: {printOptions(options)}"
        # Add the answer to our filters
        filters.append(getAnswer(userMessage, options))

        # Get all of the sizes corresponding to a broad type
        options = getOptions("SELECT Size FROM CLOTHING WHERE BroadType = '" + filters[1] + "'", c)
        userMessage = f"What is the size? Please choose from these options: {printOptions(options)}"
        # Add the answer to our filters
        filters.append(getAnswer(userMessage, options))

        # Get all of the brands corresponding to a broad type
        options = getOptions("SELECT Brand FROM CLOTHING WHERE BroadType = '" + filters[1] + "'", c)
        userMessage = f"What is the brand? Please choose from these options: {printOptions(options)}"
        # Add the answer to our filters
        filters.append(getAnswer(userMessage, options))
    else:
        specificType = input("What is the specific type? (E.g Jersey, Low-top, etc.)\t")
        if specificType == "skip":
            filters.append("")
        else:
            filters.append(specificType)

        size = input("What is the size?\t")
        if size == "skip":
            filters.append("")
        else:
            filters.append(size)

        brand = input("What is the brand?  (E.g Nike, Adidas, etc.)\t")
        if brand == "skip":
            filters.append("")
        else:
            filters.append(brand)



    minStock = input("What is the minimum stock?\t")
    if minStock == "skip" or minStock == "":
        filters.append("")
    else:
        filters.append(int(minStock))

    minPrice = input("What is the minimum price?\t")
    if minPrice == "skip" or minPrice == "":
        filters.append("")
    else:
        filters.append(float(minPrice))

    maxPrice = input("What is the maximum price?\t")
    if maxPrice == "skip" or maxPrice == "":
        filters.append("")
    else:
        filters.append(float(maxPrice))

    userMessage = "What is the gender? M, F, or Y\t"
    filters.append(getAnswer(userMessage, ["M", "F", "Y"]))

    # Close connections
    c.close()
    conn.close()
    # Returned like [description, broadType, specificType, Size, Brand, Stock, minPrice, maxPrice, Gender <F, M, Y>
    return filters

def search(filters, orderNum, dbName, employee):
    query = "SELECT * FROM CLOTHING WHERE 1 = 1"

    params = []
    if filters[0] != "":
        query += " AND Description LIKE ?"
        params.append(f"%{filters[0]}%")
    if filters[1] != "":
        query += " AND BroadType = ?"
        params.append(filters[1])
    if filters[2] != "":
        query += " AND SpecificType = ?"
        params.append(filters[2])
    if filters[3] != "":
        query += " AND Size = ?"
        params.append(filters[3])
    if filters[4] != "":
        query += " AND Brand = ?"
        params.append(filters[4])
    if filters[5] != "":
        query += " AND Stock >= ?"
        params.append(filters[5])
    if filters[6] != "":
        query += " AND Price >= ?"
        params.append(filters[6])
    if filters[7] != "":
        query += " AND Price <= ?"
        params.append(filters[7])
    if filters[8] != "":
        if filters[8] == "M":
            query += " AND GenderM = 1"
        elif filters[8] == "F":
            query += " AND GenderF = 1"
        elif filters[8] == "Y":
            query += " AND GenderY = 1"

    # Create connections and execute query
    conn = getConnection(dbName)
    c = conn.cursor()
    c.execute(query, params)
    results = c.fetchall()

    # Formatted string to print header
    header = f"{'Description':<30}{'Broad Type':<15}{'Specific Type':<15}{'Size':<10}{'Brand':<15}{'Stock':<10}{'Price':<10}{'Gender':<10}"
    print(header)
    print("-" * (len(header) + 5))  # Print a divider line

    itemNum = 1
    for item in results:
        # Find the gender of the clothing
        gender = "M" if item[9] else "F" if item[8] else "Y" if item[10] else "Unknown"

        # Print the info of the item formatted to match the header
        print(f"{itemNum} {item[1]:<28}{item[2]:<15}{item[3]:<15}{item[4]:<10}"
              f"{item[5]:<15}{item[6]:<10}{item[7]:<10}{gender:<10}")
        itemNum += 1

    if not employee:
        if input("Type Y to add something to your cart.\t").upper().strip() == "Y":
            itemIndex = -1
            # Make sure they are adding a valid item that was printed
            while itemIndex < 0 or itemIndex > itemNum:
                itemIndex = int(input("Enter the number of the item you want to add:\t"))

            quantity = int(input("How many would you like to buy?\t"))
            addItem(results[itemIndex - 1][0], quantity, orderNum, dbName)

    c.close()
    conn.close()

def addItem(itemID, quantity, orderNum, dbName):
    conn = getConnection(dbName)
    c = conn.cursor()

    # Get the ID and Stock of the item being added to the cart
    c.execute("SELECT UniqueNum, Stock FROM CLOTHING WHERE UniqueNum = ?", [itemID])
    results = c.fetchall()

    uniqueID = results[0][0]
    stock = results[0][1]

    # return if they are ordering more than what is in stock
    if quantity > stock:
        print("There is not that much in stock!")
        return

    # Add the item to holds table
    c.execute("INSERT INTO HOLDS (OrderNum, ClothUniID, Quantity) VALUES (?, ?, ?)", [orderNum, uniqueID, quantity])
    conn.commit()
    # Update the stock of the item that was just ordered
    c.execute("UPDATE CLOTHING SET Stock = ? WHERE UniqueNum = ?", [stock - quantity, uniqueID])
    conn.commit()

    c.close()
    conn.close()

def getConnection(dbName):
    conn = sqlite3.connect(dbName)
    conn.row_factory = sqlite3.Row
    return conn

def getOptions(query, c):
    c.execute(query)
    results = c.fetchall()

    options = []
    counter = 0

    # For everything in result, print it until it exceeds a character limit
    for result in results:
        option = result[0]
        if option not in options:
            options.append(option)

    return options

def printOptions(options):

    optionsString = "\n"
    for option in options:
        optionsString += option + "\n"

    return optionsString

def getAnswer(userMessage, options):
    # default message to get into the while loop
    answer = "thismessageiscompletelyinvalidandthereisnothinglikethisinthedatabase"

    while answer not in options and answer != "skip":
        answer = input(userMessage)

    if answer == "skip":
        return ""
    return answer
