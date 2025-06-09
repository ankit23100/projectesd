from flask import Flask, render_template, request, session, redirect, url_for
from scanner.scanner import scan_url
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        target_url = request.form['url']
        results = scan_url(target_url)
        return render_template('report.html', url=target_url, results=results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
