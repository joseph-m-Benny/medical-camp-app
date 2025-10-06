from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# ✅ Connect to Render PostgreSQL
conn = psycopg2.connect(
    host="dpg-d3hhacffte5s73cuurfg-a.oregon-postgres.render.com",
    database="medical_db_xt0e",
    user="medical_db_xt0e_user",
    password="PJu7N2oRdGMaTlhmiK4Ye4o9oMpXqdQa",
    port="5432"
)
cursor = conn.cursor()

# ✅ Create patients_details table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients_details (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(20)
);
""")
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']

        cursor.execute("""
            INSERT INTO patients_details (name, age, gender, contact)
            VALUES (%s, %s, %s, %s)
        """, (name, age, gender, contact))
        conn.commit()
        return redirect(url_for('view_patients'))

    return render_template('add.html')

@app.route('/view')
def view_patients():
    cursor.execute("SELECT * FROM patients_details ORDER BY id ASC")
    patients = cursor.fetchall()
    return render_template('view.html', patients=patients)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']

        cursor.execute("""
            UPDATE patients_details
            SET name=%s, age=%s, gender=%s, contact=%s
            WHERE id=%s
        """, (name, age, gender, contact, id))
        conn.commit()
        return redirect(url_for('view_patients'))

    cursor.execute("SELECT * FROM patients_details WHERE id=%s", (id,))
    patient = cursor.fetchone()
    return render_template('update.html', patient=patient)

@app.route('/delete/<int:id>')
def delete_patient(id):
    cursor.execute("DELETE FROM patients_details WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for('view_patients'))

if __name__ == '__main__':
    app.run(debug=True)
