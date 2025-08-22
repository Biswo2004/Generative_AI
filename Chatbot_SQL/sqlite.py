import sqlite3

## connect to sqlite
connection = sqlite3.connect('student.db')
## Create a cursor object to insert record,create table
cursor = connection.cursor()

##create table
table_info = """
create table if not exists STUDENTS(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INTEGER
)
"""
cursor.execute(table_info)

##Insert some more records
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Biswojit', 'GEN AI', '23412H1', 85)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Vivek', 'GEN AI', '23412H1', 90)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Rakesh', 'CLOUD COMPUTING', '23412H1', 95)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Anuran', 'JAVA DEVELOPER', '23412H1', 80)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Satya', 'GEN AI', '23412H1', 80)")

## Display all the records 
print("The inserted records are")
data = cursor.execute("SELECT * FROM STUDENTS").fetchall()
for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()