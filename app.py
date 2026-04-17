# ================= BACKEND (Flask - app.py) =================
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"
# Database setup
        c = conn.cursor()
        c.execute("INSERT INTO users (username,password) VALUES (?,?)", (user,pwd))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
        data = c.fetchone()
        conn.close()
        if data:
            session['user'] = user
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        train = request.form['train']
        seats = request.form['seats']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (username,train,seats) VALUES (?,?,?)", (session['user'],train,seats))
        conn.commit()
        conn.close()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings WHERE username=?", (session['user'],))
    bookings = c.fetchall()
    conn.close()
    return render_template('dashboard.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
