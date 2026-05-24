from database.db_connect import connection


# =========================
# DATABASE CURSOR
# =========================

cursor = connection.cursor()

print("\n========== SEARCH LAND ==========\n")

# =========================
# USER INPUT
# =========================

land_id = input(
    "Enter Land ID to Search: "
)

# =========================
# SEARCH QUERY
# =========================

query = """
SELECT
    owner_name,
    land_id,
    location,
    area,
    created_at
FROM land_records
WHERE land_id = %s
"""

cursor.execute(
    query,
    (land_id,)
)

record = cursor.fetchone()

# =========================
# RECORD FOUND
# =========================

if record:

    print("\n========== LAND DETAILS ==========\n")

    print(f"Owner Name: {record[0]}")
    print(f"Land ID: {record[1]}")
    print(f"Location: {record[2]}")
    print(f"Area: {record[3]}")
    print(f"Registration Date: {record[4]}")

# =========================
# RECORD NOT FOUND
# =========================

else:

    print("\nNo Land Record Found!")

# =========================
# CLOSE DATABASE
# =========================

cursor.close()

connection.close()