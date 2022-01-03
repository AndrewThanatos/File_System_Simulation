from descriptor import FileDescriptor, DirDescriptor
from constants import DESCRIPTORS_AMOUNT
from errors import (
    not_enough_descriptors_error, file_not_opened_error, link_not_found_error, file_not_found_error
)


class SystemDriver:
    def __init__(self, descriptor_amount=DESCRIPTORS_AMOUNT):
        self.MAX_DESCRIPTORS = descriptor_amount
        self._descriptor_mapping = {}
        self._opened_descriptors = []
        self._file_descriptors = {}
        self._dir_descriptors = {}
        self.root: DirDescriptor = self._create_root_dir()
        self.cwd: DirDescriptor = self.root

    @staticmethod
    def _create_root_dir():
        root = DirDescriptor()
        return root

    def _add_file_descriptor(self):
        descriptor = FileDescriptor()
        self._descriptor_mapping[descriptor.desc_id] = descriptor
        self._file_descriptors[descriptor.desc_id] = descriptor
        return descriptor

    def _add_dir_descriptor(self):
        descriptor = DirDescriptor()
        self._descriptor_mapping[descriptor.desc_id] = descriptor
        self._dir_descriptors[descriptor.desc_id] = descriptor
        return descriptor

    def create_file(self, name):
        if len(self._descriptor_mapping) <= self.MAX_DESCRIPTORS:
            descriptor = self._add_file_descriptor()
            cwd = self.cwd
            cwd.links[name] = descriptor.desc_id
        else:
            not_enough_descriptors_error()

    def open_descriptor(self, name):
        descriptor = self._descriptor_mapping[self.cwd.links[name]]
        self._opened_descriptors.append(descriptor.desc_id)

    def close_descriptor(self, fd):
        if fd in self._opened_descriptors:
            self._opened_descriptors.remove(fd)
        else:
            file_not_opened_error()

    def read_descriptor(self, fd, offset, size):
        descriptor = self._descriptor_mapping[fd]
        if descriptor.get_full_size() < offset:
            print('Offset size is too big')
            return None
        return descriptor.get_descriptor_data(offset, size)

    def write_descriptor(self, fd, offset, data):
        descriptor = self._descriptor_mapping[fd]
        descriptor.add_descriptor_data(offset, data)

    def link_descriptor(self, name1, name2):
        cwd = self.cwd
        descriptor = self._descriptor_mapping[cwd.links[name2]]
        cwd.links[name1] = descriptor.desc_id
        self._descriptor_mapping[descriptor.desc_id].ref_count += 1

    def unlink_descriptor(self, name):
        cwd = self.cwd
        if name in cwd.links:
            cwd.links.pop(name)
        else:
            link_not_found_error()

    def change_file_size(self, name, new_size):
        cwd = self.cwd
        if name in cwd.links:
            descriptor = self._descriptor_mapping[cwd.links[name]]
            descriptor.change_descriptor_size(new_size)
        else:
            file_not_found_error()
















