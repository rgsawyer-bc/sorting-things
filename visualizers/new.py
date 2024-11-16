if __name__ == "__main__":
    from helpers import rgb, getPitch, sound
else:
    from .helpers import rgb, getPitch, sound

import numpy as np
from math import sin, cos, pi
from PIL import Image, ImageDraw
import moviepy.editor as mpe
import moviepy.audio.AudioClip as ac

class Visualizer():
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.length = self.algorithm.length
        self.filePath = f"videos/{self.algorithm.name}-{self.name}-{self.algorithm.length}-{self.algorithm.speed}.mp4"


    def distance(self, val, i): # normalized
        shift = self.algorithm.length / 2
        return(
            (1/shift) * abs(abs(val - i + 1) - shift)
        )
    

    def rawDifference(self, val, i):
        shift = self.algorithm.length / 2
        return(
            (1/shift) * abs(abs(val - i + 1) - shift)
        )
    

    def getColor(self, val: int, accessedData: list, length: int) -> tuple:
        return (255, 255, 255) if val in accessedData else rgb(val, length)


    def generateVideo(self, width = 1920, height = 1440, audio = False):
        framelist = []
        time = 0

        self.algorithm.sort()
        self.algorithm.addData()
        totalData = len(self.algorithm.data)
        for i in range(totalData):
            print((i + 1) / totalData)
            data = self.algorithm.data[i]
            accessedData = self.algorithm.accessedData[i]

            framelist.append(self.generateImage(data, accessedData, width, height))

        print(len(framelist))

        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)

        if audio is False:
            video.write_videofile(self.filePath, fps=60)
        else:
            audioClips = [sound(getPitch(i)).set_start(i) for i in self.algorithm.soundTimes]
            audioClips = ac.CompositeAudioClip(audioClips)
            newvideo = video.set_audio(audioClips)
            newvideo.write_videofile(self.filePath, fps=60)


class StandardBar(Visualizer):
    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.name = "bar"


    def generateImage(self, data, accessedData, width = 1920, height = 1440):
        buffer = int(width/15)
        increment = (width - 2*buffer)/length
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        length = self.algorithm.length

        for i, val in enumerate(data):
            draw.rectangle(
                [(x:= increment*i - increment/2 + buffer, height - val),
                    (x+increment, height)],
                    fill = (255, 255, 255) if data[i] in accessedData else rgb(val, length)
                )
        return(img)
    

class VSymBar(Visualizer):
    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.name = "vsymbar"


    def generateImage(self, data, accessedData, width = 1920, height = 1440):
        buffer = int(width/15)
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        length = self.length

        for i, val in enumerate(data):

            increment = (width - 2*buffer)/length
            draw.rectangle(
                [(x:= increment*i - increment/2 + buffer, height/2 - val/2),
                    (x+increment, height/2 + val/2)],
                    fill = (255, 255, 255) if data[i] in accessedData else rgb(val, length)
                )
        return(img)
    

class DisparityDots(Visualizer):
    def __init__(self, algorithm, newimage = None):
        self.name = "dots"
        super().__init__(algorithm)
        self.image = newimage

    
    def generateImage(self, data, accessedData, width = 1920, height = 1440):
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        squareSize = 10
        radius = 500

        for i, val in enumerate(data):

            theta = 2*pi * (i/self.length)
            r = radius * self.distance(val, i)
            color = self.getColor(val, accessedData, self.length)

            x = r*cos(theta) + width/2
            y = height/2 - (r*sin(theta))

            start = (x, y)
            end = (x + squareSize, y + squareSize)

            if self.image is None:
                draw.rectangle([start, end], outline = color, width = 2)
            else:
                roundedStart = (round(x), round(y))
                img.paste(self.boosh, roundedStart)

        return(img)
    

class VDisparityDots(Visualizer):
    def __init__(self, algorithm, newimage = None):
        self.name = "vdots"
        super().__init__(algorithm)
        self.image = newimage


    def generateImage(self, data, accessedData, width = 1920, height = 1440):
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        buffer = int(width/15)
        increment = (width - 2*buffer)/self.length

        squareSize = 10
        radius = 500

        for i, val in enumerate(data):
            offset = self.distance(val, i)
            color = self.getColor(val, accessedData, self.length)

            x = increment*i - increment/2 + buffer
            y = height/2 + (val - i + 1)/2

            start = (x, y)
            end = (x + squareSize, y + squareSize)

            if self.image is None:
                draw.rectangle([start, end], outline = color, width = 2)
            else:
                roundedStart = (round(x), round(y))
                img.paste(self.boosh, roundedStart)

        return(img)
    

class Diamond(Visualizer):
    def __init__(self, algorithm, newimage = None):
        self.name = "diamond"
        super().__init__(algorithm)


    def generateImage(self, data, accessedData, width = 1920, height = 1440):
        length = self.length
        buffer = int(height/15)
        increment = (height - 2*buffer)/length
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')
        
        xCenter = int(width/2)
        yCenter = int(height/2)

        for i, val in enumerate(data):
            r = ((length - i) * increment) / 2
            indeces = [
                (xCenter + r, yCenter),
                (xCenter, yCenter + r),
                (xCenter - r, yCenter),
                (xCenter, yCenter - r)
            ]

            draw.polygon(indeces, fill = self.getColor(val, accessedData, length))

        return(img)