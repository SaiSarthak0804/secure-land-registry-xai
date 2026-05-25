import pandas as pd

from sklearn.tree import DecisionTreeClassifier


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


# =========================
# APPLY ENCODING TO DATASET
# =========================

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
# FRAUD DETECTION FUNCTION
# =========================

def check_fraud(

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

    sample = [[

        area,

        transaction_count,

        market_value,

        owner_history,

        transfer_frequency,

        district_encoded,

        land_type_encoded,

        verification_encoded
    ]]

    # =========================
    # AI PREDICTION
    # =========================

    prediction = model.predict(sample)

    probability = model.predict_proba(
        sample
    )

    confidence = round(

        probability[0][1] * 100,

        2
    )

    # =========================
    # RULE-BASED FRAUD BOOST
    # =========================

    suspicious_score = 0

    # HIGH TRANSACTION ACTIVITY

    if transaction_count >= 5:

        suspicious_score += 25

    # MANY OWNERS

    if owner_history >= 4:

        suspicious_score += 25

    # HIGH TRANSFER FREQUENCY

    if transfer_frequency >= 5:

        suspicious_score += 25

    # PENDING VERIFICATION

    if verification_status == "Pending":

        suspicious_score += 15

    # HIGH MARKET VALUE

    if market_value >= 5000000:

        suspicious_score += 10

    # =========================
    # FINAL CONFIDENCE
    # =========================

    confidence = max(
        confidence,
        suspicious_score
    )

    # =========================
    # FRAUD DECISION
    # =========================

    if confidence >= 50:

        prediction = [1]

    else:

        prediction = [0]

    # =========================
    # FRAUD DETECTED
    # =========================

    if prediction[0] == 1:

        reason = (

            "Suspicious ownership pattern, "

            "high transfer activity, "

            "verification anomaly, or "

            "abnormal land transaction detected."
        )

        return True, reason, confidence

    # =========================
    # SAFE TRANSACTION
    # =========================

    else:

        reason = (

            "Transaction pattern appears normal."
        )

        return False, reason, confidence