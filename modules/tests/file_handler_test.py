import import_modules
from file_handler import file_handler

fileHandler = file_handler()

def test1():
    fileHandler.append_to_file([0, 1, 2, 3, 4, 5, 6, 7])

test1()