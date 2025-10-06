from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database setup
def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            disease TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home / Dashboard
@app.route("/")
def index():
    return render_template("index.html")

# Add patient
@app.route("/add", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        disease = request.form["disease"]

        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)", (name, age, disease))
        conn.commit()
        conn.close()
        flash("Patient added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add.html")

# Search patient
@app.route("/search", methods=["GET", "POST"])
def search_patient():
    patient = None
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        if not patient:
            flash("Patient not found!", "danger")
    return render_template("search.html", patient=patient)

# Update patient
@app.route("/update", methods=["GET", "POST"])
def update_patient():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        name = request.form.get("name")
        age = request.form.get("age")
        disease = request.form.get("disease")

        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        patient = cursor.fetchone()
        if patient:
            if name: cursor.execute("UPDATE patients SET name=? WHERE id=?", (name, patient_id))
            if age: cursor.execute("UPDATE patients SET age=? WHERE id=?", (age, patient_id))
            if disease: cursor.execute("UPDATE patients SET disease=? WHERE id=?", (disease, patient_id))
            conn.commit()
            flash("Patient updated successfully!", "success")
        else:
            flash("Patient not found!", "danger")
        conn.close()
        return redirect(url_for("index"))
    return render_template("update.html")

# Delete patient
@app.route("/delete", methods=["GET", "POST"])
def delete_patient():
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        if cursor.rowcount == 0:
            flash("Patient not found!", "danger")
        else:
            flash("Patient deleted successfully!", "success")
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("delete.html")

# View all patients
@app.route("/view")
def view_patients():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template("view.html", patients=patients)

if __name__ == "__main__":
    app.run(debug=True)
