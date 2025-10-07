from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize the database (SQLite for simplicity)
def init_db():
    conn = sqlite3.connect('patients.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            disease TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add patient
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']
        disease = request.form['disease']

        conn = sqlite3.connect('patients.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO patients (name, age, phone, address, disease) VALUES (?, ?, ?, ?, ?)",
                    (name, age, phone, address, disease))
        conn.commit()

        patient_id = cur.lastrowid
        conn.close()

        return render_template('add.html', success=True, patient_id=patient_id, name=name, age=age, phone=phone, address=address, disease=disease)
    return render_template('add.html')

# Search patient
@app.route('/search', methods=['GET', 'POST'])
def search():
    patient = None
    searched = False
    if request.method == 'POST':
        name = request.form['name']
        conn = sqlite3.connect('patients.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients WHERE name = ?", (name,))
        patient = cur.fetchone()
        conn.close()
        searched = True
    return render_template('search.html', patient=patient, searched=searched)

# Update patient
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        pid = request.form['id']
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        address = request.form['address']
        disease = request.form['disease']

        conn = sqlite3.connect('patients.db')
        cur = conn.cursor()
        cur.execute("""
            UPDATE patients SET name=?, age=?, phone=?, address=?, disease=? WHERE id=?
        """, (name, age, phone, address, disease, pid))
        conn.commit()
        conn.close()
        return render_template('update.html', success=True)
    return render_template('update.html')

# Delete patient
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        pid = request.form['id']
        conn = sqlite3.connect('patients.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        return render_template('delete.html', success=True)
    return render_template('delete.html')

# View all patients
@app.route('/view')
def view():
    conn = sqlite3.connect('patients.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    conn.close()
    return render_template('view.html', patients=patients)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
