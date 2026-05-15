import pandas as pd
import random


records = []

locations = [
    "Odisha",
    "Bhubaneswar",
    "Cuttack",
    "Puri",
    "Sambalpur"
]


for i in range(1, 501):

    area = round(random.uniform(1, 20), 2)

    transaction_count = random.randint(1, 10)

    market_value = random.randint(100000, 5000000)

    owner_history = random.randint(1, 8)

    # Fraud logic
    fraud = 0

    if area > 10 and transaction_count > 5:
        fraud = 1

    if owner_history > 5:
        fraud = 1

    record = {

        "land_id": f"LAND{i}",

        "area": area,

        "transaction_count": transaction_count,

        "market_value": market_value,

        "owner_history": owner_history,

        "location": random.choice(locations),

        "fraud": fraud
    }

    records.append(record)


# Create dataframe
df = pd.DataFrame(records)

# Save CSV dataset
df.to_csv(
    "datasets/land_fraud_dataset.csv",
    index=False
)

print("\nDataset Generated Successfully!\n")

print(df.head())