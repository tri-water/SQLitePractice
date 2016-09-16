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

def ParaQuery():
    
    uId = 1
    uPrice = 62300

    con = lite.connect('test.db')
    
    with con:
        
        cur = con.cursor()
        
        cur.execute("UPDATE Cars SET Price = ? WHERE Id = ?", (uPrice, uId))
        con.commit()

        print("Number of rows updated:", cur.rowcount)
        
        uId = 4
        cur.execute("SELECT Name, Price FROM Cars WHERE Id = :Id", {"Id": uId})
        row = cur.fetchone()
        print(*row)


def readImage():
       
    try:
        fin = open("woman.jpg", "rb")
        img = fin.read()
        return img
    
    except IOError as e:
        
        print("Error", e.args[0], e.args[1])
        sys.exit(1)

    finally:
        
        if fin:
            fin.close()


def SaveImageInDB():
    
    try:
        con = lite.connect('test.db')
        
        cur = con.cursor()
        data = readImage()
        binary = lite.Binary(data)
        cur.execute("CREATE TABLE Images(Id INTEGER PRIMARY KEY, Data BLOB)")
        cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,))

        con.commit()

    except lite.Error as e:
        
        if con:
            con.rollback()

        print("Error:", e.args[0])

    finally:
    
        if con:
            con.close()

def writeImage(data):
    
    try:
        fout = open('woman2.jpg', 'wb')
        fout.write(data)

    except IOError as e:
        print("Error: ", e.args[0], e.args[1])
        sys.exit(1)

    finally:
        
        if fout:
            fout.close()

def readImageFromDB():

    try:
        con = lite.connect('test.db')
        
        cur = con.cursor()
        cur.execute("SELECT Data FROM Images LIMIT 1")
        data = cur.fetchone()[0]

        writeImage(data)

    except lite.Error as e:
    
        print("Error:", e.args[0])
        sys.exit(1)

def DBinfo():

    con = lite.connect('test.db')
    
    with con:

        cur = con.cursor()
         
        # Table Information
        cur.execute("PRAGMA table_info(Cars)")

        data = cur.fetchall()
    
        for d in data:
            print("%s %-5s %s" % (d[0], d[1], d[2]))

        # row information
        cur.execute("SELECT * FROM Cars")
        
        col_names = [cn[0] for cn in cur.description]

        rows = cur.fetchall()
        
        print("%s %-10s %s" %( col_names[0], col_names[1], col_names[2]))

        for row in rows:
            print("%2s %-10s %s" % row)

        # all tables in DB
        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        rows = cur.fetchall()
        for row in rows:
            print(row[0])

if __name__ == "__main__":
    
    DBinfo()