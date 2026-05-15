from .block import Block


class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # First block of blockchain
    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    # Get latest block
    def get_latest_block(self):
        return self.chain[-1]

        # Add new block
    def add_block(self, new_block):

        new_block.previous_hash = self.get_latest_block().hash

        new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)

        # Save block to file
        with open(
            "blockchain/blockchain_logs.txt",
            "a"
        ) as file:

            file.write(
                f"\nBlock Index: {new_block.index}\n"
            )

            file.write(
                f"Timestamp: {new_block.timestamp}\n"
            )

            file.write(
                f"Data: {new_block.data}\n"
            )

            file.write(
                f"Previous Hash: "
                f"{new_block.previous_hash}\n"
            )

            file.write(
                f"Current Hash: "
                f"{new_block.hash}\n"
            )

            file.write(
                "--------------------------\n"
            )
    # Display blockchain
    def display_chain(self):

        for block in self.chain:

            print("\n---------------------------")
            print("Block Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Current Hash:", block.hash)

    # Validate blockchain
    def validate_chain(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check current hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check previous hash linkage
            if current_block.previous_hash != previous_block.hash:
                return False

        return True