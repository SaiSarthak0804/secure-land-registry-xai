import pandas as pd
import random

records = []

districts = [

    "Bhubaneswar",
    "Cuttack",
    "Puri",
    "Sambalpur",
    "Rourkela",
    "Balasore",
    "Berhampur"

]

land_types = [

    "Agricultural",
    "Residential",
    "Commercial"

]

verification_statuses = [

    "Verified",
    "Pending"

]

for i in range(1, 1501):

    area = round(
        random.uniform(1, 25),
        2
    )

    transaction_count = random.randint(1, 12)

    market_value = random.randint(
        100000,
        10000000
    )

    owner_history = random.randint(1, 10)

    transfer_frequency = random.randint(0, 8)

    district = random.choice(
        districts
    )

    land_type = random.choice(
        land_types
    )

    verification_status = random.choice(
        verification_statuses
    )

    # FRAUD LOGIC

    fraud = 0

    risk_score = 0

    # High ownership transfer

    if owner_history > 6:

        risk_score += 25

    # Frequent transactions

    if transaction_count > 7:

        risk_score += 25

    # High transfer frequency

    if transfer_frequency > 5:

        risk_score += 20

    # Pending verification

    if verification_status == "Pending":

        risk_score += 15

    # Suspicious large land

    if area > 18:

        risk_score += 15

    # Fraud Threshold

    if risk_score >= 50:

        fraud = 1

    record = {

        "land_id": f"LAND{i}",

        "area": area,

        "transaction_count": transaction_count,

        "market_value": market_value,

        "owner_history": owner_history,

        "transfer_frequency": transfer_frequency,

        "district": district,

        "land_type": land_type,

        "verification_status": verification_status,

        "fraud": fraud
    }

    records.append(record)

# CREATE DATAFRAME

df = pd.DataFrame(records)

# SAVE CSV

df.to_csv(

    "datasets/land_fraud_dataset.csv",

    index=False
)

print("\nDataset Generated Successfully!\n")

print(df.head())

print("\nTotal Records Generated:")

print(len(df))