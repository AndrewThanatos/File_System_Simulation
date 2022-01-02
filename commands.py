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
        descriptor = self.fs.descriptor_mapping[did]
        descriptor.print_descriptor_data()

    def ls(self):
        print('|        Id|           Size|     Ref. count|    Block count|')
        for descriptor in self.fs.file_descriptors:
            print('|%10d|%15d|%15d|%15d|' %
                  (descriptor.desc_id, descriptor.byte_size, descriptor.ref_count, len(descriptor.blocks)))

    def create(self, name):
        self.fs.create_file(name)
        print(f'Created file {name}')

    def open(self, name):
        self.fs.open(name)
        print(f'Opened file {name}')

    def close(self, fd):
        self.fs.close(fd)
        print(f'Closed file id {fd}')

    def read(self, fd, offset, size):
        print(f'File id {fd} data:')
        print(''.join(list(map(str, self.fs.read(fd, offset, size)))))

    def write(self, fd, offset, data):
        self.fs.write(fd, offset, data)
        print(f'Write file id {fd}')

    def link(self, name1, name2):
        self.fs.link(name1, name2)
        print(f'Linked | {name1} -> {name2}')

    def unlink(self, name):
        self.fs.unlink(name)
        print(f'Unlinked | {name}')

    def truncate(self, name, size):
        self.fs.change_file_size(name, size)
        print('Change file size')




