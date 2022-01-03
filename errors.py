from termcolor import colored


def print_red(message):
    print(colored(message, 'red'))


def not_enough_descriptors_error():
    print_red('Reached max descriptors amount, file was not created')


def file_not_opened_error():
    print_red('File was not opened, so it cannot be closed')


def link_not_found_error():
    print_red('Link was not found')


def file_not_found_by_id_error():
    print_red('File was not found by id')


def file_not_found_by_name_error():
    print_red('File was not found by name')


def descriptor_is_not_a_file_error():
    print_red('Descriptor is not a file')


def too_big_offset_error():
    print_red('Offset is too big')
