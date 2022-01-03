from commands import Commands


def client():
    cmd = Commands()
    cmd.mount()
    cmd.create('dummy_text')
    cmd.create('test_file')
    cmd.write(1, 0, "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s")
    cmd.read(1, 0, 1000)
    cmd.write(1, 3, ' <change data at position 3>')
    cmd.write(1, 52, '<change data at position 32>')
    cmd.read(1, 0, 1000)
    cmd.read(1, 30, 60)
    cmd.ls()
    cmd.fstat(0)
    cmd.open('dummy_text')
    cmd.open('test_file')
    cmd.close(2)
    cmd.link('new_name', 'dummy_text')
    cmd.unlink('dummy_text')
    cmd.open('new_name')
    cmd.truncate('new_name', 100)
    cmd.read(1, 0, 100)
