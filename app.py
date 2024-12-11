from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to database and retrieve attendance records
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT name, date FROM attendance ORDER BY date DESC")
    records = c.fetchall()
    conn.close()

    # Pass the records to the HTML template
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
