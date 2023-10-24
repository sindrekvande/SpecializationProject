import import_modules
from file_handler import file

fileHandler = file()

def test1():
    fileHandler.append_to_file([0, 1, 2, 3, 4, 5, 6, 7])

def test2():
    fileHandler.append_to_file()

test2()