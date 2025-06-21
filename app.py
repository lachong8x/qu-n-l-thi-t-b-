from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # Bạn có thể đổi thành chuỗi bất kỳ

@app.route('/')
def home():
    if 'user' in session:
        return f"Chào mừng {{session['user']}}!"
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra thông tin người dùng từ database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return 'Sai tài khoản hoặc mật khẩu'

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)