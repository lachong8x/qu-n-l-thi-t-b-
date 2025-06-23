from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # Bạn có thể đổi thành chuỗi bất kỳ

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Ở đây bạn có thể kiểm tra username/password
        if username == 'admin' and password == '123456':
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return 'Sai tài khoản hoặc mật khẩu'
    return render_template('login.html')