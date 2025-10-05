from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# ✅ Database connection
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=TURBO\DS_SQL;'  # Change this to your SQL Server name
    'DATABASE=medical;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# 🏠 Home Page
@app.route('/')
def index():
    return render_template('index.html')

# ➕ Add Patient
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        cursor.execute("EXEC AddPatient ?, ?, ?, ?", (name, age, gender, contact))
        conn.commit()
        return redirect(url_for('view_all'))
    return render_template('add.html')

# 👁️ View All Patients
@app.route('/view')
def view_all():
    cursor.execute("EXEC GetAllPatients")
    patients = cursor.fetchall()
    return render_template('view.html', patients=patients)

# 🔍 Search and Update Patient
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        pid = request.form['id']
        cursor.execute("SELECT * FROM patients WHERE id=?", pid)
        patient = cursor.fetchone()
        if patient:
            return render_template('update.html', patient=patient)
        else:
            return "❌ Patient not found"
    return render_template('search.html')

# ✏️ Update Patient
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contact = request.form['contact']
    cursor.execute("EXEC UpdatePatient ?, ?, ?, ?, ?", (id, name, age, gender, contact))
    conn.commit()
    return redirect(url_for('view_all'))

# ❌ Delete Patient
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        pid = request.form['id']
        cursor.execute("EXEC DeletePatient ?", pid)
        conn.commit()
        return redirect(url_for('view_all'))
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
