if __name__ == "sorts.sort":
    from .classes import Elem, List
else:
    from classes import Elem, List

class Sort():
    def __init__(self, unsorted, speed):
        self.sorting = List(unsorted)
        self.sorted = False
        self.speed = speed
        self.length = len(unsorted)
        

    def comparisons(self):
        return sum([i.val for i in self.sorting])/2
        
    
    def accesses(self):
        return self.sorting.accesses
    

    def accessed(self):
        return []
        #return self.sorting.recentlyAccessed
    

    def accessedInt(self):
        return [i.val for i in self.accessed()]


    def writes(self):
        return self.sorting.writes


    def str(self):
        return(
            f"""Accesses: {self.accesses}
Comparisons: {self.compares}
Writes: {self.writes}
Sorted: {self.checkSort()}"""
        )


    def checkSort(self):
        return(
            sum([0 if self.sorting[i] <= self.sorting[i+1] else 1 for i in range(len(self.sorting)-1)]) == 0
        )


    def update(self):
        for i in range(self.speed):
            self.step()


    def fullSort(self):
        while self.sorted == False:
            self.update()