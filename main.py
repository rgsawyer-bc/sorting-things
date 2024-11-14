from sorts.allSorts import *
from visualizers.allVisualizers import *

from PIL import *

from datetime import datetime



from random import shuffle

l = [i for i in range(1, 501)]

shuffle(l)

b = MergeSort(l, 10)

time1 = datetime.now()
print(b.current())
time2 = datetime.now()
print(time2 - time1)

#img = DisparityDots(b).generateImage(1920, 1080)

DisparityDots(b).generateVideo(1920, 1080)