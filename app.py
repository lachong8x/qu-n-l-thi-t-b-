# Flask app entry
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', user=session['user'], role=session['role'])
    return redirect(url_for('login'))
