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

    def fstat(self, desc_id):
        descriptor = self.fs.get_descriptor_by_id(desc_id)
        if descriptor:
            print(descriptor)

    def ls(self):
        print('-'*100)
        files, dirs, symlinks = self.fs.get_descriptors_data_in_dir()
        if files:
            print('|%5s|%15s|%15s|%15s|%15s|%15s|' % ('ID', 'Type', 'Data size', 'Full size', 'Ref. count', 'Blocks count'))
        for file in files:
            print(file)
        if dirs:
            print('|%5s|%15s|%15s|' % ('ID', 'Type', 'Links count'))
        for directory in dirs:
            print(directory)
        if symlinks:
            print('Symlinks:')
        for symlink in symlinks:
            print(symlink)


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
        data = self.fs.read_descriptor(fd, offset, size)
        if data:
            print(f'File id {fd} data:')
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

    def mkdir(self, path):
        if self.fs.create_directory(path):
            print('Directory created')

    def rmdir(self, path):
        if self.fs.remove_directory(path):
            print('Directory deleted')

    def cd(self, path):
        if self.fs.change_cwd(path):
            print('CWD changed')

    def symblink(self, data, path):
        self.fs.create_symblink(data, path)
        print('Symlink created')




