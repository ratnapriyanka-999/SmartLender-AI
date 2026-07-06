import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from imblearn.over_sampling import SMOTE
from pandas.api.types import is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ==========================================
# Load Dataset
# ==========================================

print("=" * 60)
print("Loading Loan Prediction Dataset...")
print("=" * 60)

data = pd.read_csv("dataset/loan_prediction.csv")

print("\nDataset Shape :", data.shape)
data["TotalIncome"] = (
    data["ApplicantIncome"] +
    data["CoapplicantIncome"]
)

# ==========================================
# Missing Values
# ==========================================

print("\nMissing Values Before Handling")
print(data.isnull().sum())

for column in data.columns:

    if is_numeric_dtype(data[column]):
        data[column] = data[column].fillna(data[column].median())

    else:
        data[column] = data[column].fillna(data[column].mode()[0])

print("\nMissing Values After Handling")
print(data.isnull().sum())

# ==========================================
# Loan Status Distribution
# ==========================================

print("\nLoan Status Distribution")
print(data["Loan_Status"].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x="Loan_Status", data=data)
plt.title("Loan Status Distribution")
plt.tight_layout()
plt.show()
# ==========================================
# Remove Loan_ID
# ==========================================

if "Loan_ID" in data.columns:
    data.drop("Loan_ID", axis=1, inplace=True)

# ==========================================
# Feature Engineering
# ==========================================

# Total Monthly Income
data["TotalIncome"] = (
    data["ApplicantIncome"] +
    data["CoapplicantIncome"]
)

# Loan to Income Ratio
data["LoanIncomeRatio"] = (
    data["LoanAmount"] /
    data["TotalIncome"].replace(0, 1)
)

# Estimated Monthly EMI
data["MonthlyLoanBurden"] = (
    data["LoanAmount"] /
    data["Loan_Amount_Term"].replace(0, 1)
)
# ==========================================
# One-Hot Encoding
# ==========================================

data = pd.get_dummies(data, drop_first=True)

print("\nEncoded Dataset Shape :", data.shape)

# ==========================================
# Features & Target
# ==========================================

X = data.drop("Loan_Status_Y", axis=1)
y = data["Loan_Status_Y"]

print("\nFeatures")
print(list(X.columns))

# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# ==========================================
# Scaling
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "model/scaler.pkl")

print("\nScaler saved successfully.")

# ==========================================
# SMOTE
# ==========================================

smote = SMOTE(random_state=42)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_scaled,
    y_train
)

print("\nBefore SMOTE")
print(y_train.value_counts())

print("\nAfter SMOTE")
print(pd.Series(y_train_balanced).value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x=y_train_balanced)
plt.title("Balanced Training Data")
plt.tight_layout()
plt.show()

print("\nPreprocessing Completed Successfully!")

# ==========================================
# Save Processed Data
# ==========================================

joblib.dump(
    {
        "X_train": X_train_balanced,
        "X_test": X_test_scaled,
        "y_train": y_train_balanced,
        "y_test": y_test,
        "feature_names": X.columns.tolist()
    },
    "model/preprocessed_data.pkl"
)

print("Processed dataset saved as model/preprocessed_data.pkl")