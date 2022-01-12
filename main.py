import flask
from flask import request, jsonify, render_template, redirect, url_for, flash
import sqlite3
from init_db import init_db
#from ping import ping_id, ping_type, ping_all

app = flask.Flask(__name__)
app.config["DEBUG"] = True
init_db()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = sqlite3.connect('data.db')
    db.row_factory = dict_factory
    return db

@app.route('/', methods=['GET'])
def home():
    return render_template('./templates/ground-home.html')


# https://stackoverflow.com/questions/34715593/rows-returned-by-pyodbc-are-not-json-serializable

@app.route('/device', methods=['GET', 'POST', 'DELETE'])
def get_device():
    db = get_db()
    params = request.args
    if request.method == 'GET':
        id = params.get('id')
        type = params.get('type')

        #add wildcard after type
        type += "%"

        if id:
            results = db.execute("SELECT * FROM device WHERE id=?;", [id]).fetchall()
        elif type:
            results = db.execute("SELECT * FROM device WHERE id LIKE ?;", [type]).fetchall()
        
        db.close()
        return jsonify(results)
    
    if request.method == 'POST':
        id = request.json['id']
        lat = request.json['lat']
        long = request.json['long']

        db.execute("INSERT INTO device ('id', 'lat', 'long') VALUES (?, ?, ?);", [id, lat, long])

        db.commit()
        db.close()
        return "Successfully added " + id + " to devices.\n"

    if request.method == 'DELETE':
        id = request.json['id']

        db.execute("DELETE FROM device WHERE id=?", [id])

        db.commit()
        db.close()
        return "Successfully deleted " + id + " from devices.\n"

@app.route('/alldevice', methods=['GET'])
def get_all_devices():
    db = get_db()
    posts = db.execute('SELECT * FROM device').fetchall()
    db.close()
    return jsonify(posts)

@app.route('/data', methods=['GET', 'POST'])
def get_device_data():
    db = get_db()

    if request.method == 'GET':
        params = request.args
        id = params.get('id')
        date_start = params.get('datei')
        date_end = params.get('datef')
        time_start = params.get('timei')
        time_end = params.get('timef')

        #create query
        query = "SELECT * FROM"
        filter = []

        #identify device type
        if id[:2] == "WS":
            query += " ws"
        elif id[:2] == "B":
            query += " hab"

        query += " WHERE"

        #check for parameters and add them to query
        if id:
            query += " device_id=? AND"
            filter.append(id)
        if date_start:
            query += " date BETWEEN ? AND"
            filter.append(date_start)

            if date_end:
                query += " ? AND"
                filter.append(date_end)
            else:
                query += " ? AND"
                filter.append(date_start)
        
        if time_start:
            query += " time BETWEEN ? AND"
            filter.append(time_start)

            if time_end:
                query += " ? AND"
                filter.append(time_end)
            else:
                query += " 23:59:00 AND"
                filter.append("23:59:00")
            
        if not id:
            return page_not_found(404)

        #remove AND, then add ; to query
        query = query[:-4] + ";"

        #execute query in database and return results
        results = db.execute(query, filter).fetchall()
        return jsonify(results)

    if request.method == 'POST':
        id = request.json['id']
        date = request.json['date']
        time = request.json['time']

        query = "INSERT INTO"
        filter = [id, time, date]

        #identify type of device
        if id[:2] == "WS":
            filter.append(request.json['temp'])
            filter.append(request.json['hum'])

            query += " ws ('device_id', 'time', 'date', 'temperature', 'humidity') VALUES (?, ?, ?, ?, ?);"
        elif id[:2] == "B":
            filter.append(request.json['temp'])
            filter.append(request.json['hum'])
            filter.append(request.json['alt'])
            
            query += " ws ('device_id', 'time', 'date', 'temperature', 'humidity', 'altitude') VALUES (?, ?, ?, ?, ?, ?);"

        db.execute(query, filter).fetchall()
        db.commit()
        db.close()
        return "Data received from " + id + "\n"

@app.errorhandler(404)
def page_not_found(e):
    return "Page Not Found", 404

app.run()

