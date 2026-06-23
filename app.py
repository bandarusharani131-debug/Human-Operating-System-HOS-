from flask import Flask, render_template, request
import joblib
import sqlite3
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Load Models
heart_model = joblib.load("models/heart_model.pkl")
diabetes_model = joblib.load("models/diabetes_model.pkl")

# Create reports folder automatically
os.makedirs("reports", exist_ok=True)


def generate_pdf(name, age, heart_risk, diabetes_risk, health_score):

    pdf = canvas.Canvas(f"reports/{name}_report.pdf")

    pdf.drawString(100, 800, "Human Operating System (HOS) Report")
    pdf.drawString(100, 770, f"Patient Name: {name}")
    pdf.drawString(100, 750, f"Age: {age}")
    pdf.drawString(100, 730, f"Heart Disease Risk: {heart_risk}")
    pdf.drawString(100, 710, f"Diabetes Risk: {diabetes_risk}")
    pdf.drawString(100, 690, f"Health Score: {health_score}%")

    pdf.save()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    name = request.form['name']
    age = int(request.form['age'])

    # Heart Inputs
    sex = int(request.form['sex'])
    cp = int(request.form['cp'])
    trestbps = int(request.form['trestbps'])
    chol = int(request.form['chol'])
    fbs = int(request.form['fbs'])
    restecg = int(request.form['restecg'])
    thalach = int(request.form['thalach'])
    exang = int(request.form['exang'])
    oldpeak = float(request.form['oldpeak'])
    slope = int(request.form['slope'])
    ca = int(request.form['ca'])
    thal = int(request.form['thal'])

    heart_input = [[
        age, sex, cp, trestbps, chol,
        fbs, restecg, thalach,
        exang, oldpeak, slope, ca, thal
    ]]

    heart_prediction = heart_model.predict(heart_input)[0]

    heart_risk = "HIGH" if heart_prediction == 1 else "LOW"

    # Diabetes Inputs
    pregnancies = int(request.form['pregnancies'])
    glucose = int(request.form['glucose'])
    bloodpressure = int(request.form['bloodpressure'])
    skinthickness = int(request.form['skinthickness'])
    insulin = int(request.form['insulin'])
    bmi = float(request.form['bmi'])
    dpf = float(request.form['dpf'])

    diabetes_input = [[
        pregnancies,
        glucose,
        bloodpressure,
        skinthickness,
        insulin,
        bmi,
        dpf,
        age
    ]]

    diabetes_prediction = diabetes_model.predict(diabetes_input)[0]

    diabetes_risk = "HIGH" if diabetes_prediction == 1 else "LOW"

    # Health Score
    health_score = 100

    if heart_prediction == 1:
        health_score -= 20

    if diabetes_prediction == 1:
        health_score -= 20

    future_heart = min(100, health_score + 15)
    future_diabetes = min(100, health_score + 10)

    recommendations = []

    if heart_prediction == 1:
        recommendations.append(
            "Reduce cholesterol and monitor blood pressure"
        )

    if diabetes_prediction == 1:
        recommendations.append(
            "Reduce sugar intake and monitor glucose levels"
        )

    recommendations.append("Exercise 30 minutes daily")
    recommendations.append("Maintain healthy diet")
    recommendations.append("Schedule regular medical checkups")

    # Save to Database
    conn = sqlite3.connect("hos.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients
    (name, age, heart_risk, diabetes_risk, health_score)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        name,
        age,
        heart_risk,
        diabetes_risk,
        health_score
    ))

    conn.commit()
    conn.close()

    # Generate PDF
    generate_pdf(
        name,
        age,
        heart_risk,
        diabetes_risk,
        health_score
    )

    return render_template(
        'index.html',
        name=name,
        age=age,
        heart_risk=heart_risk,
        diabetes_risk=diabetes_risk,
        health_score=health_score,
        future_heart=future_heart,
        future_diabetes=future_diabetes,
        recommendations=recommendations
    )


@app.route('/history')
def history():

    conn = sqlite3.connect("hos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        rows=rows
    )


if __name__ == "__main__":
    app.run(debug=True)