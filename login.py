from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    banned = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        banned_user = conn.execute('SELECT * FROM banned_user WHERE username = ?', (username,)).fetchone()
        if banned_user:
            flash('Username is banned.', 'danger')
            banned = True

        user = conn.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if ((user or (username == 'Admin' and password == 'pass')) and not banned):
            session['loggedin'] = True
            session['username'] = username

            if username == 'Admin':
                session['admin_login'] = True
                return redirect('/admin')
            else:
                return redirect('/stream')
        else:
            error = True
            flash('Incorrect Username or Password', 'danger')

    return render_template('login.html', error=error)

@app.route('/admin')
def admin_panel():
    if session.get('admin_login'):
        return "<h1>Welcome Admin</h1>"
    return redirect('/login')

@app.route('/stream')
def stream_page():
    if session.get('loggedin'):
        return "<h1>Welcome to Stream Page</h1>"
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
