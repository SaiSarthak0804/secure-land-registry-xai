from database.db_connect import connection


cursor = connection.cursor()

print("\n========== SEARCH LAND ==========\n")

# User input
land_id = input("Enter Land ID to Search: ")

# Search query
query = """
SELECT * FROM land_records
WHERE land_id = %s
"""

cursor.execute(query, (land_id,))

record = cursor.fetchone()

# Record found
if record:

    print("\n========== LAND DETAILS ==========\n")

    print(f"Record ID: {record[0]}")
    print(f"Owner Name: {record[1]}")
    print(f"Land ID: {record[2]}")
    print(f"Location: {record[3]}")
    print(f"Area: {record[4]}")
    print(f"Registration Date: {record[5]}")

# Record not found
else:

    print("\nNo Land Record Found!")

cursor.close()
connection.close()