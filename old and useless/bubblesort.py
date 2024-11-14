if __name__ == "__main__":
    from sort import Sort
else:
    from .sort import Sort


class bubbleSort(Sort):
    def __init__(self, unsorted, speed):
        super().__init__(unsorted, speed)
        self.index = 0
        self.switches = 1
        self.highest = len(unsorted) - 1


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