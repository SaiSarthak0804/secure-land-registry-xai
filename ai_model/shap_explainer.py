import pandas as pd

import shap

import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier


# =========================
# GENERATE SHAP EXPLANATION
# =========================

def generate_xai(

    area,

    transaction_count,

    market_value,

    owner_history,

    transfer_frequency,

    district,

    land_type,

    verification_status
):

    # =========================
    # LOAD DATASET
    # =========================

    data = pd.read_csv(
        "datasets/land_fraud_dataset.csv"
    )

    # =========================
    # MANUAL SAFE ENCODING
    # =========================

    district_mapping = {

        "Khordha": 0,
        "Cuttack": 1,
        "Puri": 2,
        "Sambalpur": 3,
        "Bhubaneswar": 4
    }

    land_type_mapping = {

        "Agricultural": 0,
        "Residential": 1,
        "Commercial": 2
    }

    verification_mapping = {

        "Verified": 1,
        "Pending": 0
    }

    # APPLY ENCODING TO DATASET

    data["district"] = data["district"].map(
        district_mapping
    )

    data["land_type"] = data["land_type"].map(
        land_type_mapping
    )

    data["verification_status"] = data[
        "verification_status"
    ].map(
        verification_mapping
    )

    # =========================
    # FEATURES
    # =========================

    X = data[
        [
            "area",
            "transaction_count",
            "market_value",
            "owner_history",
            "transfer_frequency",
            "district",
            "land_type",
            "verification_status"
        ]
    ]

    # =========================
    # TARGET
    # =========================

    y = data["fraud"]

    # =========================
    # TRAIN MODEL
    # =========================

    model = DecisionTreeClassifier(

        max_depth=6,

        random_state=42
    )

    model.fit(X, y)

    # =========================
    # SHAP EXPLAINER
    # =========================

    explainer = shap.Explainer(

        model,

        X
    )

    # =========================
    # SAFE INPUT ENCODING
    # =========================

    district_encoded = district_mapping.get(
        district,
        0
    )

    land_type_encoded = land_type_mapping.get(
        land_type,
        0
    )

    verification_encoded = verification_mapping.get(
        verification_status,
        0
    )

    # =========================
    # INPUT SAMPLE
    # =========================

    sample = pd.DataFrame(

        [[

            area,

            transaction_count,

            market_value,

            owner_history,

            transfer_frequency,

            district_encoded,

            land_type_encoded,

            verification_encoded
        ]],

        columns=[

            "area",

            "transaction_count",

            "market_value",

            "owner_history",

            "transfer_frequency",

            "district",

            "land_type",

            "verification_status"
        ]
    )

    # =========================
    # SHAP VALUES
    # =========================

    shap_values = explainer(sample)

    # =========================
    # CREATE FIGURE
    # =========================

    plt.figure(figsize=(12, 6))

    shap.plots.waterfall(

        shap_values[0, :, 0],

        show=False
    )

    # =========================
    # SAVE IMAGE
    # =========================

    plt.savefig(

        "static/shap_plot.png",

        bbox_inches="tight"
    )

    plt.close()