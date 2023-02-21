import sqlite3
import json
import os


# data.json from https://www.py4e.com/
# https://github.com/csev/py4e/blob/master/code/roster/roster_data_sample.json

class DB:
    
    def __init__(self, db_url):
        self.db_url = db_url
        
        if os.path.exists(self.db_url):
            self.create_db()
    
    # call the database and able to enter data    
    def call_db(self, query, *args):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        try:
            res = cur.execute(query, args)
        except:
            res = cur.executescript(query) # handle multiple sql statements such as create_db() func is doing
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data
    
    # create the tables 
    def create_db(self):
        # delete the tables if they already exist *optional
        create_db_query = """
        DROP TABLE IF EXISTS Name;
        DROP TABLE IF EXISTS Course;
        DROP TABLE IF EXISTS Information;
        
        CREATE TABLE Name (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT
        );
        
        CREATE TABLE Course (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            course_name TEXT
        );
        
        CREATE TABLE Information (
            name_id INTEGER,
            course_id INTEGER,
            role INTEGER,
            PRIMARY KEY (name_id, course_id)
        )
        
        """
        self.call_db(create_db_query)
        
    # enter data from data.json file
    def data_entry(file_name: str):
        file_name = "data.json"
        
        str_data = open(file_name).read()
        json_data = json.loads(str_data)
        
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        
        for index in json_data:
            
            name = index[0]
            course_name = index[1]
            role = index[2]
            
            print((name, course_name, role))
            
            # To not enter duplicates to the database, we have INSERT OR IGNORE,
            # if there already is an entry with the same name it wont enter it twice
            cur.execute("""INSERT OR IGNORE INTO Name (name)
                VALUES ( ? )""", (name, ))
            cur.execute("SELECT id FROM Name WHERE name = ?", (name, ))
            name_id = cur.fetchone()[0]

            
            cur.execute("""INSERT OR IGNORE INTO Course (course_name)
                VALUES ( ? )""", (course_name, ))
            cur.execute("SELECT id FROM Course WHERE course_name = ?", (course_name, ))
            course_id = cur.fetchone()[0]
            
            
            cur.execute("""INSERT OR REPLACE INTO Information (name_id, course_id, role)
                VALUES ( ?, ?, ? )""", (name_id, course_id, role))
            
            conn.commit()
            




     
    
