from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpe
import moviepy.audio.AudioClip as ac
import moviepy.audio.fx.all as all
import numpy as np

from math import sin, pi

def red(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-width/2))+127.5
    )
def green(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-(7*width)/6))+127.5
    )
def blue(x, width = 1920):
    return(
      127.5*sin((pi/width)*(2*x-(11*width)/6))+127.5
    )

def rgb(i, width):
    return(
        (int(red(i, width)), int(green(i, width)), int(blue(i, width)))
    )

def getPitch(i):
    return(
        2**(.01*i) + 500
    )

def make_frame(t, freq=440):
    # Generate a stereo signal (two channels)
    left_channel = np.sin(freq * 2 * np.pi * t)  # Left channel
    right_channel = np.sin(freq * 2 * np.pi * t)  # Right channel
    return np.array([left_channel, right_channel]).T

def sound(freq):
    clip = ac.AudioClip(lambda t: make_frame(t, freq = freq), duration=.016)
    newclip = clip.volumex(.05)
    return(newclip)

class standardBar():
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def generateImage(self, width, height):
        buffer = int(width/15)
        img = Image.new( mode = "RGB", size = (width, height) )
        draw = ImageDraw.Draw(img, 'RGBA')

        for i in range(length := len(self.algorithm.sorting)):

            val = self.algorithm.sorting.list[i].val
            increment = (width - 2*buffer)/length
            draw.rectangle(
                [(x:= increment*i - increment/2 + buffer, height - val),
                    (x+increment, height)],
                    fill = (255, 255, 255) if self.algorithm.sorting.list[i] in self.algorithm.accessed() else rgb(val, length)
                )
        return(img)


    def generateVideo(self, width, height):
        framelist = []
        audioClips = []
        time = 0
        while self.algorithm.sorted == False:
            val = self.algorithm.accessed()[-1].val
            audioClips.append(sound(getPitch(val)).set_start(time))
            time += .016

            framelist.append(self.generateImage(width, height))
            self.algorithm.update()
        framelist.append(self.generateImage(width, height))

        audioClips = ac.CompositeAudioClip(audioClips)
        #audioClips = ac.CompositeAudioClip([sound(400), sound(500)])

        print(len(framelist))

        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)
        newvideo = video.set_audio(audioClips)
        #newvideo = video.set_audio(sound(440).set_start(.016))
        newvideo.write_videofile("output_video.mp4", fps=60)