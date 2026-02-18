from flask import Flask, render_template, request, redirect, abort
import sqlite3
import shortuuid
from datetime import datetime

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    # Table for URLs
    c.execute('''CREATE TABLE IF NOT EXISTS urls 
                 (id INTEGER PRIMARY KEY, original_url TEXT, short_code TEXT UNIQUE, created_at TEXT)''')
    # Table for Analytics (Clicks)
    c.execute('''CREATE TABLE IF NOT EXISTS clicks 
                 (id INTEGER PRIMARY KEY, short_code TEXT, click_time TEXT, user_agent TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        # Generate a short 5-char code
        short_code = shortuuid.ShortUUID().random(length=5)
        
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute("INSERT INTO urls (original_url, short_code, created_at) VALUES (?, ?, ?)",
                  (original_url, short_code, datetime.now()))
        conn.commit()
        conn.close()
        
        return render_template('index.html', short_url=f"{request.host_url}{short_code}")
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    result = c.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,)).fetchone()
    
    if result:
        # Log the click for analytics
        c.execute("INSERT INTO clicks (short_code, click_time, user_agent) VALUES (?, ?, ?)",
                  (short_code, datetime.now(), request.headers.get('User-Agent')))
        conn.commit()
        conn.close()
        return redirect(result[0])
    else:
        conn.close()
        return abort(404)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get all links and count their clicks
    stats = c.execute('''
        SELECT u.original_url, u.short_code, u.created_at, COUNT(c.id) as clicks 
        FROM urls u 
        LEFT JOIN clicks c ON u.short_code = c.short_code 
        GROUP BY u.id
    ''').fetchall()
    
    conn.close()
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)