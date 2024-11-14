if __name__ == "__main__":
    from helpers import rgb, getPitch, sound
else:
    from .helpers import rgb, getPitch, sound

import numpy as np
from PIL import Image, ImageDraw
import moviepy.editor as mpe
import moviepy.audio.AudioClip as ac

class Visualizer():
    def __init__(self, algorithm):
        self.algorithm = algorithm


    def distance(self, val, i): # normalized
        shift = self.algorithm.length / 2
        return(
            (1/shift) * abs(abs(val - i + 1) - shift)
        )


    def generateVideo(self, width = 1920, height = 1440):
        framelist = []
        audioClips = []
        time = 0

        self.algorithm.sort()
        for i in range(len(self.algorithm.data)):
            #val = self.algorithm.current().accessed()[-1].val
            #audioClips.append(sound(getPitch(val)).set_start(time))
            #time += .016

            data = self.algorithm.data[i]
            accessedData = self.algorithm.accessedData[i]

            framelist.append(self.generateImage(data, accessedData, width, height))

        #audioClips = ac.CompositeAudioClip(audioClips)

        print(len(framelist))

        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)
        #newvideo = video.set_audio(audioClips)
        video.write_videofile(f"videos/{self.algorithm.name}-{self.algorithm.length}-{self.algorithm.speed}.mp4", fps=60)


class StandardBar(Visualizer):
    def __init__(self, algorithm):
        super().__init__(algorithm)


    def generateImage(self, data, accessedData, width = 1920, height = 1440):
        buffer = int(width/15)
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        length = self.algorithm.length

        for i, val in enumerate(data):

            increment = (width - 2*buffer)/length
            draw.rectangle(
                [(x:= increment*i - increment/2 + buffer, height - val),
                    (x+increment, height)],
                    fill = (255, 255, 255) if data[i] in accessedData else rgb(val, length)
                )
        return(img)