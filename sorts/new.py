from random import shuffle
from math import floor
import numpy as np
import random
import time

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

        self.start = time.time()
        self.soundTimes = []


    def addData(self) -> None:
        self.data.append(self.current())
        self.accessedData.append([i for i in self.recentlyAccessed])

    
    def increment(self) -> None:
        if self.iterations % self.speed == 0:
            self.addData()
        self.iterations += 1


    def access(self, n: int) -> None:
        count = self.accessedCount
        self.recentlyAccessed[1:count] = self.recentlyAccessed[0:count - 1]
        self.recentlyAccessed[0] = n
        
        self.soundTimes.append((time.time() - self.start) / self.speed)


    def swap(self, i: int, j: int):
        first = self.sorting[i]
        second = self.sorting[j]
        self.sorting[j] = first; self.sorting[i] = second


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
    

class MergeSort(Sort): # this method is not built for repeated elements
    def __init__(self, unsorted:list, speed: int) -> None:
        super().__init__(unsorted, speed)
        self.sorting = [i for i in unsorted]
        self.splits = [i for i in range(len(unsorted)+1)]
        self.name = "mergesort"


    def oneMerge(self, left: int, middle: int, right: int) -> int | str:
        #print(self.sorting)
        #print(left, middle, right)
        toMove = self.sorting[left]; self.access(toMove)
        if middle == right:
            #print('end')
            self.sorting.remove(toMove)
            self.sorting.insert(middle - 1, toMove)
            self.increment()
            return middle
        else:
            rightElem = self.sorting[middle]; self.access(rightElem)
            if toMove < rightElem:
                #print('insert')
                self.sorting.remove(toMove)
                self.sorting.insert(middle - 1, toMove)
                self.increment()
                return middle
            else:
                #print('shift')
                middle += 1
                self.oneMerge(left, middle, right)
                return middle


    def merge(self, left: int, middle: int, right: int) -> None:
        for i in range(middle - left):
            middle = self.oneMerge(left, middle ,right)


    def sort(self):
        while(len(self.splits)) != 2:
            for i in range(0, len(self.splits) - 2, 2):
                self.merge(self.splits[i], self.splits[i + 1], self.splits[i + 2])
            for i in self.splits[1:-1:2]:
                self.splits.remove(i)
        
        self.data.append(self.current())
        self.accessedData.append([i for i in self.recentlyAccessed])


        # self.splits.remove(middle)


    def current(self):
        return [i for i in self.sorting]


class RadixMSD2(Sort): # also not built for repeated elements
    def __init__(self, unsorted:list, speed: int) -> None:
        super().__init__(unsorted, speed)
        self.splits = [0, len(self.sorting)]
        self.binary = False
        self.name = "radixmsd2"


    def toBinary(self, val: int) -> int:
        if val == 0:
            return 0
        
        digits = []
        while val != 0:
            digits.append(str(int(val - floor(val/2)*2)))
            val = floor(val/2)

        result = int(''.join(digits[::-1]))
        return result
    

    def to10(self, val: int) -> int:
        total = 0
        power = 0
        for i in str(val)[::-1]:
            i = int(i)
            total += i * (2**power)
            power += 1

        return(total)
    

    def convert(self) -> None:
        converted = []
        self.maxDigit = 0
        for i in self.sorting:
            binaried = self.toBinary(i)
            converted.append(binaried)
            self.maxDigit = max(self.maxDigit, len(str(binaried)))
            self.access(i)
            self.increment()
        self.currentDigit = self.maxDigit
        self.sorting = converted
        self.binary = True
    

    def getDigit(self, val: int, digit: int) -> int:
        val = [i for i in str(val)]
        for i in range(self.maxDigit - len(val)):
            val.insert(0, 0)
        return int(val[-digit])
    

    def split(self, left:int, right:int, digit: int, maxdigit = None) -> None:
        if maxdigit is not None:
            self.maxDigit = maxdigit

        middle = left
        toMove = self.sorting[left:right]

        for i in toMove:
            self.access(self.to10(i))
            self.sorting.remove(i)
            if self.getDigit(i, digit) == 0:
                middle += 1
                self.sorting.insert(left, i)
            else:
                self.sorting.insert(right - 1, i)
            self.increment()
        if middle != left and middle != right:
            self.splits.insert(self.splits.index(right), middle)


    def sort(self) -> None:
        self.convert()

        while self.currentDigit != 1:
            splits = [i for i in self.splits]
            for i in range(len(splits) - 1):
                leftSplit = splits[i]
                rightSplit = splits[i + 1]
                self.split(leftSplit, rightSplit, self.currentDigit)

            self.currentDigit -= 1

        self.sorting = [self.to10(i) for i in self.sorting]
        self.binary = False
        self.data.append(self.current())
        self.accessedData.append([i for i in self.recentlyAccessed])
                

    
    def current(self) -> list:
        if self.binary is False:
            return [i for i in self.sorting]
        else:
            return [self.to10(i) for i in self.sorting]

    
class CountingSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = 0
        self.state = 0
        self.countArray = []
        self.max = self.sorting[0]
        self.name = "countingsort"


    def getMax(self):
        for current in self.sorting:
            self.access(current); self.increment()
            if current > self.max:
                self.max = current

        self.countArray = [0 for i in range(self.max + 1)]


    def count(self):
        for current in self.sorting:
            self.access(current); self.increment()
            self.countArray[current] += 1

        for i in range(1, len(self.countArray)):
            self.countArray[i] += self.countArray[i - 1]
        self.sortArray = [0 for i in range(self.length)]


    def finish(self):
        unsorted = [i for i in self.sorting]
        for current in unsorted:
            self.access(current)
            self.sorting[self.countArray[current] - 1] = current
            self.increment()

        self.addData() # no idea why this needs to be here twice but whatever
        self.addData()


    def sort(self):
        self.getMax(); self.count(); self.finish()


    def current(self):
        return [i for i in self.sorting]
    

class QuickSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.splits = [0, len(unsorted)]
        self.name = "quicksort"


    def partition(self, left, right):
        swaps = 0
        i = left - 1
        #pivot = int(random.choice(self.sorting[left:right])); self.access(int(random.choice(self.sorting[left:right])))
        pivot = self.sorting[right]

        for j in range(left, right):
            self.increment()
            current = self.sorting[j]; self.access(current)
            if current < pivot:
                swaps = 1
                i += 1
                self.access(self.sorting[i])
                self.swap(i, j)

        self.swap(i + 1, right)
        #if i + 1 not in self.splits:
        #    self.splits.insert(self.splits.index(right), i + 1)

        return(i + 1)


    def quickSort(self, low, high):
        #swaps = 1
        #while swaps != 0:
        #    swaps = 0
        #    splits = [i for i in self.splits]
        #    for i in range(len(splits) - 1):
        #        swaps += self.partition(splits[i], splits[i+1])
        if low < high:
            pi = self.partition(low, high)
            print('p', pi)
            self.quickSort(low, pi - 1)
            self.quickSort(pi + 1, high)

    
    def sort(self):
        self.quickSort(0, len(self.sorting) - 1)

    def current(self):
        return [i for i in self.sorting]



if __name__ == "__main__":
    #l1 = [10, 7, 8, 9, 1, 5]
    l1 = [i for i in range(100)]; shuffle(l1)
    a = QuickSort(l1, 1)

    a.sort(0, len(l1) - 1)
    print(a.sorting)


    