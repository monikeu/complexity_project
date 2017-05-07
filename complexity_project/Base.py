from random import randint


class Base:
    alist = [] # sample
    n = 0

    # setup should contain variables and structures initializations etc
    # calculated complexity is n-dependent
    def setup(self, n):
        self.n = n #sample
        for i in range(0, n):
            self.alist.append(randint(0, 100)) # need to import randint
        # pass

    # definition of to-measure function
    def function(self):
        sorted(self.alist) # sample
        # pass

    # cleaning up, deleting structures, etc
    def clean_up(self):
        self.alist = [] # sample
        # pass
