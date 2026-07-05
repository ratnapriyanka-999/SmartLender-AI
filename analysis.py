import pandas as pd

# Load dataset
data = pd.read_csv("dataset/loan_prediction.csv")

print("First 5 Rows")
print(data.head())

print("\nDataset Information")
print(data.info())

print("\nDataset Shape")
print(data.shape)

print("\nStatistical Summary")
print(data.describe())

print("\nMissing Values")
print(data.isnull().sum())
import matplotlib.pyplot as plt
import seaborn as sns

# Loan Status
sns.countplot(x="Loan_Status", data=data)
plt.title("Loan Status Distribution")
plt.show()
sns.countplot(x="Gender", data=data)
plt.title("Gender Distribution")
plt.show()
sns.countplot(x="Education", data=data)
plt.title("Education Distribution")
plt.show()
sns.histplot(data["ApplicantIncome"], bins=30)
plt.title("Applicant Income Distribution")
plt.show()
sns.histplot(data["LoanAmount"], bins=30)
plt.title("Loan Amount Distribution")
plt.show()
# ===========================
# BIVARIATE ANALYSIS
# ===========================

# Gender vs Loan Status
sns.countplot(x="Gender", hue="Loan_Status", data=data)
plt.title("Gender vs Loan Status")
plt.show()

# Education vs Loan Status
sns.countplot(x="Education", hue="Loan_Status", data=data)
plt.title("Education vs Loan Status")
plt.show()

# Property Area vs Loan Status
sns.countplot(x="Property_Area", hue="Loan_Status", data=data)
plt.title("Property Area vs Loan Status")
plt.show()

# Applicant Income vs Loan Amount
sns.scatterplot(
    x="ApplicantIncome",
    y="LoanAmount",
    data=data
)
plt.title("Applicant Income vs Loan Amount")
plt.show()
# ===========================
# MULTIVARIATE ANALYSIS
# ===========================

# Create a copy of the dataset
df = data.copy()

# Convert categorical columns to numeric
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("category").cat.codes

# Correlation Heatmap
plt.figure(figsize=(12,8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Pairplot
sns.pairplot(
    df[[
        "ApplicantIncome",
        "LoanAmount",
        "Credit_History"
    ]]
)
plt.show()