from commands import Commands


# def client():
#     cmd = Commands()
#     while True:
#         command = input('--> ').split()
#
#         match command:
#             case 'exit',:
#                 break
#
#             case 'mkfs', n:
#                 cmd.mkfs(int(n))
#             case 'mount',:
#                 cmd.mount()
#             case 'umount',:
#                 cmd.unmount()
#             case 'fstad', n:
#                 cmd.fstat(int(n))
#             case 'create', name:
#                 cmd.create(name)
#             case 'open', name:
#                 cmd.open(name)
#             case 'read', fd, offset, size:
#                 cmd.read(fd, offset, size)
#             case 'write', fd, offset, data:
#                 cmd.write(fd, offset, data)
#             case 'close', fd:
#                 cmd.close(fd)
#             case 'link', name1, name2:
#                 cmd.link(name1, name2)
#             case 'unlink', name:
#                 cmd.unlink(name)
#             case 'ls',:
#                 cmd.ls()
#             case 'truncate', name, size:
#                 pass
#
#             case _:
#                 print('Not a valid command, type help for more info')


def client():
    cmd = Commands()
    cmd.mount()
    cmd.create('file1')
    cmd.create('file2')
    cmd.write(1, 0, '---------------Hello world!---------------')
    cmd.write(1, 3, '<<<')
    cmd.write(1, 32, '>>>')
    cmd.create('test')
    cmd.write(1, 33, 'Some new data')
    cmd.read(1, 3, 13)
    cmd.read(1, 0, 100)
    cmd.ls()
    cmd.fstat(0)
    cmd.open('file2')
    cmd.open('file1')
    cmd.close(2)
    cmd.link('link1', 'file1')
    cmd.unlink('file1')
    cmd.open('link1')
    cmd.truncate('link1', 100)
    cmd.read(1, 0, 100)
    cmd.truncate('link1', 15)
    cmd.read(1, 0, 100)
