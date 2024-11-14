if __name__ == "__main__":
    from sort import Sort
    from classes import Elem, List
else:
    from .sort import Sort
    from .classes import Elem, List


class RadixLSD2(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = -1
        self.maxdigits = 0
        #self.bottomSwitch = 0
        #self.topSwitch = self.length - 1
        #self.countZero = 0
        #self.splitIndex = 1
        self.digit = 0
        self.state = 0

        #self.lifted = 0
        #self.liftedIndex = 0

        #self.currentSplit = 0
        #self.splits = [0, self.length]

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

        #print(currentBucket)

        currentBucketOneList = [j for i in currentBucket for j in i]

        #output[self.bucket:self.bucket+len(currentBucket)] = currentBucket
        output[self.bucket] = currentBucketOneList

        #if len(output) != self.length:
        #    print('bruh', [[str(j) for j in i] for i in g])
        #    print('fail', [[str(j) for j in i] for i in currentBucket])
        #    print('waaa', [[str(j) for j in i] for i in output])
        #    print(self.bucket)

        return(
            List([i.to10() for j in output for i in j])
        )
        

    

#a = RadixLSD2([6,3,5,7,1,8,2,4], 8)

#for i in range(8):
#    a.step()

#for i in range(8):
#    a.step()
#    a.step()

#for i in range(8):
#    a.update()

#print(a.current())

