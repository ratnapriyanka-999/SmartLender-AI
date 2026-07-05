from imblearn.over_sampling import SMOTE
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pandas.api.types import is_numeric_dtype
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# ==========================================
# Load Dataset
# ==========================================

print("Loading Dataset...")

data = pd.read_csv("dataset/loan_prediction.csv")

# ==========================================
# Missing Values Before Handling
# ==========================================

print("\n========== Missing Values Before Handling ==========")
print(data.isnull().sum())

# ==========================================
# Handle Missing Values
# ==========================================

for col in data.columns:
    if is_numeric_dtype(data[col]):
        data[col] = data[col].fillna(data[col].median())
    else:
        data[col] = data[col].fillna(data[col].mode()[0])

# ==========================================
# Missing Values After Handling
# ==========================================

print("\n========== Missing Values After Handling ==========")
print(data.isnull().sum())

# ==========================================
# Loan Status Distribution
# ==========================================

print("\n========== Loan Status Distribution ==========")
print(data["Loan_Status"].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x="Loan_Status", data=data)
plt.title("Loan Status Distribution")
plt.xlabel("Loan Status")
plt.ylabel("Count")
plt.show()

# ==========================================
# Remove Loan_ID
# ==========================================

if "Loan_ID" in data.columns:
    data = data.drop("Loan_ID", axis=1)

# ==========================================
# Convert Categorical Columns to Numeric
# ==========================================

data = pd.get_dummies(data, drop_first=True)

# Convert boolean columns into integers
data = data.astype(int)

print("\n========== Data Types ==========")
print(data.dtypes)

# ==========================================
# Features and Target
# ==========================================

target_column = "Loan_Status_Y"

X = data.drop(columns=[target_column])
y = data[target_column]

# ==========================================
# Feature Scaling
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\n========== Scaling Completed Successfully ==========")
print(X_scaled[:5])

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

print("\n========== Dataset Split ==========")
print("Training Data Shape :", X_train.shape)
print("Testing Data Shape  :", X_test.shape)

# ==========================================
# Dataset Balancing using SMOTE
# ==========================================

print("\n========== Before SMOTE ==========")
print(pd.Series(y_train).value_counts())

smote = SMOTE(random_state=42)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train,
    y_train
)

print("\n========== After SMOTE ==========")
print(pd.Series(y_train_balanced).value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x=y_train_balanced)
plt.title("Balanced Loan Status Distribution (SMOTE)")
plt.xlabel("Loan Status")
plt.ylabel("Count")
plt.show()

print("\n======================================")
print("Preprocessing Completed Successfully!")
print("======================================")