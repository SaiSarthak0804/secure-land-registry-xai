import hashlib
import datetime


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            str(self.index)
            + self.timestamp
            + str(self.data)
            + self.previous_hash
        )

        return hashlib.sha256(block_string.encode()).hexdigest()