from system_sym import SystemDriver
from typing import Optional


class Commands:
    def __init__(self):
        self.FS = SystemDriver(100)
        self.fs: Optional[SystemDriver] = None

    def mkfs(self, fd):
        self.fs = SystemDriver(descriptor_amount=fd)
        print(f'Create {fd} descriptors')

    def mount(self):
        self.fs = self.FS
        print('Mount')

    def unmount(self):
        self.fs = None
        print('Unmount')

    def fstat(self, did):
        print('fstat not implemented')

    def ls(self):
        print('|        Id|           Size|     Ref. count|    Block count|')
        print('ls not implemented')

    def create(self, name):
        if self.fs.create_file(name):
            print(f'Created file {name}')

    def open(self, name):
        if self.fs.open_descriptor(name):
            print(f'Opened file {name}')

    def close(self, fd):
        if self.fs.close_descriptor(fd):
            print(f'Closed file id {fd}')

    def read(self, fd, offset, size):
        print(f'File id {fd} data:')
        data = self.fs.read_descriptor(fd, offset, size)
        if data:
            print(''.join(list(map(str, data))))

    def write(self, fd, offset, data):
        if self.fs.write_descriptor(fd, offset, data):
            print(f'Write file id {fd}')

    def link(self, name1, name2):
        if self.fs.link_descriptor(name1, name2):
            print(f'Linked | {name1} -> {name2}')

    def unlink(self, name):
        if self.fs.unlink_descriptor(name):
            print(f'Unlinked | {name}')

    def truncate(self, name, size):
        if self.fs.change_file_size(name, size):
            print('Change file size')




