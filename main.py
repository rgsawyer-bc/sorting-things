from sorts.new import *
from visualizers.new import *

from datetime import datetime



from random import shuffle

l = [i for i in range(1, 1001)]

shuffle(l)

b = QuickSort(l, 10)

#img = DisparityDots(b).generateImage(1920, 1080)
boosh = Image.open("visualizers/boosh kirby.png")
smallBoosh = boosh.resize((20, 20))

DisparityDots(b).generateVideo(1920, 1080)