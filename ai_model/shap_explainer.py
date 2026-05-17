import pandas as pd

import shap

import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier


# Generate SHAP explanation
def generate_xai(

    area,
    transaction_count,
    market_value,
    owner_history
):

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

    # SHAP explainer
    explainer = shap.Explainer(
        model,
        X
    )

    # Input sample
    sample = pd.DataFrame(

        [[
            area,
            transaction_count,
            market_value,
            owner_history
        ]],

        columns=[
            "area",
            "transaction_count",
            "market_value",
            "owner_history"
        ]
    )

    # SHAP values
    shap_values = explainer(sample)

    # Create figure
    plt.figure(figsize=(10, 5))

    # SHAP waterfall plot
    shap.plots.waterfall(

        shap_values[0, :, 0],

        show=False
    )

    # Save image
    plt.savefig(

        "static/shap_plot.png",

        bbox_inches="tight"
    )

    plt.close()