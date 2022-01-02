from descriptor import Descriptor
from constants import DESCRIPTORS_AMOUNT


class SystemDriver:
    def __init__(self, descriptor_amount):
        self.descriptor_mapping = {}
        self.opened_descriptors = {}
        self.file_descriptors = []
        self.links = {}
        self._fd_num = 0
        self._opened_fd_num = 0

    def _add_descriptor(self, descriptor):
        self.descriptor_mapping[self._fd_num] = descriptor
        descriptor.desc_id = self._fd_num
        if descriptor.is_file:
            self.file_descriptors.append(descriptor)
        self._fd_num += 1

    def _open_descriptor(self, descriptor):
        self.opened_descriptors[self._opened_fd_num] = descriptor
        self._opened_fd_num += 1

    def create_file(self, name):
        if len(self.descriptor_mapping) < DESCRIPTORS_AMOUNT:
            descriptor = Descriptor(is_dir=False)
            self._add_descriptor(descriptor)
            self.links[name] = descriptor.desc_id

    def open(self, name):
        descriptor = self.descriptor_mapping[self.links[name]]
        self._open_descriptor(descriptor)

    def close(self, fd):
        self.opened_descriptors.pop(fd)

    def read(self, fd, offset, size):
        descriptor = self.descriptor_mapping[fd]
        if descriptor.byte_size < offset:
            print('Offset size is too big')
            return None
        return descriptor.read_data(offset, size)

    def write(self, fd, offset, data):
        descriptor = self.descriptor_mapping[fd]
        descriptor.write_data(offset, data)

    def link(self, name1, name2):
        self.links[name1] = name2
        self.descriptor_mapping[name2].ref_count += 1

    def unlink(self, name):
        self.links.pop(name)

    def change_file_size(self, name, new_size):
        descriptor = self.descriptor_mapping[self.links[name]]
        descriptor.change_size(new_size)
















