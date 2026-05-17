from database.db_connect import connection

from blockchain.blockchain import Blockchain
from blockchain.block import Block


# Create blockchain
land_chain = Blockchain()

# Database cursor
cursor = connection.cursor()

print("\n========== BLOCKCHAIN VERIFICATION ==========\n")

# Get all land records
query = """
SELECT owner_name, land_id, location, area
FROM land_records
ORDER BY id
"""

cursor.execute(query)

records = cursor.fetchall()

# No records
if not records:

    print("No land records found!")

# Build blockchain from DB records
else:

    for record in records:

        owner_name = record[0]
        land_id = record[1]
        location = record[2]
        area = record[3]

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

        land_chain.add_block(new_block)

    # Validate blockchain
    if land_chain.validate_chain():

        print("Blockchain VALID")
        print("\nAll records are secure and untampered.")

    else:

        print("Blockchain INVALID")
        print("\nTampering Detected!")

# Close DB
cursor.close()
