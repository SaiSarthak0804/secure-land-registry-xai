import pandas as pd
import shap
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier


# Load dataset
data = pd.read_csv("datasets/land_fraud_dataset.csv")

# Features
X = data[["area", "transaction_count"]]

# Target
y = data["fraud"]

# Train AI model
model = DecisionTreeClassifier()

model.fit(X, y)


# XAI explanation function
def generate_xai(area, transaction_count):

    # Create SHAP explainer
    explainer = shap.Explainer(model, X)

    # Sample transaction
    sample_data = pd.DataFrame(
        [[area, transaction_count]],
        columns=["area", "transaction_count"]
    )

    # Generate SHAP values
    shap_values = explainer(sample_data)

    print("\nGenerating XAI Explanation...")

    # Generate waterfall plot
    shap.plots.waterfall(shap_values[0, :, 0])

    # Show graph
    plt.show()