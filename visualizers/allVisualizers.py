import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpe
import moviepy.audio.AudioClip as ac
from math import pi, sin, cos

if __name__ == "__main__":
    from visualizers.helpers import rgb, getPitch, sound, Visualizer
else:
    from .helpers import rgb, getPitch, sound, Visualizer


class standardBar(Visualizer):
    def __init__(self, algorithm):
        super().__init__(algorithm)


    def generateImage(self, width, height):
        buffer = int(width/15)
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        for i in range(length := len(self.algorithm.current())):

            val = self.algorithm.current().list[i].val
            increment = (width - 2*buffer)/length
            draw.rectangle(
                [(x:= increment*i - increment/2 + buffer, height - val),
                    (x+increment, height)],
                    fill = (255, 255, 255) if self.algorithm.sorting.list[i] in self.algorithm.accessed() else rgb(val, length)
                )
        return(img)
    

class VSymBar(Visualizer):
    def __init__(self, algorithm):
        super().__init__(algorithm)


    def generateImage(self, width, height):
        buffer = int(width/15)
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        for i in range(self.algorithm.length):

            val = self.algorithm.current().list[i].val
            increment = (width - 2*buffer)/self.algorithm.length
            draw.rectangle(
                [(x:= increment*i - increment/2 + buffer, height/2 - val/2),
                    (x+increment, height/2 + val/2)],
                    fill = (255, 255, 255) if self.algorithm.current().list[i] in self.algorithm.accessed() else rgb(val, self.algorithm.length)
                )
        return(img)
    

class DisparityDots(Visualizer):
    def __init__(self, algorithm):
        super().__init__(algorithm)

    
    def generateImage(self, width, height):
        #print(self.algorithm.timeRatio())

        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        squareSize = 10
        radius = 500

        print('bruh')

        for i in range(length := self.algorithm.length):
            val = self.algorithm.current().list[i].val

            theta = 2*pi * (i/self.algorithm.length)
            #r = radius - abs(val-i+1)
            #r = abs(val-i+1) / (self.algorithm.length/radius)
            #r = radius - (abs(val-i+1) / (self.algorithm.length/radius))
            r = radius * self.distance(val, i)
            color = (255, 255, 255) if self.algorithm.current().list[i] in self.algorithm.accessed() else rgb(val, self.algorithm.length)

            x = r*cos(theta) + width/2
            y = height/2 - (r*sin(theta))

            start = (x, y)
            end = (x + squareSize, y + squareSize)

            draw.rectangle([start, end], fill = color)

        return(img)