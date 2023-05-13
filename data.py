import re

class Data:
    def __init__(self):
        self.t = []
        self.A = []
        self.type = None

    def read(self, filename):
        with open(filename, 'r') as file:
            data = file.read()
            for i in data.split('\n'):
                splited_line = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", i)
                if len(splited_line) == 2:
                    self.t.append(float(splited_line[0].strip()))
                    self.A.append(float(splited_line[1].strip()))

    def get_data(self):
        return [self.t, self.A]