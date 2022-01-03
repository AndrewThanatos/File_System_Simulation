from constants import BLOCK_SIZE


class Block:
    def __init__(self):
        self.data = [None for _ in range(BLOCK_SIZE)]
        self.size = 0

    def size(self):
        return self.size

    def add_data(self, index, data):
        if index < BLOCK_SIZE:
            self.data[index] = data
            return True
        return False

    def remove_data(self, index):
        if index < BLOCK_SIZE:
            self.data[index] = None
            return True
        return False

    def get_data(self, index):
        return self.data[index]


