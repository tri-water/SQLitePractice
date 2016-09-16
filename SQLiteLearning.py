import sqlite3 as lite
import sys

def main():

    con = None
    
    try:
        con = lite.connect('test.db')
        
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        
        data = cur.fetchone()

        print ("SQLite version:", *data)

    except lite.Error as e:
        
        print ("Error:" *e.args[0])
        sys.exit(1)
    
    finally:
        
        if con:
            con.close()

def CreateCarsTable():
    
    con = lite.connect('test.db')
    
    with con:
        
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Cars")
        cur.execute("CREATE TABLE Cars (Id INT, Name TEXT, Price INT)")
        cur.execute("INSERT INTO Cars VALUES(1, 'Audi', 52642)")
        cur.execute("INSERT INTO Cars VALUES(2, 'Mercedes', 57127)")
        cur.execute("INSERT INTO Cars VALUES(3, 'Skoda', 9000)")
        cur.execute("INSERT INTO Cars VALUES(4, 'Volvo', 29000)")
        cur.execute("INSERT INTO Cars VALUES(5, 'Bentley', 350000)")
        cur.execute("INSERT INTO Cars VALUES(6, 'Citroen', 21000)")
        cur.execute("INSERT INTO Cars VALUES(7, 'Hummer', 41400)")
        cur.execute("INSERT INTO Cars VALUES(8, 'Volkswagen', 21600)")

        cur.execute("SELECT * FROM Cars")
        for car in cur:
            print(*car)

def CreateCarsTable2():
    cars = ((1, 'Audi', 52642),
            (2, 'Mercedes', 57127),
            (3, 'Skoda', 9000),
            (4, 'Volvo', 29000),
            (5, 'Bentley', 350000),
            (6, 'Hummer', 41400),
            (7, 'Volkswagen', 21600))

    con = lite.connect('test.db')

    with con:
        
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Cars")
        cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)

def CreateCarsTable3():

    try:
        con = lite.connect('test.db')

        cur = con.cursor()

        cur.executescript("""
            DROP TABLE IF EXISTS Cars;
            CREATE TABLE Cars(Id INT, Name TEXT, Price INT);
            INSERT INTO Cars VALUES(1,'Audi',52642);
            INSERT INTO Cars VALUES(2,'Mercedes',57127);
            INSERT INTO Cars VALUES(3,'Skoda',9000);
            INSERT INTO Cars VALUES(4,'Volvo',29000);
            INSERT INTO Cars VALUES(5,'Bentley',350000);
            INSERT INTO Cars VALUES(6,'Citroen',21000);
            INSERT INTO Cars VALUES(7,'Hummer',41400);
            INSERT INTO Cars VALUES(8,'Volkswagen',21600);
        """)
        
        con.commit()
    
    except lite.Error as e:
        
        if con:
            con.rollback()

        print("Error:", *e.args[0])
        sys.exit(1)

    finally:
        
        if con:
            con.close()

def LastRowId():
    
    con = lite.connect(':memory:')
    
    with con:
        
        cur = con.cursor()
        cur.execute("CREATE TABLE Friends(Id INTEGER PRIMARY KEY, Name TEXT)")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Tom')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Jim')")
        cur.execute("INSERT INTO Friends(Name) VALUES ('Robert')")

        lid = cur.lastrowid
        print('The last Id of the inserted row is:', lid)

def RetrieveAllData():
    
    con = lite.connect('test.db')

    with con:
        
        cur = con.cursor()
        cur.execute("SELECT * FROM Cars")
        
        rows = cur.fetchall()
        
        for row in rows:
            print(*row)

def RetrieveOneData():
        
    con = lite.connect('test.db')
        
    with con:
        
        cur = con.cursor()
        cur.execute("SELECT * FROM Cars")

        while True:
            
            row = cur.fetchone()
            
            if row == None:
                break
            
            print(*row)

def DictCursor():
       
    con = lite.connect('test.db')
    
    with con:
        
        con.row_factory = lite.Row
        
        cur = con.cursor()
        cur.execute("SELECT * FROM Cars")
        
        rows = cur.fetchall()

        for row in rows:
            print(row['Id'], row['Name'], row['Price'])

if __name__ == "__main__":
    
    DictCursor()