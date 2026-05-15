from blockchain.blockchain import Blockchain
from blockchain.block import Block


# Create blockchain
land_chain = Blockchain()

# Add sample blocks
land_chain.add_block(
    Block(
        1,
        "Land Record: LAND101",
        ""
    )
)

land_chain.add_block(
    Block(
        2,
        "Land Record: LAND102",
        ""
    )
)

# Verify blockchain
print("\nVerifying Blockchain...\n")

if land_chain.validate_chain():

    print("Blockchain Integrity VERIFIED")
    print("No Tampering Detected")

else:

    print("Blockchain TAMPERED!")