import pandas as pd

from sklearn.tree import DecisionTreeClassifier

# Load dataset
data = pd.read_csv("datasets/land_fraud_dataset.csv")

# Features
X = data[["area", "transaction_count"]]

# Target
y = data["fraud"]

# Train model
model = DecisionTreeClassifier()

model.fit(X, y)

print("AI Fraud Detection Model Trained Successfully!")

# Test prediction
area = float(input("\nEnter Land Area: "))
transaction_count = int(input("Enter Transaction Count: "))

prediction = model.predict([[area, transaction_count]])

# Output result
if prediction[0] == 1:
    print("\nSuspicious Transaction Detected!")
else:
    print("\nTransaction Looks Safe.")