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
        cur.execute("CREATE TABLE Cars (Id INT, Name TEXT, Price INT)")
        cur.execute("INSERT INTO Cars VALUES(1, 'Audi', 52642)")
        cur.execute("INSERT INTO Cars VALUES(2, 'Mercedes', 57127)")
        cur.execute("INSERT INTO Cars VALUES(3, 'Skoda', 9000)")
        cur.execute("INSERT INTO Cars VALUES(4, 'Volvo', 29000)")
        cur.execute("INSERT INTO Cars VALUES(5, 'Bentley', 350000)")
        cur.execute("INSERT INTO Cars VALUES(6, 'Citroen', 21000)")
        cur.execute("INSERT INTO Cars VALUES(7, 'Hummer', 41400)")
        cur.execute("INSERT INTO Cars VALUES(8, 'Volkswagen', 21600)")


if __name__ == "__main__":
    main()
    CreateCarsTable()
