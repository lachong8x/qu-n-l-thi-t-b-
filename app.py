from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'devices.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        serial_number TEXT,
        location TEXT,
        start_date TEXT,
        status TEXT,
        issue_reason TEXT,
        repair_time TEXT,
        notes TEXT,
        incident_start TEXT,
        solution TEXT,
        progress TEXT,
        incident_end TEXT
    )
''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    query = request.args.get('query', '')
    filter_status = request.args.get('status', '')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    sql = "SELECT * FROM devices WHERE 1=1"
    params = []
    if query:
        sql += " AND (name LIKE ? OR serial_number LIKE ?)"
        params.extend([f'%{query}%', f'%{query}%'])
    if filter_status:
        sql += " AND status = ?"
        params.append(filter_status)
    c.execute(sql, params)
    devices = c.fetchall()
    conn.close()
    return render_template('index.html', devices=devices, query=query, status=filter_status)

@app.route('/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['serial_number'],
            request.form['location'],
            request.form['start_date'],
            request.form['status'],
            request.form.get('issue_reason', ''),
            request.form.get('repair_time', ''),
            request.form.get('notes', '')
        )
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO devices (name, serial_number, location, start_date, status, issue_reason, repair_time, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_device.html')

@app.route('/edit/<int:device_id>', methods=['GET', 'POST'])
def edit_device(device_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['serial_number'],
            request.form['location'],
            request.form['start_date'],
            request.form['status'],
            request.form.get('issue_reason', ''),
            request.form.get('repair_time', ''),
            request.form.get('notes', ''),
            device_id
        )
        c.execute('''
            UPDATE devices SET name=?, serial_number=?, location=?, start_date=?, status=?, issue_reason=?, repair_time=?, notes=?
            WHERE id=?
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/')
    c.execute("SELECT * FROM devices WHERE id=?", (device_id,))
    device = c.fetchone()
    conn.close()
    return render_template('edit_device.html', device=device)

@app.route('/delete/<int:device_id>')
def delete_device(device_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE id=?", (device_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
