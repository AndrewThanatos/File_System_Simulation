from constants import SYSTEM_WIDE, BLOCK_SIZE
from block import Block


class DescriptorType:
    is_dir = None
    is_file = None
    is_symblink = None

    def repr(self):
        if self.is_dir:
            return 'Dir.'
        elif self.is_file:
            return 'File'
        elif self.is_symblink:
            return 'Symblink'
        else:
            return 'UND.'


class Descriptor:
    def __init__(self):
        self.desc_id = self._get_descriptor_id()
        self.type = DescriptorType()

    @staticmethod
    def _get_descriptor_id():
        return SYSTEM_WIDE['descriptors_id'].pop(0)


class FileDescriptor(Descriptor):
    def __init__(self):
        super().__init__()
        self.ref_count = 1
        self.blocks: list[Block] = []
        self.type.is_file = True

    def get_size(self):
        return sum(block.size for block in self.blocks)

    def get_full_size(self):
        return len(self.blocks) * BLOCK_SIZE

    def _add_empty_block(self):
        self.blocks.append(Block())

    def add_descriptor_data(self, offset, data):
        data = list(data)
        while offset + len(data) >= self.get_full_size():
            self._add_empty_block()

        block_index = offset // BLOCK_SIZE
        block_offset = offset % BLOCK_SIZE
        while data:
            if not self.blocks[block_index].add_data(block_offset, data[0]):
                block_offset = 0
                block_index += 1
            else:
                data.pop(0)
                block_offset += 1

    def get_descriptor_data(self, offset, size):
        cur_size = 0
        result = []
        block_index = offset // BLOCK_SIZE
        block_offset = offset % BLOCK_SIZE

        while cur_size != size and not block_index >= len(self.blocks):
            byte_data = self.blocks[block_index].get_data(block_offset)
            if byte_data:
                result.append(byte_data)
                cur_size += 1
            block_offset += 1
            if block_offset == BLOCK_SIZE:
                block_offset = 0
                block_index += 1

        return result

    def change_descriptor_size(self, new_size):
        while new_size > self.get_full_size():
            self._add_empty_block()

        block_amount = len(self.blocks)
        new_block_amount = new_size // BLOCK_SIZE
        for i in range(new_block_amount, block_amount - 1):
            self.blocks.pop(new_block_amount)

        block_offset = new_size % BLOCK_SIZE
        while self.blocks[-1].remove_data(block_offset):
            block_offset += 1

    def __repr__(self):
        return '|%5d|%15s|%15d|%15d|%15d|%15d|' % (
            self.desc_id, self.type.repr(), self.get_size(), self.get_full_size(), self.ref_count, len(self.blocks)
        )


class DirDescriptor(Descriptor):
    def __init__(self):
        super().__init__()
        self.links = {}
        self.default_links = {}
        self.type.is_dir = True

    def __repr__(self):
        return '|%5d|%15s|%15d|' % (
            self.desc_id, self.type.repr(), len(self.links)
        )

    def set_default_links(self, prev_desk_id):
        self.default_links = {'.': self.desc_id, '..': prev_desk_id}

    def set_default_root_links(self):
        self.default_links = {'.': self.desc_id, '..': self.desc_id}


class SymbLinkDescriptor(Descriptor):
    def __init__(self):
        super().__init__()
        self.links = {}
        self.type.is_symblink = True
        self.path = ''

    def set_path(self, path):
        self.path = path

    def __repr__(self):
        return 'ID = %3d, path: %s' % (self.desc_id, self.path)






