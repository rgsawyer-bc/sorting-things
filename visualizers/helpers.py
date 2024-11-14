from math import sin, pi
import numpy as np
import moviepy.editor as mpe
import moviepy.audio.AudioClip as ac

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
        500 + 1.5*i
    )

def make_frame(t, freq=440):
    # Generate a stereo signal (two channels)
    left_channel = np.sin(freq * 2 * np.pi * t)  # Left channel
    right_channel = np.sin(freq * 2 * np.pi * t)  # Right channel
    return np.array([left_channel, right_channel]).T

def sound(freq):
    clip = ac.AudioClip(lambda t: make_frame(t, freq = freq), duration=.008)
    newclip = clip.volumex(.05)
    return(newclip)


class Visualizer():
    def __init__(self, algorithm):
        self.algorithm = algorithm


    def distance(self, val, i): # normalized
        shift = self.algorithm.length / 2
        return(
            (1/shift) * abs(abs(val - i + 1) - shift)
        )


    def generateVideo(self, width, height):
        framelist = []
        audioClips = []
        time = 0
        while self.algorithm.sorted == False:
            #val = self.algorithm.current().accessed()[-1].val
            #audioClips.append(sound(getPitch(val)).set_start(time))
            #time += .016

            framelist.append(self.generateImage(width, height))
            self.algorithm.update()
        framelist.append(self.generateImage(width, height))

        #audioClips = ac.CompositeAudioClip(audioClips)

        print(len(framelist))

        clips = [mpe.ImageClip(np.array(img)).set_duration(.016) for img in framelist]
        video = mpe.concatenate_videoclips(clips)
        #newvideo = video.set_audio(audioClips)
        video.write_videofile(f"videos/{self.algorithm.name}-{self.algorithm.length}-{self.algorithm.speed}.mp4", fps=60)