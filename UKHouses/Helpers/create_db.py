import sqlite3

# 1. create the 'empty' DB table
connection = sqlite3.connect("../houseprices.db")
cursor = connection.cursor()

sql = """
 CREATE TABLE HousePrices (
    Id INTEGER PRIMARY KEY,
    Code VARCHAR(32),
    price FLOAT,
    date DATETIME,
    postcode VARCHAR(16),
    propType VARCHAR(16),
    newBuild BOOLEAN,
    estateType VARCHAR(16),
    number INTEGER,
    street VARCHAR(32),
    town VARCHAR(16),
    district VARCHAR(16),
    county VARCHAR(16)
    )
"""

cursor.execute(sql)
print("HousePrices has been created.")

connection.commit()

#########  importing_from_csv file  #########
# 3. inserting csv dat into SQLAlchemy DB
with open("../csv_data/complete.csv", "r") as csv_file:
    no_records = 0
    for row in csv_file:
        cursor.execute(
            "INSERT INTO HousePrices VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(",")
        )
        connection.commit()
        no_records += 1
connection.close()
print(f"\n {no_records} Records transferred")
