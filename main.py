from sorts.bubblesort import bubbleSort
from visualizers.standardbar import standardBar



from random import shuffle

l = [i for i in range(1, 1001)]
shuffle(l)

b = bubbleSort(l, 1100)

standardBar(b).generateVideo(1920, 1080)