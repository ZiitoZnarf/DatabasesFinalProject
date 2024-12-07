import sqlite3

# Global constant for database name
DB_NAME = 'ClothingStore.db'

def connect_db():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db():
    """Creates tables and inserts initial data into the database."""
    conn = connect_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PROFILE (
        Email TEXT PRIMARY KEY NOT NULL,
        Password TEXT NOT NULL,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        CardInfo TEXT,
        BillingAddress TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CUSTOMER_ORDER (
        OrderNum TEXT PRIMARY KEY NOT NULL,
        ShipAdd TEXT NOT NULL,
        Status TEXT NOT NULL,
        ProfileEmail TEXT NOT NULL,
        FOREIGN KEY (ProfileEmail) REFERENCES PROFILE (Email)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CLOTHING (
        UniqueNum TEXT PRIMARY KEY NOT NULL,
        Description TEXT NOT NULL,
        BroadType TEXT NOT NULL,
        SpecificType TEXT NOT NULL,
        Size TEXT NOT NULL,
        Brand TEXT NOT NULL,
        Stock INTEGER NOT NULL,
        Price REAL NOT NULL,
        GenderF BOOLEAN,
        GenderM BOOLEAN,
        GenderY BOOLEAN
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HOLDS (
        OrderNum TEXT NOT NULL,
        ClothUniID TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        FOREIGN KEY (OrderNum) REFERENCES CUSTOMER_ORDER (OrderNum)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (ClothUniID) REFERENCES CLOTHING (UniqueNum)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS COLOR (
        ClothUniID TEXT NOT NULL,
        Color TEXT NOT NULL,
        FOREIGN KEY (ClothUniID) REFERENCES CLOTHING (UniqueNum)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MATERIAL (
        ClothUniID TEXT NOT NULL,
        Material TEXT NOT NULL,
        FOREIGN KEY (ClothUniID) REFERENCES CLOTHING (UniqueNum)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    ''')

    # Insert initial data
    insert_sample_data(cursor)

    conn.commit()
    conn.close()
    print("Database initialized with tables and sample data.")

def insert_sample_data(cursor):
    """Inserts initial sample data into the database."""
    cursor.executemany('''
    INSERT OR IGNORE INTO PROFILE (Email, Password, FirstName, LastName, CardInfo, BillingAddress)
    VALUES (?, ?, ?, ?, ?, ?);
    ''', [
        ('johnsmith@email.com', 'password1', 'John', 'Smith', '1234567890987654', '123 Elm Street, Las Vegas, NV'),
        ('johndoe1982@email.com', 'goodP@ssword', 'John', 'Doe', '5468154617467495', '8963 North Rutgers Street, Pittsburgh, PA'),
        ('janedoe1990@email.com', 'stayOut', 'Jane', 'Doe', '9546174173689857', '8963 North Rutgers Street, Pittsburgh, PA'),
        ('real-life-fish@email.com', 'water', 'Fish', 'Gill', '9820032489049875', '6423 Ocean Lane, Los Angeles, CA')
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO CUSTOMER_ORDER (OrderNum, ShipAdd, Status, ProfileEmail)
    VALUES (?, ?, ?, ?);
    ''', [
        ('ORDER001', '123 Elm Street, Las Vegas, NV', 'Confirmed', 'johnsmith@email.com'),
        ('ORDER002', '8963 North Rutgers Street, Pittsburgh, PA', 'Shipped', 'johndoe1982@email.com'),
        ('ORDER003', '8963 North Rutgers Street, Pittsburgh, PA', 'Delivered', 'janedoe1990@email.com'),
        ('ORDER004', '6423 Ocean Lane, Los Angeles, CA', 'Shipped', 'real-life-fish@email.com')
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO CLOTHING (UniqueNum, Description, BroadType, SpecificType, Size, Brand, Stock, Price, GenderF, GenderM, GenderY)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', [
        ('CL001', 'White Air Forces', 'Shoe', 'Mid-top', '19', 'Nike', 100, 25.00, True, False, False),
        ('CL002', 'White Air Forces', 'Shoe', 'Mid-top', '10', 'Nike', 100, 25.00, False, True, False),
        ('CL003', 'White Air Forces', 'Shoe', 'Mid-top', '11', 'Nike', 100, 25.00, False, True, False),
        ('CL004', 'Black Air Forces', 'Shoe', 'Low-top', '10.5', 'Nike', 100, 25.00, None, True, False),
        ('CL005', 'Marvin Harrison Jr. Jersey', 'Shirt', 'Jersey', 'XL', 'Nike', 19, 100.00, False, True, False),
        ('CL006', 'Marvin Harrison Jr. Jersey', 'Shirt', 'Jersey', 'M', 'Nike', 3, 100.00, False, False, True),
        ('CL007', 'LeBron Witness 8', 'Shoe', 'High-top', '11.5', 'Nike', 25, 110.00, False, True, False),
        ('CL008', 'LeBron Witness 8', 'Shoe', 'High-top', '12', 'Nike', 30, 110.00, False, True, False),
        ('CL009', 'LeBron Witness 8', 'Shoe', 'High-top', '13', 'Nike', 50, 110.00, False, True, False),
        ('CL010', 'LeBron Witness 8', 'Shoe', 'High-top', '6', 'Nike', 45, 110.00, True, False, False),
        ('CL011', 'LeBron Witness 8', 'Shoe', 'High-top', '7', 'Nike', 15, 110.00, True, False, False),
        ('CL0012', 'Campus 00s', 'Shoe', 'Low-top', '5', 'Adidas', 40, 110.00, True, False, False),
        ('CL0013', 'Campus 00s', 'Shoe', 'Low-top', '5.5', 'Adidas', 36, 110.00, True, False, False),
        ('CL0014', 'Campus 00s', 'Shoe', 'Low-top', '6', 'Adidas', 79, 110.00, True, False, False),
        ('CL0015', 'Campus 00s', 'Shoe', 'Low-top', '6.5', 'Adidas', 15, 110.00, True, False, False),
        ('CL0016', 'Campus 00s', 'Shoe', 'Low-top', '6.5', 'Adidas', 45, 110.00, True, False, False),
        ('CL0017', 'Campus 00s', 'Shoe', 'Low-top', '9', 'Adidas', 76, 110.00, False, True, False),
        ('CL0018', 'Campus 00s', 'Shoe', 'Low-top', '9.5', 'Adidas', 34, 110.00, False, True, False),
        ('CL0019', 'Campus 00s', 'Shoe', 'Low-top', '10', 'Adidas', 78, 110.00, False, True, False),
        ('CL0020', 'Campus 00s', 'Shoe', 'Low-top', '10.5', 'Adidas', 65, 110.00, False, True, False),
        ('CL0021', 'Campus 00s', 'Shoe', 'Low-top', '11', 'Adidas', 43, 110.00, False, True, False),
        ('CL0022', 'Campus 00s', 'Shoe', 'Low-top', '5', 'Adidas', 15, 110.00, False, False, True),
        ('CL0023', 'Campus 00s', 'Shoe', 'Low-top', '5.5', 'Adidas', 56, 110.00, False, False, True),
        ('CL0024', 'Campus 00s', 'Shoe', 'Low-top', '6', 'Adidas', 43, 110.00, False, False, True),
        ('CL0025', 'Campus 00s', 'Shoe', 'Low-top', '6.5', 'Adidas', 24, 110.00, False, False, True),
        ('CL0026', 'Campus 00s', 'Shoe', 'Low-top', '7', 'Adidas', 89, 110.00, False, False, True),
        ('CL0027', 'Tour Snap back', 'Accessories', 'Golf Hat', 'S', 'Adidas', 24, 32.00, False, False, True),
        ('CL0028', 'Tour Snap back', 'Accessories', 'Golf Hat', 'M', 'Adidas', 56, 32.00, False, False, True),
        ('CL0029', 'Tour Snap back', 'Accessories', 'Golf Hat', 'L', 'Adidas', 43, 32.00, False, False, True),
        ('CL0030', 'Tour Snap back', 'Accessories', 'Golf Hat', 'S', 'Adidas', 56, 32.00, False, True, False),
        ('CL0031', 'Tour Snap back', 'Accessories', 'Golf Hat', 'M', 'Adidas', 43, 32.00, False, True, False),
        ('CL0032', 'Tour Snap back', 'Accessories', 'Golf Hat', 'L', 'Adidas', 45, 32.00, False, True, False),
        ('CL0033', 'Tour Snap back', 'Accessories', 'Golf Hat', 'S', 'Adidas', 78, 32.00, True, False, False),
        ('CL0034', 'Tour Snap back', 'Accessories', 'Golf Hat', 'M', 'Adidas', 75, 32.00, True, False, False),
        ('CL0035', 'Tour Snap back', 'Accessories', 'Golf Hat', 'L', 'Adidas', 35, 32.00, True, False, False),
        ('CL0036', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'S', 'Adidas', 35, 26.00, True, False, False),
        ('CL0037', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'M', 'Adidas', 56, 26.00, True, False, False),
        ('CL0038', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'L', 'Adidas', 87, 26.00, True, False, False),
        ('CL0039', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'S', 'Adidas', 43, 26.00, False, True, False),
        ('CL0040', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'M', 'Adidas', 46, 26.00, False, True, False),
        ('CL0041', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'L', 'Adidas', 76, 26.00, False, True, False),
        ('CL0042', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'S', 'Adidas', 56, 26.00, False, False, True),
        ('CL0043', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'M', 'Adidas', 67, 26.00, False, False, True),
        ('CL0044', 'Skeleton Trucker Hat', 'Accessories', 'Trucker Hat', 'L', 'Adidas', 76, 26.00, False, False, True),
        ('CL0045', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'S', 'Independent', 35, 28.00, False, True, False),
        ('CL0046', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'M', 'Independent', 47, 28.00, False, True,False),
        ('CL0047', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'L', 'Independent', 35, 28.00, False, True,False),
        ('CL0047', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'XL', 'Independent', 35, 28.00, False, True,False),
        ('CL0048', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'S', 'Independent', 75, 28.00, True, False, False),
        ('CL0049', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'M', 'Independent', 43, 28.00, True, False,False),
        ('CL0050', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'L', 'Independent', 46, 28.00, True, False,False),
        ('CL0047', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'XL', 'Independent', 35, 28.00, True, False,False),
        ('CL0051', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'S', 'Independent', 67, 28.00, False, False, True),
        ('CL0052', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'M', 'Independent', 86, 28.00, False, False,True),
        ('CL0053', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'L', 'Independent', 32, 28.00, False, False,True),
        ('CL0047', 'Independent Spanning Chest', 'Shirt', 'Graphic Tee', 'XL', 'Independent', 35, 28.00, False, False,True),

    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO HOLDS (OrderNum, ClothUniID, Quantity)
    VALUES (?, ?, ?);
    ''', [
        ('ORDER001', 'CL001', 2),
        ('ORDER002', 'CL002', 1),
        ('ORDER003', 'CL003', 4),
        ('ORDER004', 'CL004', 3)
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO COLOR (ClothUniID, Color)
    VALUES (?, ?);
    ''', [
        ('CL001', 'White'),
        ('CL002', 'Black'),
        ('CL003', 'Red'),
        ('CL003', 'Black'),
        ('CL004', 'White'),
        ('CL004', 'Red'),
        ('CL005', 'White'),
        ('CL005', 'Orange')
    ])

    cursor.executemany('''
    INSERT OR IGNORE INTO MATERIAL (ClothUniID, Material)
    VALUES (?, ?);
    ''', [
        ('CL001', 'Rubber'),
        ('CL002', 'Leather'),
        ('CL003', 'Polyester'),
        ('CL004', 'Polyester'),
        ('CL005', 'Fabric')
    ])

def print_all_data():
    """Prints all data from all tables in the database."""
    conn = connect_db()
    cursor = conn.cursor()

    tables = ["PROFILE", "CUSTOMER_ORDER", "CLOTHING", "HOLDS", "COLOR", "MATERIAL"]

    for table in tables:
        print(f"\nContents of {table}:")
        rows = cursor.execute(f"SELECT * FROM {table};").fetchall()
        for row in rows:
            print(row)

    conn.close()

def reset_db():
    """Drops all tables in the database (useful for testing)."""
    conn = connect_db()
    cursor = conn.cursor()
    tables = ["PROFILE", "CUSTOMER_ORDER", "CLOTHING", "HOLDS", "COLOR", "MATERIAL"]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")
    conn.commit()
    conn.close()
    print("Database reset complete.")

if __name__ == "__main__":
    initialize_db()
    print_all_data()
