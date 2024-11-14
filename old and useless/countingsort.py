if __name__ == "__main__":
    from sort import Sort
    from classes import List
else:
    from .sort import Sort
    from .classes import List

#make countArray and sortArray Lists and change the accessed() function so it counts list accesses properly


class CountingSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = 0
        self.state = 0
        self.countArray = []
        self.max = self.sorting[0]


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
