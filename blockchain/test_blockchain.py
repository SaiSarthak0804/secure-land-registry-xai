from blockchain import Blockchain
from block import Block

# Create blockchain
land_chain = Blockchain()

# Add blocks
land_chain.add_block(
    Block(1, "Land Registered: Sai - LAND101", "")
)

land_chain.add_block(
    Block(2, "Land Registered: Alex - LAND102", "")
)

# Display blockchain
land_chain.display_chain()