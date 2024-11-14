from random import shuffle

class Sort():
    def __init__(self, unsorted: list, speed: int):
        self.name = "bubblesort"
        self.sorting = unsorted
        self.speed = speed
        self.iterations = 0
        self.data = []
        self.accessedData = []
        self.length = len(unsorted)

        self.accessedCount = 4
        self.recentlyAccessed = ['' for i in range(self.accessedCount)]

        self.soundTimes = []

    
    def increment(self) -> None:
        if self.iterations % self.speed == 0:
            self.data.append(self.current())
            self.accessedData.append([i for i in self.recentlyAccessed])
        self.iterations += 1


    def access(self, n: int) -> None:
        count = self.accessedCount
        self.recentlyAccessed[1:count] = self.recentlyAccessed[0:count - 1]
        self.recentlyAccessed[0] = n
        # add time to self.soundTimes


class BubbleSort(Sort):
    def __init__(self, unsorted:list, speed: int):
        super().__init__(unsorted, speed)
        self.top = len(self.sorting)

    
    def sort(self):
        switches = 1
        while switches != 0:
            switches = 0
            for i in range(self.top - 1):
                first = self.sorting[i]; self.access(first)
                second = self.sorting[i+1]; self.access(second)
                if first > second:
                    self.sorting[i] = second
                    self.sorting[i+1] = first
                    switches += 1

                self.increment()

            self.top -= 1

    def current(self):
        return [i for i in self.sorting]
    

class MergeSort(Sort):
    def __init__(self, unsorted:list, speed: int) -> None:
        super().__init__(unsorted, speed)

    def merge(self, left:list, right:list) -> list:
        
    


if __name__ == "__main__":
    l = [i for i in range(50)]
    shuffle(l)

    a = BubbleSort(l, 50)
    a.sort()
    print(len(a.accessedData))
    print(len(a.data))