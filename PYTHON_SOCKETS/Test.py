import sys
import pickle
import random

class Test:
    def __init__(self, msg=""):

        self.lst = [msg] + list(range(10))
        self.lst2 = list(range(0, 20))

        self.messages = ['hello world!', 'this is a socket']

        self.additions = list()

    def size(self):
        return sys.getsizeof(self)

    def header(self):
        return pickle.dumps(dict({
            'size' : sys.getsizeof(self),
            'id' : random.randint(1, 5000),
            }))

    def execute(self):
        print("item 1")
        [print(l) for l in self.lst]

        print("\nitem2")
        [print(l) for l in self.lst2]

        print("\nmessages")
        [print(l) for l in self.messages]

    def add_data(self, msg):
        self.additions.append(msg)

    def show_additions(self):
        [print(l) for l in self.additions]


