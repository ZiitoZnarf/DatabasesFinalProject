import sqlite3

# Global constant for database name
DB_NAME = 'ClothingStore.db'

def connect_db(DB_NAME):
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
        ('johnsmith@email.com', 'password1', 'John', 'Smith', '1234-5678-9098-7654', '123 Elm Street, Las Vegas, NV'),
        ('johndoe1982@email.com', 'goodP@ssword', 'John', 'Doe', '5468-1546-1746-7495', '8963 North Rutgers Street, Pittsburgh, PA'),
        ('janedoe1990@email.com', 'stayOut', 'Jane', 'Doe', '9546-1741-7368-9857', '8963 North Rutgers Street, Pittsburgh, PA'),
        ('real-life-fish@email.com', 'water', 'Fish', 'Gill', '9820-0324-8904-9875', '6423 Ocean Lane, Los Angeles, CA')
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
        ('CL002', 'Black Air Forces', 'Shoe', 'Low-top', '10.5', 'Nike', 100, 25.00, None, True, False),
        ('CL003', 'Marvin Harrison Jr. Jersey', 'Shirt', 'Jersey', 'XL', 'Nike', 0, 100.00, False, True, False),
        ('CL004', 'Marvin Harrison Jr. Jersey', 'Shirt', 'Jersey', 'M', 'Nike', 0, 100.00, False, False, True),
        ('CL005', 'LeBron Witness 8', 'Shoe', 'High-top', '11.5', 'Nike', 25, 110.00, False, True, False)
    ])

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
