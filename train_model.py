import pandas as pd
import joblib

from pandas.api.types import is_numeric_dtype

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, classification_report

# ==========================================
# Load Dataset
# ==========================================

print("Loading Dataset...")

data = pd.read_csv("dataset/loan_prediction.csv")

# ==========================================
# Handle Missing Values
# ==========================================

for col in data.columns:
    if is_numeric_dtype(data[col]):
        data[col] = data[col].fillna(data[col].median())
    else:
        data[col] = data[col].fillna(data[col].mode()[0])

# ==========================================
# Remove Loan_ID
# ==========================================

if "Loan_ID" in data.columns:
    data = data.drop("Loan_ID", axis=1)

# ==========================================
# Convert Categorical Columns
# ==========================================

data = pd.get_dummies(data, drop_first=True)

data = data.astype(int)

# ==========================================
# Features and Target
# ==========================================

X = data.drop("Loan_Status_Y", axis=1)
y = data["Loan_Status_Y"]

# ==========================================
# Feature Scaling
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# ==========================================
# Decision Tree
# ==========================================

print("\n==============================")
print("Decision Tree Model")
print("==============================")

dt_model = DecisionTreeClassifier(random_state=42)

dt_model.fit(X_train, y_train)

dt_pred = dt_model.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_pred)

print("Accuracy :", dt_accuracy)

print("\nClassification Report")
print(classification_report(y_test, dt_pred))

# ==========================================
# Random Forest
# ==========================================

print("\n==============================")
print("Random Forest Model")
print("==============================")

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

print("Accuracy :", rf_accuracy)

print("\nClassification Report")
print(classification_report(y_test, rf_pred))

# ==========================================
# KNN
# ==========================================

print("\n==============================")
print("KNN Model")
print("==============================")

knn_model = KNeighborsClassifier(n_neighbors=5)

knn_model.fit(X_train, y_train)

knn_pred = knn_model.predict(X_test)

knn_accuracy = accuracy_score(y_test, knn_pred)

print("Accuracy :", knn_accuracy)

print("\nClassification Report")
print(classification_report(y_test, knn_pred))

# ==========================================
# XGBoost
# ==========================================

print("\n==============================")
print("XGBoost Model")
print("==============================")

xgb_model = XGBClassifier(
    random_state=42,
    eval_metric="logloss"
)

xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)

xgb_accuracy = accuracy_score(y_test, xgb_pred)

print("Accuracy :", xgb_accuracy)

print("\nClassification Report")
print(classification_report(y_test, xgb_pred))

# ==========================================
# Accuracy Comparison
# ==========================================

print("\n====================================")
print("MODEL ACCURACY COMPARISON")
print("====================================")

print(f"Decision Tree : {dt_accuracy:.4f}")
print(f"Random Forest : {rf_accuracy:.4f}")
print(f"KNN           : {knn_accuracy:.4f}")
print(f"XGBoost       : {xgb_accuracy:.4f}")

accuracies = {
    "Decision Tree": dt_accuracy,
    "Random Forest": rf_accuracy,
    "KNN": knn_accuracy,
    "XGBoost": xgb_accuracy
}

best_model_name = max(accuracies, key=accuracies.get)

print("\nBest Model :", best_model_name)

# ==========================================
# Save Best Model
# ==========================================

if best_model_name == "Decision Tree":
    best_model = dt_model

elif best_model_name == "Random Forest":
    best_model = rf_model

elif best_model_name == "KNN":
    best_model = knn_model

else:
    best_model = xgb_model

joblib.dump(best_model, "model/loan_model.pkl")

print("Best model saved as model/loan_model.pkl")

# Save Scaler

joblib.dump(scaler, "model/scaler.pkl")

print("Scaler saved as model/scaler.pkl")

print("\n====================================")
print("MODEL BUILDING COMPLETED SUCCESSFULLY")
print("====================================")