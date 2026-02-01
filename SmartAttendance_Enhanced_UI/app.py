from flask import Flask, render_template, request, redirect
import sqlite3, qrcode, io
from datetime import datetime
from flask import send_file

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    email TEXT,
                    event TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('create_event.html')

@app.route('/create', methods=['POST'])
def create():
    event = request.form['event']
    qr = qrcode.make(f"http://localhost:5000/register?event={event}")
    buf = io.BytesIO()
    qr.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/register')
def register():
    event = request.args.get('event')
    return render_template('register.html', event=event)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    event = request.form['event']
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (email, event, timestamp) VALUES (?, ?, ?)", (email, event, timestamp))
    conn.commit()
    conn.close()
    return "Attendance recorded successfully!"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    rows = c.fetchall()
    conn.close()
    return render_template('admin.html', rows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
