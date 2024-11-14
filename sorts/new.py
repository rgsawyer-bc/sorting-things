from random import shuffle

class Sort():
    def __init__(self, unsorted: list, speed: int):
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
        self.name = "bubblesort"

    
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
    

class MergeSort(Sort): # make this an in-place method using the left, middle, right thing
    def __init__(self, unsorted:list, speed: int) -> None:
        super().__init__(unsorted, speed)
        self.sorting = [[i] for i in unsorted]

    def merge(self, left: int, middle: int, right: int) -> None: # there is definitely a better way to do this but this works for now
        if right is None:
            return left

        # stuff for keeping self.sorting up to date


        output = [i for i in right]
        i = 0
        rightElem = right[0]; self.access(rightElem)
        for leftElem in left:
            self.access(leftElem)
            while leftElem > rightElem:
                i += 1
                if i >= len(output):
                    break
                rightElem = output[i]; self.access(rightElem)
            output.insert(i, leftElem)
            i += 1
            self.increment()

        return(output)
    

    def mergeList(self, lis: list[list]) -> list:
        return self.merge(lis[0], lis[1])
    

    def mergeAll(self) -> list[list]:
        lis = self.sorting
        if len(lis) % 2 == 0:
            partitions = [[lis[i], lis[i+1]] for i in range(0, len(lis), 2)]
        else:
            partitions = [[lis[i], lis[i+1]] for i in range(0, len(lis) - 1, 2)] + [[lis[-1], None]]

        for partition in partitions:
            self.mergeList(partition)

    

    def sort(self) -> list[list]:
        while len(self.sorting) != 1:
            self.sorting = self.mergeAll(self.sorting)


    def current(self):
        return [i for j in self.sorting for i in j]

    


if __name__ == "__main__":
    l1 = [i for i in range(11,22,2)]
    l2 = [i for i in range(2,13,2)]

    a = MergeSort([5,2,3,1,4], 1)

    a.sort()
    print(a.sorting)

    