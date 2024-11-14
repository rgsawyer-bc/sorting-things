from numpy import floor

class Elem():
    def __init__(self, val):
        self.val = val
        self.comparisons = 0


    def digit(self, n):
        if n >= 0:
            return(
                int(str(self.val)[n])
            )
        else:
            return(0)
    

    def toBinary(self):
        val = self.val
        digits = []
        while val != 0:
            digits.append(str(int(val - floor(val/2)*2)))
            val = floor(val/2)

        result = Elem(int(''.join(digits[::-1])))
        return(result)
    

    def to10(self):
        val = self.val
        total = 0
        power = 0
        for i in str(val)[::-1]:
            i = int(i)
            total += i * (2**power)
            power += 1

        return(total)


    def __float__(self):
        return float(self.val)
    

    def __lt__(self, other):
        self.comparisons += 1
        other.comparisons += 1
        return float(self) < float(other)


    def __le__(self, other):
        self.comparisons += 1
        other.comparisons += 1
        return float(self) <= float(other)
    

    def __gt__(self, other):
        return not self.__le__(other)


    def __ge__(self, other):
        return not self.__lt_(other)
    

    def __eq__(self, other):
        self.comparisons += 1
        other.comparisons += 1
        try:
            return float(self) == float(other)
        except ValueError:
            return self.val == other
    

    def __add__(self, other):
        return self.val + other.val
    

    def __str__(self):
        return(str(self.val))
    

    def __len__(self):
        return(len(str(self)))


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


    def switch(self, i, j):
        iElem = self[i]
        jElem = self[j]
        self[i] = jElem
        self[j] = iElem
        

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