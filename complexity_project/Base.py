from random import randint


class Base:

    table = []
    n = 0

    def setup(self, n):
        self.n = n
        for i in range(0, n):
            self.table.append(randint(0, 100))

    def function(self):
        for i in range(0, self.n):
            for a in range(0, self.n):
                self.table.append(5)

    def clean_up(self):
        self.table = []

