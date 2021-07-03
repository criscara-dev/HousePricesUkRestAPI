import sqlite3, csv

# 1. create the 'empty' DB table
connection = sqlite3.connect("./houseprices.db")
# connection = sqlite3.connect("./houseprices2.sqlite")
cursor = connection.cursor()

sql = """
 CREATE TABLE HousePrices (
    Id INTEGER PRIMARY KEY,
    Code VARCHAR(30),
    price FLOAT,
    date STRING(30),
    postcode VARCHAR(30),
    propType VARCHAR(30),
    newBuild BOOLEAN(30),
    estateType VARCHAR(30),
    number INTEGER,
    street VARCHAR(30),
    town VARCHAR(30),
    district VARCHAR(30),
    county VARCHAR(30)
    )
"""

cursor.execute(sql)
print('HousePrices has been created.')

connection.commit()

#########  importing_from_csv file  #########
# 3. inserting csv dat into SQLAlchemy DB
with open('./data/ready_data.csv','r') as csv_file:
    no_records = 0
    for row in csv_file:
          cursor.execute("INSERT INTO HousePrices VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(","))
          connection.commit()
          no_records += 1
connection.close()
print(f'\n {no_records} Records transferred')