from database.db_connect import connection

from blockchain.blockchain import Blockchain

from blockchain.block import Block

from ai_model.fraud_checker import check_fraud

from ai_model.shap_explainer import generate_xai

from blockchain.digital_signature import (
    generate_signature,
    verify_signature
)


# =========================
# CREATE BLOCKCHAIN
# =========================

land_chain = Blockchain()

# DATABASE CURSOR

cursor = connection.cursor()


print("\n========== LAND REGISTRATION ==========\n")

# =========================
# USER INPUT
# =========================

owner_name = input(
    "Enter Owner Name: "
)

land_id = input(
    "Enter Land ID: "
)

location = input(
    "Enter Location: "
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

area = float(
    input("Enter Land Area: ")
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

# =========================
# CHECK DUPLICATE LAND ID
# =========================

check_query = """
SELECT * FROM land_records
WHERE land_id = %s
"""

cursor.execute(
    check_query,
    (land_id,)
)

existing_land = cursor.fetchone()

# DUPLICATE DETECTED

if existing_land:

    print("\nDuplicate Land ID Detected!")

    print("Land Registration Failed.")

    cursor.close()

    connection.close()

    exit()

# =========================
# STORE IN POSTGRESQL
# =========================

insert_query = """
INSERT INTO land_records
(owner_name, land_id, location, area)
VALUES (%s, %s, %s, %s)
"""

cursor.execute(

    insert_query,

    (
        owner_name,
        land_id,
        location,
        area
    )
)

connection.commit()

print("\nLand Registered Successfully!")

# =========================
# BLOCKCHAIN BLOCK
# =========================

block_data = (

    f"{land_id} | "

    f"{owner_name} | "

    f"{location} | "

    f"{area}"
)

new_block = Block(

    len(land_chain.chain),

    block_data,

    land_chain.get_latest_block().hash
)

land_chain.add_block(
    new_block
)

print("\nBlockchain Record Added!")

# =========================
# DIGITAL SIGNATURE
# =========================

signature = generate_signature(
    block_data
)

# VERIFY SIGNATURE

is_verified = verify_signature(

    block_data,

    signature
)

# SIGNATURE RESULT

if is_verified:

    print(
        "Digital Signature VERIFIED"
    )

else:

    print(
        "Digital Signature FAILED"
    )

# =========================
# VALIDATE BLOCKCHAIN
# =========================

if land_chain.validate_chain():

    print(
        "Blockchain VALID"
    )

else:

    print(
        "Blockchain INVALID"
    )

# =========================
# AI FRAUD DETECTION
# =========================

is_fraud, reason, confidence = check_fraud(

    area,

    transaction_count,

    market_value,

    owner_history,

    transfer_frequency,

    district,

    land_type,

    verification_status
)

print("\n========== AI FRAUD ANALYSIS ==========\n")

print(reason)

print(
    f"Fraud Confidence: {confidence}%"
)

# =========================
# FRAUD DETECTED
# =========================

if is_fraud:

    fraud_query = """
    INSERT INTO fraud_logs
    (land_id, owner_name, fraud_reason)
    VALUES (%s, %s, %s)
    """

    cursor.execute(

        fraud_query,

        (
            land_id,
            owner_name,
            reason
        )
    )

    connection.commit()

    print(
        "\nFraud Log Stored Successfully!"
    )

# =========================
# GENERATE SHAP GRAPH
# =========================

generate_xai(

    area,

    transaction_count,

    market_value,

    owner_history,

    transfer_frequency,

    district,

    land_type,

    verification_status
)

print(
    "\nSHAP Explainable AI Graph Generated!"
)

# =========================
# CLOSE DATABASE
# =========================

cursor.close()

