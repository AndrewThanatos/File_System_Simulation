from descriptor import FileDescriptor, DirDescriptor, SymbLinkDescriptor
from constants import DESCRIPTORS_AMOUNT
from errors import (
    not_enough_descriptors_error, file_not_opened_error, link_not_found_error, file_not_found_by_id_error,
    file_not_found_by_name_error, descriptor_is_not_a_file_error, too_big_offset_error, not_correct_path_error
)


class SystemDriver:
    def __init__(self, descriptor_amount=DESCRIPTORS_AMOUNT):
        self.MAX_DESCRIPTORS = descriptor_amount
        self._descriptor_mapping = {}
        self._opened_descriptors = []
        self._file_descriptors = {}
        self._dir_descriptors = {}
        self._symblink_descriptors = {}
        self.root: DirDescriptor = self._add_dir_descriptor(is_root=True)
        self.cwd: DirDescriptor = self.root

    def _add_file_descriptor(self):
        descriptor = FileDescriptor()
        self._descriptor_mapping[descriptor.desc_id] = descriptor
        self._file_descriptors[descriptor.desc_id] = descriptor
        return descriptor

    def _add_dir_descriptor(self, is_root=None, cwd=None):
        descriptor = DirDescriptor()
        self._descriptor_mapping[descriptor.desc_id] = descriptor
        self._dir_descriptors[descriptor.desc_id] = descriptor
        if is_root:
            descriptor.set_default_root_links()
        else:
            if not cwd:
                cwd = self.cwd
            descriptor.set_default_links(cwd.desc_id)
        return descriptor

    def _check_descriptor_presence_by_id(self, fd):
        if fd not in self._descriptor_mapping:
            file_not_found_by_id_error()
            return False
        return True

    def _is_file_descriptor(self, fd):
        if self._descriptor_mapping[fd].type.is_file:
            return True
        else:
            descriptor_is_not_a_file_error()
            return False

    def check_descriptor_presence_by_path(self, path, name):
        cwd = self._get_cwd(path)
        if name not in cwd.links:
            file_not_found_by_name_error()
            return False
        else:
            fd = cwd.links[name]
            return self._check_descriptor_presence_by_id(fd)

    def create_file(self, path):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if len(self._descriptor_mapping) <= self.MAX_DESCRIPTORS:
            descriptor = self._add_file_descriptor()
            cwd.links[name] = descriptor.desc_id
            return True
        else:
            not_enough_descriptors_error()
            return

    def open_descriptor(self, path):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if not self.check_descriptor_presence_by_path(new_path, name):
            return
        descriptor = self._descriptor_mapping[cwd.links[name]]
        if not self._is_file_descriptor(descriptor.desc_id):
            return
        self._opened_descriptors.append(descriptor.desc_id)
        return True

    def close_descriptor(self, fd):
        if fd in self._opened_descriptors:
            self._opened_descriptors.remove(fd)
        else:
            file_not_opened_error()

    def read_descriptor(self, fd, offset, size):
        if not self._check_descriptor_presence_by_id(fd) or not self._is_file_descriptor(fd):
            return
        descriptor = self._descriptor_mapping[fd]
        if descriptor.get_full_size() < offset:
            too_big_offset_error()
            return
        return descriptor.get_descriptor_data(offset, size)

    def write_descriptor(self, fd, offset, data):
        if not self._check_descriptor_presence_by_id(fd) or not self._is_file_descriptor(fd):
            return
        descriptor = self._descriptor_mapping[fd]
        descriptor.add_descriptor_data(offset, data)
        return True

    def link_descriptor(self, name1, path):
        new_path, name2 = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if name2 not in cwd.links:
            link_not_found_error()
            return
        descriptor = self._descriptor_mapping[cwd.links[name2]]
        cwd.links[name1] = descriptor.desc_id
        self._descriptor_mapping[descriptor.desc_id].ref_count += 1
        return True

    def unlink_descriptor(self, path):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if name in cwd.links:
            cwd.links.pop(name)
        else:
            link_not_found_error()
            return None
        return True

    def change_file_size(self, path, new_size):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if not self.check_descriptor_presence_by_path(new_path, name):
            return
        descriptor = self._descriptor_mapping[cwd.links[name]]
        if not self._is_file_descriptor(descriptor.desc_id):
            return
        descriptor.change_descriptor_size(new_size)
        return True

    def get_descriptors_data_in_dir(self):
        cwd = self.cwd
        files = set()
        dirs = set()
        symlinks = set()
        for _, desc_id in cwd.links.items():
            descriptor = self._descriptor_mapping[desc_id]
            if descriptor.type.is_file:
                files.add(descriptor)
            elif descriptor.type.is_dir:
                dirs.add(descriptor)
            elif descriptor.type.is_symblink:
                symlinks.add(descriptor)

        return files, dirs, symlinks

    def get_descriptor_by_id(self, desc_id):
        if not self._check_descriptor_presence_by_id(desc_id):
            return
        return self._descriptor_mapping[desc_id]

    def _get_cwd(self, path):
        if path.startswith('/'):
            cwd = self.root
            path = path.strip('/')
        else:
            cwd = self.cwd
        if not path:
            return cwd
        path_list = path.split('/')
        for name in path_list:
            full_links = cwd.links | cwd.default_links
            if name not in full_links:
                not_correct_path_error()
                return
            cwd = self._descriptor_mapping[full_links[name]]
        return cwd
    
    def change_cwd(self, path):
        new_cwd = self._get_cwd(path)
        if new_cwd:
            self.cwd = new_cwd
            return True
        return False
    
    @staticmethod
    def _path_name_split(path):
        path_list = path.split('/')
        name = path_list[-1]
        new_path = ('/' if path.startswith('/') else '') + '/'.join(path_list[:-1])
        return new_path, name
    
    def create_directory(self, path):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if not cwd:
            return
        descriptor = self._add_dir_descriptor(cwd=cwd)
        cwd.links[name] = descriptor.desc_id
        return True

    def remove_directory(self, path):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        if not self.check_descriptor_presence_by_path(new_path, name):
            return
        descriptor = self._descriptor_mapping[cwd.links[name]]
        self._dir_descriptors.pop(descriptor.desc_id)
        self._descriptor_mapping.pop(descriptor.desc_id)
        cwd.links.pop(name)

    def create_symblink(self, data, path):
        new_path, name = self._path_name_split(path)
        cwd = self._get_cwd(new_path)
        symblink = SymbLinkDescriptor()
        symblink.set_path(data)
        cwd.links[name] = symblink.desc_id
        self._descriptor_mapping[symblink.desc_id] = symblink
        self._symblink_descriptors[symblink.desc_id] = symblink





        
        
        



















