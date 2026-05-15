import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score


# Load dataset
data = pd.read_csv(
    "datasets/land_fraud_dataset.csv"
)

# Features
X = data[["area", "transaction_count"]]

# Target
y = data["fraud"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42
)

# Models
models = {

    "Decision Tree": DecisionTreeClassifier(),

    "Logistic Regression": LogisticRegression(),

    "Random Forest": RandomForestClassifier()
}

print("\n========== MODEL COMPARISON ==========\n")

# Train and evaluate models
for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(f"{name} Accuracy: {accuracy:.2f}")