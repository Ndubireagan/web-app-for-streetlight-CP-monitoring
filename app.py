from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_FILE = 'sensor_readings.db'

def get_readings():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT timestamp, sms_text, voltage, current, power, status FROM readings ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows



@app.route('/')
def index():
    print("Index route accessed")
    readings = get_readings()
    print("Readings fetched:", readings)
    return render_template('index.html', readings=readings)


if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    pass  # Hypercorn will run the app

