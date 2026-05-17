import pandas as pd

from sklearn.tree import DecisionTreeClassifier


# Load dataset
data = pd.read_csv(
    "datasets/land_fraud_dataset.csv"
)

# Features
X = data[
    [
        "area",
        "transaction_count",
        "market_value",
        "owner_history"
    ]
]

# Target
y = data["fraud"]

# Train model
model = DecisionTreeClassifier()

model.fit(X, y)


# Fraud detection function
def check_fraud(

    area,
    transaction_count,
    market_value,
    owner_history
):

    # Input sample
    sample = [[
        area,
        transaction_count,
        market_value,
        owner_history
    ]]

    # Prediction
    prediction = model.predict(sample)

    # Probability
    probability = model.predict_proba(sample)

    # Fraud confidence %
    confidence = round(
        probability[0][1] * 100,
        2
    )

    # Fraud detected
    if prediction[0] == 1:

        reason = (
            "Suspicious ownership pattern, "
            "high transaction count, or "
            "abnormal land value detected."
        )

        return True, reason, confidence

    # Safe transaction
    else:

        reason = (
            "Transaction pattern appears normal."
        )

        return False, reason, confidence