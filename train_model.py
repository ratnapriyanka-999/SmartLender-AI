import joblib
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# ==========================================
# Load Preprocessed Data
# ==========================================

print("=" * 60)
print("Loading Preprocessed Dataset...")
print("=" * 60)

data = joblib.load("model/preprocessed_data.pkl")

X_train = data["X_train"]
X_test = data["X_test"]

y_train = data["y_train"]
y_test = data["y_test"]

feature_names = data["feature_names"]

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# ==========================================
# Models
# ==========================================

models = {

    "Decision Tree":
    DecisionTreeClassifier(
        max_depth=6,
        random_state=42
    ),

    "Random Forest":
    RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=2,
        random_state=42
    ),

    "KNN":
    KNeighborsClassifier(
        n_neighbors=5
    ),

    "XGBoost":
    XGBClassifier(
        random_state=42,
        eval_metric="logloss"
    )

}

results = {}

best_model = None
best_accuracy = 0
best_name = ""

# ==========================================
# Train Models
# ==========================================

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)
    precision = precision_score(y_test, prediction)
    recall = recall_score(y_test, prediction)
    f1 = f1_score(y_test, prediction)

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nClassification Report\n")
    print(classification_report(y_test, prediction))

    results[name] = accuracy

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_name = name

# ==========================================
# Accuracy Comparison
# ==========================================

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

for name, score in results.items():

    print(f"{name:20} : {score:.4f}")

print("\nBest Model :", best_name)
print("Accuracy   :", best_accuracy)
# ==========================================
# Feature Importance Analysis
# ==========================================

if best_name == "Random Forest":

    import matplotlib.pyplot as plt

    print("\n")
    print("=" * 70)
    print("RANDOM FOREST FEATURE IMPORTANCE")
    print("=" * 70)

    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": best_model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print(importance)

    print("\nTop 10 Most Important Features")
    print(importance.head(10))

    plt.figure(figsize=(10,6))

    plt.barh(
        importance["Feature"],
        importance["Importance"]
    )

    plt.gca().invert_yaxis()

    plt.title("Random Forest Feature Importance")

    plt.xlabel("Importance")

    plt.tight_layout()

    plt.show()
# ==========================================
# Save Model
# ==========================================

joblib.dump(
    best_model,
    "model/loan_model.pkl"
)

print("\nBest model saved successfully.")

print("\n")
print("=" * 60)
print("MODEL TRAINING COMPLETED")
print("=" * 60)