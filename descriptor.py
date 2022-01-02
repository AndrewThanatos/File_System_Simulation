from constants import BLOCK_SIZE
from block import Block


class Descriptor:
    def __init__(self, is_dir):
        self.is_dir = is_dir
        self.is_file = not self.is_dir
        self.desc_id = None
        self.ref_count = 1
        self.byte_size = 0
        self.blocks = []
        self.dir_links = []

    def read_data(self, offset, size):
        if size + offset > self.byte_size:
            size = self.byte_size - offset
        end = offset + size
        start_block = offset // BLOCK_SIZE
        end_block = end // BLOCK_SIZE
        if start_block == end_block:
            return self.blocks[start_block].data[offset % BLOCK_SIZE: end % BLOCK_SIZE]
        data = self.blocks[start_block].data[offset % BLOCK_SIZE:]
        for block in self.blocks[start_block + 1: end_block]:
            data += block.data
        data += self.blocks[end_block].data[: end % BLOCK_SIZE]
        return data

    def write_data(self, offset, data):
        if not self.blocks:
            self._add_empty_block()
        if offset > self.byte_size:
            offset = self.byte_size
        start_block = offset // BLOCK_SIZE

        counter = 0
        data = list(data)
        for i in range(offset % BLOCK_SIZE, BLOCK_SIZE):
            if counter >= len(data):
                break
            if i >= self.byte_size:
                self.blocks[start_block].data += data[counter]
            else:
                self.blocks[start_block].data[i] = data[counter]
            counter += 1
        data = data[counter:]
        start_block += 1
        while data:
            if start_block > len(self.blocks) - 1:
                data = self._add_data_block(data)
            else:
                block = self.blocks[start_block]
                data = self._fill_data_block(block, data)
            start_block += 1

        self._set_descriptor_size()

    def _add_data_block(self, data):
        block_data = data[:BLOCK_SIZE] if len(data) > BLOCK_SIZE else data
        self.blocks.append(Block(data=block_data))
        return data[BLOCK_SIZE:] if len(data) > BLOCK_SIZE else None

    def _add_empty_block(self):
        self.blocks.append(Block(data=[]))

    def _fill_data_block(self, block, data):
        block_data = data[:BLOCK_SIZE] if len(data) > BLOCK_SIZE else data
        block.data[: len(block_data)] = block_data
        return data[BLOCK_SIZE:] if len(data) > BLOCK_SIZE else None

    def _set_descriptor_size(self):
        if not self.blocks:
            self.byte_size = 0
            return
        self.byte_size = (len(self.blocks) - 1) * BLOCK_SIZE + self.blocks[-1].size()

    def print_descriptor_data(self):
        print(f'Id = {self.desc_id} | Size = {self.byte_size} | Ref. Count = {self.ref_count} | '
              f'Block amount = {len(self.blocks)}')

    def change_size(self, new_size):
        if len(self.blocks) * BLOCK_SIZE < new_size:
            block_to_add = new_size // BLOCK_SIZE - len(self.blocks)
            for _ in range(block_to_add):
                self._add_empty_block()
        else:
            blocks = new_size // BLOCK_SIZE
            offset = new_size % BLOCK_SIZE
            self.blocks[blocks].data = self.blocks[blocks].data[:offset]
            self.blocks = self.blocks[:blocks + 1]

        self._set_descriptor_size()




