import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpe
import moviepy.audio.AudioClip as ac

if __name__ == "__main__":
    from visualizers.helpers import rgb, getPitch, sound, Visualizer
else:
    from .helpers import rgb, getPitch, sound, Visualizer


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