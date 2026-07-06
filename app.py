from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import joblib
import database
app = Flask(__name__)
app.secret_key = "smartlender_secret_key"

# ==========================
# Load Model
# ==========================

model = joblib.load("model/loan_model.pkl")
scaler = joblib.load("model/scaler.pkl")
def get_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# ==========================
# Login
# ==========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_connection()

        try:

            conn.execute(
                """
                INSERT INTO users
                (fullname,email,username,password)
                VALUES (?,?,?,?)
                """,
                (
                    fullname,
                    email,
                    username,
                    password
                )
            )

            conn.commit()

            conn.close()

            return redirect(url_for("login"))

        except:

            conn.close()

            return render_template(
                "register.html",
                error="Username or Email already exists."
            )

    return render_template("register.html")
# ==========================
# Dashboard
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ==========================
# Analytics
# ==========================

@app.route("/analytics")
def analytics():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("analytics.html")


# ==========================
# AI Model
# ==========================

@app.route("/model")
def model_info():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "model.html",
        accuracy="82.93%",
        model_name="XGBoost",
        algorithms=4,
        records=614
    )


# ==========================
# Prediction Page
# ==========================

@app.route("/predict")
def predict():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("predict.html")
 # ==========================================
# Prediction Logic
# ==========================================

@app.route("/submit", methods=["POST"])
def submit():

    if "user" not in session:
        return redirect(url_for("login"))

    # ==========================
    # Read Form Data
    # ==========================

    gender = request.form["Gender"]
    married = request.form["Married"]
    dependents = request.form["Dependents"]
    education = request.form["Education"]
    self_employed = request.form["Self_Employed"]

    applicant_income = float(request.form["ApplicantIncome"])
    coapplicant_income = float(request.form["CoapplicantIncome"])

    # User enters loan amount in Rupees
    loan_amount = float(request.form["LoanAmount"])

    # Convert Rupees to Thousands (dataset format)
    loan_amount = loan_amount / 1000

    loan_term = float(request.form["Loan_Amount_Term"])
    credit_history = float(request.form["Credit_History"])

    property_area = request.form["Property_Area"]

    # ==========================
    # Feature Engineering
    # ==========================

    total_income = applicant_income + coapplicant_income

    loan_income_ratio = loan_amount / max(total_income, 1)

    monthly_loan_burden = loan_amount / max(loan_term, 1)

    # ==========================
    # One-Hot Encoding
    # ==========================

    Gender_Male = 1 if gender == "1" else 0
    Married_Yes = 1 if married == "1" else 0

    Dependents_1 = 1 if dependents == "1" else 0
    Dependents_2 = 1 if dependents == "2" else 0
    Dependents_3 = 1 if dependents == "3" else 0

    Education_Not_Graduate = 1 if education == "0" else 0

    Self_Employed_Yes = 1 if self_employed == "1" else 0

    Property_Area_Semiurban = 1 if property_area == "1" else 0
    Property_Area_Urban = 1 if property_area == "2" else 0

    # ==========================
    # Feature Vector
    # ==========================

    features = [[
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit_history,
        total_income,
        loan_income_ratio,
        monthly_loan_burden,
        Gender_Male,
        Married_Yes,
        Dependents_1,
        Dependents_2,
        Dependents_3,
        Education_Not_Graduate,
        Self_Employed_Yes,
        Property_Area_Semiurban,
        Property_Area_Urban
    ]]

    # ==========================
    # Scale Features
    # ==========================

    scaled_features = scaler.transform(features)

    # ==========================
    # Prediction
    # ==========================

    prediction = model.predict(scaled_features)

    if prediction[0] == 1:
        result = "approved"
    else:
        result = "rejected"

    return render_template(
        "result.html",
        prediction=result
    )


# ==========================
# Logout
# ==========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

# ==========================
# Run App
# ==========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)