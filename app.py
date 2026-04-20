from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bugs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bugs
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 description TEXT NOT NULL,
                 priority TEXT NOT NULL,
                 status TEXT DEFAULT 'Open',
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('bugs.db')
    c = conn.cursor()
    total = c.execute('SELECT COUNT(*) FROM bugs').fetchone()[0]
    open_bugs = c.execute('SELECT COUNT(*) FROM bugs WHERE status="Open"').fetchone()[0]
    fixed = c.execute('SELECT COUNT(*) FROM bugs WHERE status="Fixed"').fetchone()[0]
    conn.close()
    return render_template('index.html', total=total, open_bugs=open_bugs, fixed=fixed)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        conn = sqlite3.connect('bugs.db')
        c = conn.cursor()
        c.execute('INSERT INTO bugs (title, description, priority) VALUES (?, ?, ?)',
                  (title, description, priority))
        conn.commit()
        conn.close()
        return redirect(url_for('bugs'))
    return render_template('report.html')

@app.route('/bugs')
def bugs():
    conn = sqlite3.connect('bugs.db')
    c = conn.cursor()
    all_bugs = c.execute('SELECT * FROM bugs ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('bugs.html', bugs=all_bugs)

@app.route('/update/<int:bug_id>', methods=['POST'])
def update_bug(bug_id):
    status = request.form['status']
    conn = sqlite3.connect('bugs.db')
    c = conn.cursor()
    c.execute('UPDATE bugs SET status = ? WHERE id = ?', (status, bug_id))
    conn.commit()
    conn.close()
    return redirect(url_for('bugs'))

@app.route('/delete/<int:bug_id>', methods=['POST'])
def delete_bug(bug_id):
    conn = sqlite3.connect('bugs.db')
    c = conn.cursor()
    c.execute('DELETE FROM bugs WHERE id = ?', (bug_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('bugs'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)