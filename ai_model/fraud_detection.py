import pandas as pd

from sklearn.tree import DecisionTreeClassifier

from sklearn.preprocessing import LabelEncoder

# LOAD DATASET

data = pd.read_csv(
    "datasets/land_fraud_dataset.csv"
)

# ENCODE CATEGORICAL DATA

district_encoder = LabelEncoder()

land_type_encoder = LabelEncoder()

verification_encoder = LabelEncoder()

data["district"] = district_encoder.fit_transform(
    data["district"]
)

data["land_type"] = land_type_encoder.fit_transform(
    data["land_type"]
)

data["verification_status"] = verification_encoder.fit_transform(
    data["verification_status"]
)

# FEATURES

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

# TARGET

y = data["fraud"]

# TRAIN MODEL

model = DecisionTreeClassifier()

model.fit(X, y)

print(
    "AI Fraud Detection Model Trained Successfully!"
)

# USER INPUT

area = float(
    input("\nEnter Land Area: ")
)

transaction_count = int(
    input("Enter Transaction Count: ")
)

market_value = int(
    input("Enter Market Value: ")
)

owner_history = int(
    input("Enter Owner History Count: ")
)

transfer_frequency = int(
    input("Enter Transfer Frequency: ")
)

district = input(
    "Enter District: "
)

land_type = input(
    "Enter Land Type: "
)

verification_status = input(
    "Enter Verification Status: "
)

# ENCODE INPUTS

district_encoded = district_encoder.transform(
    [district]
)[0]

land_type_encoded = land_type_encoder.transform(
    [land_type]
)[0]

verification_encoded = verification_encoder.transform(
    [verification_status]
)[0]

# PREDICTION

prediction = model.predict([[
    area,
    transaction_count,
    market_value,
    owner_history,
    transfer_frequency,
    district_encoded,
    land_type_encoded,
    verification_encoded
]])

# RESULT

if prediction[0] == 1:

    print(
        "\nSuspicious Transaction Detected!"
    )

else:

    print(
        "\nTransaction Looks Safe."
    )