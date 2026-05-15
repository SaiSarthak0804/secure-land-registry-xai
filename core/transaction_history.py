import psycopg2


# Database connection
connection = psycopg2.connect(
    host="localhost",
    database="land_registry_db",
    user="postgres",
    password="postgresgrp8"
)

cursor = connection.cursor()

# Fetch all land records
query = """
SELECT * FROM land_records
"""

cursor.execute(query)

records = cursor.fetchall()

print("\n========== TRANSACTION HISTORY ==========\n")

# Display records
for row in records:

    print(f"ID: {row[0]}")
    print(f"Owner Name: {row[1]}")
    print(f"Land ID: {row[2]}")
    print(f"Location: {row[3]}")
    print(f"Area: {row[4]}")
    print(f"Registration Date: {row[5]}")

    print("-----------------------------------")

# Close connection
cursor.close()
connection.close()