import sqlite3

#create database connection
db = sqlite3.connect('data.db')

def init_db():
    #executes schema.sql
    with open('schema.sql') as f:
        db.executescript(f.read())

    db.execute("INSERT INTO device (id, lat, long) VALUES (?, ?, ?)",
               ['WS01', 123.123, 23.123]
               )

    db.execute("INSERT INTO device (id, lat, long) VALUES (?, ?, ?)",
               ['WS21', 123.123, 23.123]
               )

    db.commit()
    db.close()
