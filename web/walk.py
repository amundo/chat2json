import os

def callback(arg, directory, files):
    for file in files:
        print os.path.join(directory, file), repr(arg)

def find_cha(arg, directory, files):
    for file in files:
        if file.endswith('cha'):
            print os.path.join(directory, file), repr(arg)

os.path.walk(".", find_cha, "secret message")
