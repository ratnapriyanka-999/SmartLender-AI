# SmartLender AI

An AI-powered Loan Eligibility Prediction System built using Flask and Machine Learning.

---

## Overview

SmartLender AI predicts whether a loan application is likely to be approved based on applicant details such as income, credit history, education, employment status, and property area.

The application provides:

- User Registration & Login
- Secure Password Hashing
- Loan Eligibility Prediction
- Analytics Dashboard
- AI Model Information
- Responsive User Interface

---

## Features

- User Authentication using SQLite
- Machine Learning Prediction
- Dashboard
- Analytics Page
- AI Model Details
- Responsive Design
- Secure Session Management

---

## Technologies Used

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons

### Backend

- Flask
- SQLite
- Joblib

### Machine Learning

- Scikit-learn
- XGBoost
- Random Forest
- Decision Tree
- KNN

---

## Dataset

Loan Prediction Dataset

Features include:

- Gender
- Married
- Dependents
- Education
- Self Employed
- Applicant Income
- Coapplicant Income
- Loan Amount
- Loan Amount Term
- Credit History
- Property Area

---

## Project Structure

```
SmartLender-AI/

│

├── app.py

├── database.py

├── users.db

├── requirements.txt

│

├── dataset/

├── model/

├── static/

│ ├── css/

│ └── images/

│

├── templates/

│ ├── components/

│ ├── login.html

│ ├── register.html

│ ├── dashboard.html

│ ├── predict.html

│ ├── result.html

│ ├── analytics.html

│ └── model.html

│

└── README.md
```

---

## Installation

Clone the repository

```
git clone <repository-url>
```

Install dependencies

```
pip install -r requirements.txt
```

Run

```
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## Machine Learning Models

- Decision Tree
- Random Forest
- KNN
- XGBoost

Random Forest was selected as the final prediction model.

---

## Future Enhancements

- Email Verification
- Prediction History
- Admin Dashboard
- PDF Report Generation
- Explainable AI
- Cloud Deployment

---

## Developed By

Priya

SmartLender AI

2026