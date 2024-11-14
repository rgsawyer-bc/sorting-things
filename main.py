from sorts.new import *
from visualizers.new import *

from datetime import datetime



from random import shuffle

l = [i for i in range(1, 501)]

shuffle(l)

b = BubbleSort(l, 500)

#img = DisparityDots(b).generateImage(1920, 1080)

StandardBar(b).generateVideo(1920, 1080)