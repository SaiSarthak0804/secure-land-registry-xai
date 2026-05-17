from database.db_connect import connection


# Database cursor
cursor = connection.cursor()

print("\n========== TRANSACTION HISTORY ==========\n")

# Fetch records
query = """
SELECT
    owner_name,
    land_id,
    location,
    area,
    registration_date
FROM land_records
ORDER BY registration_date DESC
"""

cursor.execute(query)

records = cursor.fetchall()

# No records
if not records:

    print("No transaction history found!")

# Display records
else:

    for record in records:

        print(f"Owner Name       : {record[0]}")
        print(f"Land ID          : {record[1]}")
        print(f"Location         : {record[2]}")
        print(f"Area             : {record[3]}")
        print(f"Registration Date: {record[4]}")

        print("-----------------------------------")


# Fraud summary
fraud_query = """
SELECT COUNT(*) FROM fraud_logs
"""

cursor.execute(fraud_query)

fraud_count = cursor.fetchone()[0]

print(f"\nTotal Fraud Cases Detected: {fraud_count}")

# Close cursor only
cursor.close()