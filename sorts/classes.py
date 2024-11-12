class Elem():
    def __init__(self, val):
        self.val = val
        self.comparisons = 0
    

    def __lt__(self, other):
        self.comparisons += 1
        other.comparisons += 1
        return self.val < other.val


    def __le__(self, other):
        self.comparisons += 1
        other.comparisons += 1
        return self.val <= other.val
    

    def __gt__(self, other):
        return not self.__le__(other)


    def __ge__(self, other):
        return not self.__lt_(other)
    

    def __eq__(self, other):
        self.comparisons += 1
        other.comparisons += 1
        return self.val == other.val
    

    def __str__(self):
        return(str(self.val))


class List():
    def __init__(self, vals):
        self.list = [Elem(i) for i in vals]
        self.recentlyAccessed = [Elem(0) for i in range(4)]
        self.accesses = 0
        self.writes = 0


    def updateAccessed(self, new):
        self.recentlyAccessed[3] = self.recentlyAccessed[2]
        self.recentlyAccessed[2] = self.recentlyAccessed[1]
        self.recentlyAccessed[1] = self.recentlyAccessed[0]
        self.recentlyAccessed[0] = new
        

    def __getitem__(self, key):
        self.accesses += 1
        self.updateAccessed(self.list[key])
        return self.list[key]
    

    def __setitem__(self, key, val):
        self.writes += 1
        self.list[key] = val


    def __len__(self):
        return len(self.list)
    

    def __str__(self):
        return(str([i.val for i in self.list]))
        
        
