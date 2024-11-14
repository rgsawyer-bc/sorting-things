if __name__ == "__main__":
    from sort import Sort
    from classes import Elem, List
else:
    from .sort import Sort
    from .classes import Elem, List


class bubbleSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = 0
        self.switches = 1
        self.highest = len(unsorted) - 1
        self.name = "bubblesort"


    def step(self):
        if self.index == self.highest:
            if self.switches == 0:
                self.sorted = True
            self.highest -= 1
            self.index = 0
            self.switches = 0

        first = self.sorting[self.index]
        second = self.sorting[self.index + 1]
        if first > second:
            self.switches += 1
            self.sorting[self.index] = second
            self.sorting[self.index+1] = first

        self.index += 1


    def current(self):
        return self.sorting
    

class CountingSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = 0
        self.state = 0
        self.countArray = []
        self.max = self.sorting[0]
        self.name = "countingsort"


    def step(self):
        print(self.index)
        if self.state == 0:
            self.index += 1
            current = self.sorting[self.index]
            if current > self.max:
                self.max = current

            if self.index == len(self.sorting) - 1:
                self.max = self.max.val
                self.countArray = [0 for i in range(self.max+1)]
                self.index = -1
                self.state = 1


        elif self.state == 1:
            self.index += 1
            self.countArray[self.sorting[self.index].val] += 1

            if self.index == self.length - 1:
                for i in range(1, len(self.countArray)):
                    self.countArray[i] +=  self.countArray[i - 1]
                self.sortArray = [0 for i in range(self.length)]

                self.index = self.length
                self.state = 2


        elif self.state == 2:
            self.index -= 1
            current = self.sorting[self.index].val
            self.sortArray[self.countArray[current] - 1] = current

            if self.index == 0:
                self.sorting = List(self.sortArray) #self.sortArray will already be a list later
                self.sorted = True


    def current(self):
        if self.state != 2:
            return self.sorting
        else:
            return List([self.sorting.list[i].val if self.sortArray[i] == 0 else self.sortArray[i] for i in range(self.length)])
        

class RadixMSD2(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = -1
        self.maxdigits = 0
        self.digit = 0
        self.state = 0

        self.index = -1
        self.buckets = [self.sorting]
        self.initial = List([i.val for i in self.sorting.list])
        self.leftBucket = []
        self.rightBucket = []
        self.bucket = 0
        self.bucketIndex = -1
        self.unused = []

        self.time = 0
        self.maxtime = 0

        self.name = 'radixmsd2'


    def clean(self):
        while [] in self.buckets:
            self.buckets.remove([])


    def error(self):
        output = 0
        current = self.current()
        for i in range(len(current)):
            output += (current[i].val - i + 1)^2

        return output
    

    def timeRatio(self):
        if self.maxtime == 0:
            return 0
        else:
            return self.time/self.maxtime



    def step(self):
        if len(self.current()) != self.length:
            print(self.current())
            print(self)


        if self.state == 0:
            self.index += 1
            current = self.sorting[self.index]
            current = current.toBinary()
            self.sorting[self.index] = current
            self.maxdigits = max([len(str(current)), self.maxdigits])

            if self.index == self.length - 1:
                self.index = -1
                self.state = 1
                self.digit = self.maxdigits
                self.maxtime = self.maxdigits * self.length

                self.unused = [i for i in self.sorting.list]

        
        elif self.state == 1:
            self.time += 1
            self.index += 1
            self.bucketIndex += 1
            currentBucket = self.buckets[self.bucket]
            #print('i', self.index, self.bucketIndex, len(currentBucket))
            current = currentBucket[self.bucketIndex]
            currentDigit = current.digit(len(current) - self.digit)

            if currentDigit == 0:
                self.leftBucket.append(current)
            else:
                self.rightBucket.append(current)
            self.unused.remove(current)

            if self.bucketIndex == len(currentBucket) - 1:
                if len(self.leftBucket) > 0 and len(self.rightBucket) > 0:
                    self.buckets[self.bucket:self.bucket+1] = [self.leftBucket, self.rightBucket]
                    self.bucket += 2
                elif len(self.leftBucket) == 0:
                    self.buckets[self.bucket] = self.rightBucket
                    self.bucket += 1
                else:
                    self.buckets[self.bucket] = self.leftBucket
                    self.bucket += 1


                self.leftBucket = []
                self.rightBucket = []
                self.bucketIndex = -1

                if self.index == self.length - 1:
                    self.index = -1
                    self.bucket = 0
                    self.bucketIndex = -1
                    self.unused = [i for i in self.buckets[0]]
                    self.digit -= 1
                else:
                    self.unused = [i for i in self.buckets[self.bucket]]

            if self.digit == 0:
                self.sorted = True
                self.state = 2


    def __str__(self):
        return(f"""
Total index: {self.index}
Bucket index: {self.bucketIndex}
Bucket: {self.buckets[self.bucket]}
Left bucket: {self.leftBucket}
Right bucket: {self.rightBucket}
Unused: {self.unused}
""")

    def current(self):
        if self.state == 0:
            return self.initial
        
        output = [i for i in self.buckets]
        g = [i for i in output]
        currentBucket = [self.leftBucket, self.unused, self.rightBucket]
        while [] in currentBucket:
            currentBucket.remove([])

        currentBucketOneList = [j for i in currentBucket for j in i]

        output[self.bucket] = currentBucketOneList

        return(
            List([i.to10() for j in output for i in j])
        )
    

class MergeSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.sorting = [[i] for i in unsorted]
        self.merge1 = 0
        self.merge2 = 1

        self.current1 = self.sorting[self.merge1]
        self.current2 = self.sorting[self.merge2]

        self.merge1len = len(self.current1)
        self.merge2len = len(self.current2)

        self.merge1index = 0
        self.merge2index = 0

        self.state = 0

        self.name = "mergesort"


    def step(self):
        if self.state == 1:
            return None

        val1 = self.current1[self.merge1index]
        val2 = self.current2[self.merge2index] if self.merge2index < len(self.current2) else val1 + 1

        if val1 <= val2:
            self.current2.insert(self.merge2index, val1)
            self.current1.remove(val1)
        self.merge2index += 1

        if len(self.current1) == 0:
            self.sorting.pop(self.merge1)
            self.merge1 += 1
            self.merge2 += 1
            self.merge2index = 0

            if len(self.sorting) == 1:
                self.state = 1
                self.sorted = True
                self.merge1 = 0
                self.merge2 = 0

            elif self.merge2 >= len(self.sorting):
                self.merge1 = 0
                self.merge2 = 1
            self.current1 = self.sorting[self.merge1]
            self.current2 = self.sorting[self.merge2]

    def current(self):
        return(List(
            [i for j in self.sorting for i in j]
        ))

a = MergeSort([4,6,2,7,1,8,3,5,9,13,10,12,11], 20)
a.update()
print(a.sorting)

        



